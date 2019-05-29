#!/usr/bin/env python3

"""Main script for the application."""

from tkinter import Tk
from tkinter.ttk import Notebook
from utils_gui import *
from utils import Machine

if __name__ == '__main__':
    # machine obj, initially with 0 states
    machine = Machine(0)

    # initialize window
    root = Tk()
    root.title('DTM Simulator')
    root_width = root.winfo_reqwidth()
    root_height = root.winfo_reqheight()
    x_offset = int(root.winfo_screenwidth() / 3 - root_width / 3)
    y_offset = int(root.winfo_screenheight() / 3 - root_height / 3)
    root.geometry('500x500+{}+{}'.format(x_offset, y_offset))
    root.minsize(480,440)

    # intialize display and control of the GUI
    display = Display(root, machine)
    control = Notebook(root)
    control.pack(side='bottom', fill='x')

    # initialize the three panels of the control
    states_panel = StatesPanel(control, machine, display.info_manager, display)
    trans_panel = TransitionsPanel(control, machine, display.info_manager, display)
    test_panel = TestingPanel(control, machine, display.info_manager, display)

    # set the three panels as a notebook
    control.add(states_panel, text='States')
    control.add(trans_panel, text='Transitions')
    control.add(test_panel, text='Testing')

    root.mainloop()
