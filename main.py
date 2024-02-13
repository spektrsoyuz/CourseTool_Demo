"""
main.py
Created by Seth Christie on 2/4/2024
"""
import yaml
import sv_ttk
import tkinter as tk
from tkinter import ttk
import course_functions as cf

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


# ---------------------------------------------------- classes ---------------------------------------------------------


class AppButton(ttk.Frame):
    def __init__(self, parent, text="", command=None, style=None):
        ttk.Frame.__init__(self, parent, height=40, width=250, style="TButton")

        self.pack_propagate(False)
        self._btn = ttk.Button(self, text=text, command=command, style=style)
        self._btn.pack(fill=tk.BOTH, expand=1)


class MainFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        options = {'padx': 2.5, 'pady': 2.5}

        # Configure style
        style = ttk.Style()
        style.configure('TButton', font=('Calibri', '14', 'normal'))

        # Buttons
        self.button_example = AppButton(self, 'Example Button', style='TButton')

        # Pack widgets onto frame
        self.button_example.grid(**options, column=0, row=0)

        # Pack frame onto container
        self.pack(**options)


class App(tk.Tk):
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


# ----------------------------------------------------- main -----------------------------------------------------------

if __name__ == '__main__':
    config = readConfig('config.yml')

    '''
    # Run the script to fetch and parse course data
    undergradData = cf.getCourseData('summer24_all.csv', config[0], config[2], False)
    gradData = cf.getCourseData('summer24_grad.csv', config[1], config[3], False)

    # Export undergrad/grad course data
    cf.exportCourses(undergradData, 'json', 'Exports/s24_undergrad.json')
    cf.exportCourses(undergradData, 'xlsx', 'Exports/s24_undergrad.xlsx')
    cf.exportCourses(gradData, 'json', 'Exports/s24_grad.json')
    cf.exportCourses(gradData, 'xlsx', 'Exports/s24_grad.xlsx')

    # Parse ME Electives from term
    me_electives = cf.getMEElectives('Exports/s24_undergrad.json')

    # Export ME Electives
    cf.exportCourses(me_electives, 'json', 'Exports/s24_mechelv.json')
    cf.exportCourses(me_electives, 'xlsx', 'Exports/s24_mechelv.xlsx')
    cf.exportCourses(me_electives, 'yaml', 'Exports/s24_mechelv.yml')
    '''

    # Configure Application
    app = App()
    app.protocol("WM_DELETE_WINDOW", close_window)
    frame = MainFrame(app)

    # Start app
    app.mainloop()
