#!/usr/bin/env python3

# Classes to organize sections of the GUI

from tkinter import Frame, Button, Label, Entry, Checkbutton, StringVar, BooleanVar
from utils import TestingState

class StatesPanel(Frame):
    def __init__(self, master, machine, info_manager):
        super().__init__(master=master)
        self.pack(fill='x')
        self.machine = machine
        self.info_manager = info_manager
        self.add_state_btn = Button(self, text='Add state', command=self.add_state)
        self.add_state_btn.grid(row=0,column=0)
        self.state_entry_label = Label(self, text='Enter state number')
        self.state_entry_label.grid(row=1,column=0)
        self.state_entry = Entry(self, width=3)
        self.state_entry.grid(row=1,column=1)
        self.set_final_btn = Button(self, text='Set as final', command=self.set_final)
        self.set_final_btn.grid(row=1,column=2)
        self.set_nonfinal_btn = Button(self, text='Set as non-final', command=self.set_nonfinal)
        self.set_nonfinal_btn.grid(row=1,column=3)
        self.del_state_btn = Button(self, text='Delete state', command=self.del_state)
        self.del_state_btn.grid(row=1,column=4)

    def add_state(self):
        self.machine.add_state()
        self.info_manager.update_info()

    def set_final(self):
        try:
            target_state = int(self.state_entry.get())
            self.machine.set_final_state(target_state)
        except:
            # can update error message var here
            pass
        self.state_entry.delete(0, 'end')
        self.info_manager.update_info()

    def set_nonfinal(self):
        try:
            target_state = int(self.state_entry.get())
            self.machine.set_nonfinal_state(target_state)
        except:
            # can update error message var here
            pass
        self.state_entry.delete(0, 'end')
        self.info_manager.update_info()

    def del_state(self):
        try:
            target_state = int(self.state_entry.get())
            self.machine.del_state(target_state)
        except:
            # can update error message var here
            pass
        self.state_entry.delete(0, 'end')
        self.info_manager.update_info()

class TransitionsPanel(Frame):
    def __init__(self, master, machine, info_manager):
        super().__init__(master=master)
        self.pack(fill='x')
        self.machine = machine
        self.info_manager = info_manager
        self.t_prompt1 = Label(self, text='Source state number')
        self.t_prompt1.grid(row=0,column=0)
        self.t_prompt2 = Label(self, text='Target state number')
        self.t_prompt2.grid(row=0,column=1)
        self.t_prompt3 = Label(self, text='Config.')
        self.t_prompt3.grid(row=0,column=2)
        self.f_state_entry = Entry(self, width=3)
        self.f_state_entry.grid(row=1,column=0)
        self.t_state_entry = Entry(self, width=3)
        self.t_state_entry.grid(row=1,column=1)
        self.cnf_entry = Entry(self, width=10)
        self.cnf_entry.grid(row=1,column=2)
        self.add_transition_btn = Button(self, text='Add', command=self.add_transition)
        self.add_transition_btn.grid(row=1,column=3)
        self.del_transition_btn = Button(self, text='Delete', command=self.del_transition)
        self.del_transition_btn.grid(row=1,column=4)
    
    def add_transition(self):
        try:
            f_state = int(self.f_state_entry.get())
            t_state = int(self.t_state_entry.get())
            cnf = self.cnf_entry.get()
            self.machine.add_transition(f_state, t_state, cnf)
        except:
            # can update error message var here
            pass
        self.f_state_entry.delete(0, 'end')
        self.t_state_entry.delete(0, 'end')
        self.cnf_entry.delete(0, 'end')
        self.info_manager.update_info()

    def del_transition(self):
        try:
            f_state = int(self.f_state_entry.get())
            t_state = int(self.t_state_entry.get())
            cnf = self.cnf_entry.get()
            self.machine.del_transition(f_state, t_state, cnf)
        except:
            # can update error message var here
            pass
        self.f_state_entry.delete(0, 'end')
        self.t_state_entry.delete(0, 'end')
        self.cnf_entry.delete(0, 'end')
        self.info_manager.update_info()

class TestingPanel(Frame):
    def __init__(self, master, machine):
        super().__init__(master=master)
        self.grid_columnconfigure(1, weight=1)
        self.pack(fill='x')
        self.machine = machine
        self.ts = None
        self.test_str_prompt = Label(self, text='Enter test string')
        self.test_str_prompt.grid(row=0,column=0)
        self.test_str_entry = Entry(self, width=50)
        self.test_str_entry.grid(stick='we',row=0,column=1)
        self.as_function_var = BooleanVar(self)
        self.as_func_btn = Checkbutton(self, text='as function', variable=self.as_function_var)
        self.as_func_btn.grid(row=0,column=2)
        self.seq_var = BooleanVar(self)
        self.seq_btn = Checkbutton(self, text='sequential test', variable=self.seq_var)
        self.seq_btn.grid(row=0,column=3)
        self.test_btn = Button(self, text='Run test', command=self.run_test)
        self.test_btn.grid(row=0,column=4)
        self.tape_result_lbl = Label(self, text='Tape result')
        self.tape_result_lbl.grid(row=1,column=0)
        self.tape_result = Label(self, width=50, bg='white')
        self.tape_result.grid(sticky='we',row=1,column=1)
        self.result = Label(self, width=10, fg='white')
        self.btn_og_color = self.result.cget('bg')
        self.result.grid(row=1,column=2)
        self.next_btn = Button(self, text='Next', command=self.next)
        self.next_btn.grid(row=1,column=3)
        self.next_btn.grid_remove()
        self.stop_btn = Button(self, text='Stop', command=self.stop)
        self.stop_btn.grid(row=1,column=4)
        self.stop_btn.grid_remove()

    def run_test(self):
        self.result.config(text='', bg=self.btn_og_color)
        if machine.is_empty():
            raise Exception('empty machine')
        sequential = self.seq_var.get()
        as_function = self.as_function_var.get()
        if not sequential:
            results = self.machine.compute(self.test_str_entry.get(), as_function=as_function)
            if not as_function:
                self.tape_result.config(text=results[1])
                if results[0]:
                    self.result.config(text='Accepted', bg='green')
                else:
                    self.result.config(text='Rejected', bg='red')
            else:
                self.tape_result.config(text=results)
        else: # sequential test
            self.ts = TestingState(self.test_str_entry.get(), as_function, self.machine.init_state)
            self.tape_result.config(text=self.ts.tape if len(self.ts.tape) != 0 else '#')
            self.test_btn.config(state='disabled')
            self.next_btn.grid()
            self.stop_btn.grid()

    def next(self):
        self.machine.compute_one(self.ts)
        self.tape_result.config(text=self.ts.tape)
        if self.ts.done:
            if not self.ts.as_function:
                if self.ts.result:
                    self.result.config(text='Accepted', bg='green')
                else:
                    self.result.config(text='Rejected', bg='red')
            self.next_btn.grid_remove()
            self.stop_btn.grid_remove()
            self.test_btn.config(state='normal')
            self.ts = None

    def stop(self):
        self.ts = None
        self.tape_result.config(text='')
        self.next_btn.grid_remove()
        self.stop_btn.grid_remove()
        self.test_btn.config(state='normal')

class InfoManager(Frame):
    def __init__(self, master, machine):
        super().__init__(master=master)
        self.pack(side='right', fill='y')
        self.machine = machine
        self.info_var = StringVar(self)
        self.machine_info = Label(self, textvariable=self.info_var)
        self.machine_info.pack()

    def update_info(self):
        info = ''
        for desc, value in self.machine.get_info().items():
            info += '{}: {}'.format(desc, value) + '\n'
        self.info_var.set(info)
