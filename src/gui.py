#!/usr/bin/env python3

# Main script for the GUI version of DTM Simulator
# Currently a work in progress

from tkinter import *
from tkinter import ttk
from utils import Machine, Transition, TestingState

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

def add_transition():
    global machine, f_state_entry, t_state_entry, cnf_entry
    try:
        machine.add_transition(int(f_state_entry.get()), int(t_state_entry.get()), cnf_entry.get())
    except:
        # can update error message var here
        pass
    f_state_entry.delete(0, 'end')
    t_state_entry.delete(0, 'end')
    cnf_entry.delete(0, 'end')
    update_info()

def del_transition():
    global machine, f_state_entry, t_state_entry, cnf_entry
    try:
        machine.del_transition(f_state_entry.get(), t_state_entry.get(), cnf_entry.get())
    except:
        # can update error message var here
        pass
    f_state_entry.delete(0, 'end')
    t_state_entry.delete(0, 'end')
    cnf_entry.delete(0, 'end')
    update_info()

def run_test():
    global machine, next_btn, test_str_entry, as_function_var, tape_result, result
    result.config(text='', bg='white')
    as_function = as_function_var.get()
    results = machine.compute(test_str_entry.get(), as_function=as_function)
    if not as_function:
        tape_result.config(text=results[1])
        if results[0]:
            result.config(text='Accepted', bg='green')
        else:
            result.config(text='Rejected', bg='red')
    else:
        tape_result.config(text=results)

def next():
    pass

machine = Machine(0)

root = Tk()
root.title('DTM Simulator')
window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()
x_offset = int(root.winfo_screenwidth()/3 - window_width/3)
y_offset = int(root.winfo_screenheight()/3 - window_height/3)
root.geometry('500x500+{}+{}'.format(x_offset, y_offset))

display = Frame(root, bg='gray')
control = ttk.Notebook(display)

control1 = Frame(control, bg='yellow')
control1.pack(fill='x')

add_state_btn = Button(control1, text='Add state', command=add_state)
add_state_btn.grid(row=0,column=0)
state_entry_label = Label(control1, text='Enter state number')
state_entry_label.grid(row=1,column=0)
state_entry = Entry(control1, width=3)
state_entry.grid(row=1,column=1)
set_final_btn = Button(control1, text='Set as final', command=set_final)
set_final_btn.grid(row=1,column=2)
set_nonfinal_btn = Button(control1, text='Set as non-final', command=set_nonfinal)
set_nonfinal_btn.grid(row=1,column=3)
del_state_btn = Button(control1, text='Delete state', command=del_state)
del_state_btn.grid(row=1,column=4)

control2 = Frame(control, bg='green')
control2.pack(fill='x')

t_prompt1 = Label(control2, text='Source state number')
t_prompt1.grid(row=0,column=0)
t_prompt2 = Label(control2, text='Target state number')
t_prompt2.grid(row=0,column=1)
t_prompt3 = Label(control2, text='Config.')
t_prompt3.grid(row=0,column=2)
f_state_entry = Entry(control2, width=3)
f_state_entry.grid(row=1,column=0)
t_state_entry = Entry(control2, width=3)
t_state_entry.grid(row=1,column=1)
cnf_entry = Entry(control2, width=10)
cnf_entry.grid(row=1,column=2)
add_transition_btn = Button(control2, text='Add', command=add_transition)
add_transition_btn.grid(row=1,column=3)
del_transition_btn = Button(control2, text='Delete', command=del_transition)
del_transition_btn.grid(row=1,column=4)

control3 = Frame(display, bg='blue')
control3.grid_columnconfigure(1, weight=1)
control3.pack(side='bottom', fill='x')

test_str_prompt = Label(control3, text='Enter test string')
test_str_prompt.grid(row=0,column=0)
test_str_entry = Entry(control3, width=50)
test_str_entry.grid(stick='we',row=0,column=1)
as_function_var = BooleanVar(control3)
as_func_btn = Checkbutton(control3, text='as function', variable=as_function_var)
as_func_btn.grid(row=0,column=2)
seq_btn = Checkbutton(control3, text='sequential test')
seq_btn.grid(row=0,column=3)
test_btn = Button(control3, text='Run test', command=run_test)
test_btn.grid(row=0,column=4)
tape_result_lbl = Label(control3, text='Tape result')
tape_result_lbl.grid(row=1,column=0)
tape_result = Label(control3, width=50)
tape_result.grid(sticky='we',row=1,column=1)
result = Label(control3, width=10, bg='white', fg='white')
result.grid(row=1,column=2)
next_btn = Button(control3, text='Next', command=next)
next_btn.grid(row=1,column=3)
next_btn.grid_remove()

control.add(control1, text='States')
control.add(control2, text='Transitions')
control.add(control3, text='Testing')
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