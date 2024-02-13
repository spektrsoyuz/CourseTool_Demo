"""
main.py
Created by Seth Christie on 2/4/2024
"""
import yaml
import course_funcs as cf

# ----------------------------------------------------- main -----------------------------------------------------------

if __name__ == '__main__':
    # Read config.yml
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)

    undergrad_catalog = config['catalog']['undergrad']['tags']
    grad_catalog = config['catalog']['undergrad']['tags']
    undergrad_url = config['catalog']['undergrad']['url']
    grad_url = config['catalog']['grad']['url']

    # Run the script to fetch and parse course data
    undergradData = cf.getCourseData('summer24_all.csv', undergrad_catalog, undergrad_url, False)
    gradData = cf.getCourseData('summer24_grad.csv', grad_catalog, grad_url, False)
    cf.exportCourses(undergradData, 'json', 'Exports/s24_undergrad.json')
    cf.exportCourses(undergradData, 'xlsx', 'Exports/s24_undergrad.xlsx')
    cf.exportCourses(gradData, 'json', 'Exports/s24_grad.json')
    cf.exportCourses(gradData, 'xlsx', 'Exports/s24_grad.xlsx')

    # Get ME Electives from term
    me_electives = cf.getMEElectives('Exports/s24_undergrad.json')
    cf.exportCourses(me_electives, 'json', 'Exports/s24_mechelv.json')
    cf.exportCourses(me_electives, 'xlsx', 'Exports/s24_mechelv.xlsx')
    cf.exportCourses(me_electives, 'yaml', 'Exports/s24_mechelv.yml')
