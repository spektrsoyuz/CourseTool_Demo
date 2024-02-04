"""
CourseTool
"""

import course_funcs

# constants
catalog_url = 'https://catalog.kettering.edu/coursesaz/undergrad/'
catalog = [
    'BIOL', 'BUSN', 'CHME', 'CHEM', 'COMM', 'CE', 'CS', 'ECON', 'ECE', 'EE', 'ENGR', 'EP', 'HIST',
    'HUMN', 'IME', 'CILE', 'LANG', 'LA', 'LIT', 'MGMT', 'MATH', 'MECH', 'MEDI', 'PHIL', 'PHYS', 'PSYC',
    'SSCI', 'SOC'
]

# ------------------------------------------------------- main ---------------------------------------------------------

if __name__ == '__main__':
    # Run the script to fetch and parse course data
    course_funcs.getCourseData('summer24', catalog, catalog_url, True)
