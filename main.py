"""
main.py
Created by Seth Christie on 2/4/2024
"""
import yaml
import course_functions as cf


# --------------------------------------------------- functions --------------------------------------------------------


def readConfig(filename):
    """
    Function to read the config file and output parameters
    :param filename: Name of the config file
    :return: List of config parameters
    """
    with open(filename, 'r') as file:
        cfg = yaml.safe_load(file)
        undergrad_catalog = cfg['catalog']['undergrad']['tags']
        grad_catalog = cfg['catalog']['undergrad']['tags']
        undergrad_url = cfg['catalog']['undergrad']['url']
        grad_url = cfg['catalog']['grad']['url']
    return [undergrad_catalog, grad_catalog, undergrad_url, grad_url]


def runScript():
    config = readConfig('config.yml')

    # Run the script to fetch and parse course data
    undergradData = cf.getCourseData('summer24_all.csv', config[0], config[2], False)
    gradData = cf.getCourseData('summer24_grad.csv', config[1], config[3], False)

    # Export undergrad/grad course data
    cf.exportCourses(undergradData, 'json', 'Exports/s24_undergrad.json')
    cf.exportCourses(undergradData, 'xlsx', 'Exports/s24_undergrad.xlsx')
    cf.exportCourses(gradData, 'json', 'Exports/s24_grad.json')
    cf.exportCourses(gradData, 'xlsx', 'Exports/s24_grad.xlsx')

    # Parse ME Electives from terms
    me_electives = cf.getMEElectives('Exports/s24_undergrad.json')

    # Export ME Electives
    cf.exportCourses(me_electives, 'json', 'Exports/s24_mechelv.json')
    cf.exportCourses(me_electives, 'xlsx', 'Exports/s24_mechelv.xlsx')
    cf.exportCourses(me_electives, 'yaml', 'Exports/s24_mechelv.yml')


# ----------------------------------------------------- main -----------------------------------------------------------

if __name__ == '__main__':
    # Run script
    runScript()
