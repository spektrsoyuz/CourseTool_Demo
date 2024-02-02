"""
CourseTool
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
import json
import warnings

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

# globals
df = pd.DataFrame  # DataFrame to store course data
parsedData = BeautifulSoup()  # BeautifulSoup object to store parsed HTML data
courseList = {}  # Dictionary to store course information
term = ''  # Variable to store the academic term

# catalog constants
catalog_url = 'https://catalog.kettering.edu/coursesaz/undergrad/'
catalog = [
    'BIOL', 'BUSN', 'CHME', 'CHEM', 'COMM', 'CE', 'CS', 'ECON', 'ECE', 'EE', 'ENGR', 'EP', 'HIST',
    'HUMN', 'IME', 'CILE', 'LANG', 'LA', 'LIT', 'MGMT', 'MATH', 'MECH', 'MEDI', 'PHIL', 'PHYS', 'PSYC',
    'SSCI', 'SOC'
]


def strip_html(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    plain_text = soup.get_text()
    return plain_text


def getCourseData():
    global df, parsedData, courseList
    df = pd.read_csv(term + '.csv')  # Read course data from a CSV file

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
            for courseblock in courseblocks:
                course = {}
                courseblocktitle = courseblock.find('p', 'courseblocktitle').text.split('\xa0')

                subjects = df['SUBJ'].values
                tags = df['NUMB'].values
                courseids = [f'{subject}-{tag}' for subject, tag in zip(subjects, tags)]

                if courseblocktitle[0] in courseids:
                    courseblockdesc = str(courseblock.find('p', 'courseblockdesc')).split('<br/>')

                    coreqs = 'None'
                    prereqs = 'None'
                    standing = 'Freshman'
                    sections = {}

                    desc = strip_html(courseblockdesc[-3]).replace('\n', ' ')

                    for line in courseblockdesc:
                        # check for class standing
                        if 'Minimum Class Standing:' in line:
                            standing = line.split(':')[1].strip()

                        # check for prereqs
                        if 'Prerequisites:' in line:
                            prereqs = strip_html(line).replace('Prerequisites: ', '')

                        # check for coreqs
                        if 'Corequisites:' in line:
                            coreqs = strip_html(line).replace('Corequisites: ', '')

                    # check if special topics
                    if '391' in courseblocktitle[0]:
                        desc = 'None'

                    title_parts = courseblocktitle[0].split('-')

                    # handle section data
                    df_sections = df[(df['SUBJ'] == title_parts[0]) & (df['NUMB'] == title_parts[1])].copy()
                    df_sections = df_sections.drop(columns=['SUBJ', 'NUMB', 'CRN', 'CH', 'TITLE'])
                    dict_sections = df_sections.to_dict(orient='records')

                    for entry in dict_sections:
                        # parse course dates
                        dates = [entry['M'], entry['T'], entry['W'], entry['TH'], entry['F']]
                        dates = [item for item in dates if item != ' ']

                        # get section data
                        section = entry['SEC']
                        instructor = entry['INSTRUCTOR']
                        time = entry['TIME']
                        date = ', '.join(dates)
                        building = entry['BLDG']
                        room = entry['ROOM']
                        avail = entry['AVAIL']

                        # format section block
                        sectionblock = {
                            'instructor': instructor,
                            'time': time,
                            'date': date,
                            'building': building,
                            'room': room,
                            'avail': avail
                        }

                        # dump block into sections
                        sections[section] = sectionblock

                    # dump course data into course
                    course['tag'] = courseblocktitle[0]
                    course['name'] = courseblocktitle[2].replace('\n', '')
                    course['coreqs'] = coreqs.replace('\n', '')
                    course['prereqs'] = prereqs.replace('\n', '')
                    course['standing'] = standing
                    course['desc'] = desc.replace('  ', ' ')
                    course['sections'] = sections
                    course['credits'] = courseblocktitle[-1].replace(' Credits', '')

                    # dump courseblock into courses
                    courses[courseblocktitle[0]] = course

            courseList[cat] = courses

    # Save the parsed course information in a JSON file
    filename = term + '.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(courseList, file, ensure_ascii=False, indent=2)
    print('\nSaved courses to', filename)


if __name__ == '__main__':
    term = 'summer24'

    # Run the script to fetch and parse course data
    getCourseData()
