#!/usr/bin/env python3

# Main script for the GUI version of DTM Simulator
# Currently a work in progress

from tkinter import *
from utils import Machine, Transition

def update_info():
    global machine, m_info_var
    info = ''
    for desc, value in machine.get_info().items():
        info += '{}: {}'.format(desc, value) + '\n'
    m_info_var.set(info)

def add_state():
    global machine
    machine.add_state()
    update_info()

def set_final():
    global machine, state_entry
    try:
        target_state = int(state_entry.get())
        machine.set_final_state(target_state)
    except:
        # can update error message var here
        pass
    state_entry.delete(0, 'end')
    update_info()

def set_nonfinal():
    global machine, state_entry
    try:
        target_state = int(state_entry.get())
        machine.set_nonfinal_state(target_state)
    except:
        # can update error message var here
        pass
    state_entry.delete(0, 'end')
    update_info()

def del_state():
    global machine, state_entry
    try:
        target_state = int(state_entry.get())
        machine.del_state(target_state)
    except:
        # can update error message var here
        pass
    state_entry.delete(0, 'end')
    update_info()

machine = Machine(0)

root = Tk()
root.title('DTM Simulator')
window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()
x_offset = int(root.winfo_screenwidth()/3 - window_width/3)
y_offset = int(root.winfo_screenheight()/3 - window_height/3)
root.geometry('500x500+{}+{}'.format(x_offset, y_offset))

display = Frame(root, bg='gray')
control = Frame(display)

add_state_btn = Button(control, text='Add state', command=add_state)
add_state_btn.grid(row=0,column=0)
state_entry_label = Label(control, text='Enter state number:')
state_entry_label.grid(row=1,column=0)
state_entry = Entry(control, width=3)
state_entry.grid(row=1,column=1)
set_final_btn = Button(control, text='Set as final', command=set_final)
set_final_btn.grid(row=1,column=2)
set_nonfinal_btn = Button(control, text='Set as non-final', command=set_nonfinal)
set_nonfinal_btn.grid(row=1,column=3)
del_state_btn = Button(control, text='Delete state', command=del_state)
del_state_btn.grid(row=1,column=4)

control.pack(side='bottom', fill='x')
info = Frame(display, width=250, bg='red')

m_info_var = StringVar(info)
machine_info = Label(info, textvariable=m_info_var)
machine_info.pack()

info.pack(side='right', fill='y')
display.pack(fill='both', expand=True)

update_info()
root.minsize(250,250)
root.mainloop()