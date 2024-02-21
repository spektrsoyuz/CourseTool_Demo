"""
main.py
Created by Seth Christie on 2/4/2024
"""
import yaml
import sv_ttk
import tkinter as tk
from tkinter import ttk
from ctypes import windll

import course_functions as cf
import tk_interface as tki

# Constants
APP_NAME = 'Course Tool'
APP_WIDTH = 400
APP_HEIGHT = 600


# --------------------------------------------------- functions --------------------------------------------------------

def close_window():
    """
    Function to close the application window
    :return: None
    """
    app.destroy()


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


# ---------------------------------------------------- classes ---------------------------------------------------------


class AppButton(ttk.Frame):
    """
    This class represents a Custom Frame for displaying a Button.
    """

    def __init__(self, parent, text="", command=None, style=None, height=0, width=0):
        ttk.Frame.__init__(self, parent, height=height, width=width, style="TButton")

        self.pack_propagate(False)
        self._btn = ttk.Button(self, text=text, command=command, style=style)
        self._btn.pack(fill=tk.BOTH, expand=1)


class App(tk.Tk):
    """
    This class represents the Application container as a whole, which is responsible for displaying the Application's
    user interface.
    """

    def __init__(self):
        super().__init__()

        # Configure the root window
        self.title(APP_NAME)
        self.resizable(False, False)

        # Center window and set dimensions
        x = int((self.winfo_screenwidth() / 2) - (APP_WIDTH / 2))
        y = int((self.winfo_screenheight() / 2) - (APP_HEIGHT / 2))
        self.geometry(f'{APP_WIDTH}x{APP_HEIGHT}+{x}+{y}')

        # Set theme
        sv_ttk.set_theme("dark")

        # Add frames to application
        tki.MainFrame(self)


# ----------------------------------------------------- main -----------------------------------------------------------

if __name__ == '__main__':
    # Run script
    # runScript()

    # Configure Application
    app = App()
    app.protocol("WM_DELETE_WINDOW", close_window)
    windll.shcore.SetProcessDpiAwareness(1)

    # Start app
    app.mainloop()
