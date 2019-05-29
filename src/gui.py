#!/usr/bin/env python3

# Main script for the GUI version of DTM Simulator
# Currently a work in progress

from tkinter import Tk
from tkinter.ttk import Notebook
from utils_gui import *
from utils import Machine

if __name__ == '__main__':
    machine = Machine(0)

    root = Tk()
    root.title('DTM Simulator')
    root_width = root.winfo_reqwidth()
    root_height = root.winfo_reqheight()
    x_offset = int(root.winfo_screenwidth() / 3 - root_width / 3)
    y_offset = int(root.winfo_screenheight() / 3 - root_height / 3)
    root.geometry('500x500+{}+{}'.format(x_offset, y_offset))

    display = Display(root, machine)
    control = Notebook(root)
    control.pack(side='bottom', fill='x')

    states_panel = StatesPanel(control, machine, display.info_manager, display)
    trans_panel = TransitionsPanel(control, machine, display.info_manager, display)
    test_panel = TestingPanel(control, machine, display.info_manager, display)

    control.add(states_panel, text='States')
    control.add(trans_panel, text='Transitions')
    control.add(test_panel, text='Testing')

    root.minsize(480,440)
    root.mainloop()