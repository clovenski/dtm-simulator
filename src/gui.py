#!/usr/bin/env python3

# Main script for the GUI version of DTM Simulator
# Currently a work in progress

from tkinter import *

root = Tk()
root.title('DTM Simulator')
window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()
x_offset = int(root.winfo_screenwidth()/3 - window_width/3)
y_offset = int(root.winfo_screenheight()/3 - window_height/3)
root.geometry('500x500+{}+{}'.format(x_offset, y_offset))

display = Frame(root, bg='gray')
control = Frame(display)

def del_state():
    global var
    target_state = var.get()
    print(target_state)

add_state_btn = Button(control, text='Add state')
add_state_btn.grid(row=0,column=1)
var = StringVar(control)
var.set('State #')
del_state_entry = OptionMenu(control, var, *range(1,7))
del_state_entry.grid(row=1,column=0)
del_state_btn = Button(control, text='Delete state', command=del_state)
del_state_btn.grid(row=1,column=1)

control.pack(side='bottom', fill='x')
info = Frame(display, width=250, bg='red')
info.pack(side='right', fill='y')
display.pack(fill='both', expand=True)

root.minsize(250,250)
root.mainloop()