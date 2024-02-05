"""
course_funcs.py
Created by Seth Christie on 2/4/2024
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
import json
import warnings

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)


# -------------------------------------------------- functions ---------------------------------------------------------

def strip_html(html_text):
    """
    Function to strip HTML code from a String
    :param html_text: HTML code to be stripped
    :return: String with HTML code stripped
    """
    soup = BeautifulSoup(html_text, 'html.parser')
    plain_text = soup.get_text()
    return plain_text


def getCourseData(term, catalog, catalog_url, exportJSON, includeAll):
    """
    Function to parse through Kettering Courses A-Z and the Kettering
    Argos Class Schedule to create a dictionary containing available courses
    for a given term.
    :param term: Specified school term      'winter24', 'spring23', etc.
    :param catalog: List of acceptable course tags
    :param catalog_url: URL to the course catalog (undergrad/grad)
    :param exportJSON: Should the function export a json file containing the courses?
    :param includeAll: Should the function include courses with no sections?
    :return: Dictionary containing list of available courses
    """
    courseList = {}  # Dictionary to store course information
    try:
        df = pd.read_csv(f'{term}.csv')  # Read course data from a CSV file
    except FileNotFoundError as e:
        print(e)
        exit(1)

    # Clean up dataframe
    df = df.drop(columns=['TYPE', 'PART', 'MAX', 'WL_Max', 'WL_Actual', 'CAMPUS'])

    for cat in catalog:
        if cat in df['SUBJ'].values:
            courses = {}

            print(f'Parsing data for {cat}')
            url = f'{catalog_url}{cat.lower()}/'
            req = requests.get(url)
            htmlData = req.content
            parsedData = BeautifulSoup(htmlData, "html.parser")

            # Extract course information from the parsed HTML
            courseblocks = parsedData.find_all('div', 'courseblock')

            # Iterate over each courseblock and add to dictionary
            for courseblock in courseblocks:
                courseblocktitle = courseblock.find('p', 'courseblocktitle').text.split('\xa0')

                subjects = df['SUBJ'].values
                tags = df['NUMB'].values
                courseids = [f'{subject}-{tag}' for subject, tag in zip(subjects, tags)]

                if courseblocktitle[0] not in courseids and not includeAll:
                    continue

                courseblockdesc = str(courseblock.find('p', 'courseblockdesc')).split('<br/>')

                coreqs = 'None'
                prereqs = 'None'
                standing = 'Freshman'

                desc = strip_html(courseblockdesc[-3]).replace('\n', ' ')

                for line in courseblockdesc:
                    # Check for class standing
                    if 'Minimum Class Standing:' in line:
                        standing = line.split(':')[1].strip()

                    # Check for prereqs
                    if 'Prerequisites:' in line:
                        prereqs = strip_html(line).replace('Prerequisites: ', '')

                    # Check for coreqs
                    if 'Corequisites:' in line:
                        coreqs = strip_html(line).replace('Corequisites: ', '')

                # Check if special topics
                if '391' in courseblocktitle[0]:
                    desc = 'None'

                # Format course
                course = {
                    'tag': courseblocktitle[0],
                    'name': courseblocktitle[2].replace('\n', ''),
                    'coreqs': coreqs.replace('\n', ''),
                    'prereqs': prereqs.replace('\n', ''),
                    'standing': standing,
                    'desc': desc.replace('  ', ' '),
                    'sections': getSections(df, courseblocktitle),
                    'credits': courseblocktitle[-1].replace(' Credits', '')
                }

                # Dump courseblock into courses
                courses[courseblocktitle[0]] = course

            # Add course dictionary to final course list
            courseList[cat] = courses

    # Save the parsed course information in a JSON file
    if exportJSON:
        filename = term + '.json'
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(courseList, file, ensure_ascii=False, indent=2)
        print(f'\nSaved courses to {filename}.')

    return courseList


def getSections(df, course):
    """
    Function to return a dictionary containing each section for a given course
    :param df: Dataframe containing sections
    :param course: Course tag       'MATH-204', 'ECON-201', etc.
    :return:
    """
    sections = {}
    title_parts = course[0].split('-')
    df_sections = df[(df['SUBJ'] == title_parts[0]) & (df['NUMB'] == title_parts[1])].copy()
    dict_sections = df_sections.to_dict(orient='records')

    for entry in dict_sections:
        # Parse course dates
        dates = [entry['M'], entry['T'], entry['W'], entry['TH'], entry['F']]
        dates = [item for item in dates if item != ' ']

        # Get section data
        section = entry['SEC']
        instructor = entry['INSTRUCTOR']
        time = entry['TIME']
        date = ', '.join(dates)
        building = entry['BLDG']
        room = entry['ROOM']
        avail = entry['AVAIL']

        # Format section block
        sectionblock = {
            'instructor': instructor,
            'time': time,
            'date': date,
            'building': building,
            'room': room,
            'avail': avail
        }

        # Dump block into sections
        sections[section] = sectionblock

    return sections
