"""
main.py
Created by Seth Christie on 2/4/2024
"""
import course_funcs

# constants
undergrad = 'https://catalog.kettering.edu/coursesaz/undergrad/'
undergrad_catalog = [
    'BIOL', 'BUSN', 'CHME', 'CHEM', 'COMM', 'CE', 'CS', 'ECON', 'ECE', 'EE', 'ENGR', 'EP', 'HIST', 'HUMN', 'IME',
    'CILE', 'LANG', 'LA', 'LIT', 'MGMT', 'MATH', 'MECH', 'MEDI', 'PHIL', 'PHYS', 'PSYC', 'SSCI', 'SOC'
]

grad = 'https://catalog.kettering.edu/coursesaz/grad/'
grad_catalog = [
    'ACCT', 'BUSN', 'COMM', 'CE', 'CS', 'ECE', 'EE', 'ENGR', 'FINC', 'IME', 'ISYS', 'MFGO', 'MGMT', 'MKRT', 'MATH',
    'MECH'
]

# ----------------------------------------------------- main -----------------------------------------------------------

if __name__ == '__main__':
    # Run the script to fetch and parse course data
    courseData = course_funcs.getCourseData('summer24', 'undergrad', undergrad_catalog, undergrad, True, False)

    # Get ME Electives from term
    me_electives = course_funcs.getMEElectives('summer24_undergrad.json', True, 'Exports/summer24_MECHELV.json')
