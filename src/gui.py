#!/usr/bin/env python3

# Main script for the GUI version of DTM Simulator
# Currently a work in progress

from tkinter import *

root = Tk()
root.title('DTM Simulator')
root.geometry('500x500+250+250')

frame = Frame(root, bg='gray')
control = Frame(frame, height=250)
control.pack(side='bottom', fill='x')
display = Frame(frame, width=250, bg='red')
display.pack(side='right', fill='y')
frame.pack(fill='both', expand=True)

root.minsize(250,250)
root.mainloop()