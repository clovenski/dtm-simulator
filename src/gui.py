#!/usr/bin/env python3

# Main script for the GUI version of DTM Simulator
# Currently a work in progress

from tkinter import Tk, Canvas, ttk
from utils_gui import *
from utils import Machine

if __name__ == '__main__':
    machine = Machine(0)

    root = Tk()
    root.title('DTM Simulator')
    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()
    x_offset = int(root.winfo_screenwidth()/3 - window_width/3)
    y_offset = int(root.winfo_screenheight()/3 - window_height/3)
    root.geometry('500x500+{}+{}'.format(x_offset, y_offset))

    display = Canvas(root, bg='gray')
    control = ttk.Notebook(display)
    control.pack(side='bottom', fill='x')
    info_manager = InfoManager(display, machine)

    states_panel = StatesPanel(control, machine, info_manager)
    trans_panel = TransitionsPanel(control, machine, info_manager)
    test_panel = TestingPanel(control, machine)

    control.add(states_panel, text='States')
    control.add(trans_panel, text='Transitions')
    control.add(test_panel, text='Testing')

    display.pack(fill='both', expand=True)

    info_manager.update_info()
    root.minsize(250,250)
    root.mainloop()