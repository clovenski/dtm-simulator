#!/usr/bin/env python3

# Classes to organize sections of the GUI

from tkinter import Frame, Button, Label, Entry, Checkbutton, StringVar, BooleanVar, Canvas, Scrollbar
from utils import TestingState

class StatesPanel(Frame):
    def __init__(self, master, machine, info_manager, display_manager):
        super().__init__(master=master)
        self.pack(fill='x')
        self.machine = machine
        self.info_manager = info_manager
        self.display_manager = display_manager
        self._add_state_btn = Button(self, text='Add state', command=self._add_state)
        self._add_state_btn.grid(row=0,column=0)
        self._state_entry_label = Label(self, text='Enter state number')
        self._state_entry_label.grid(row=1,column=0)
        self._state_entry = Entry(self, width=3)
        self._state_entry.grid(row=1,column=1)
        self._set_final_btn = Button(self, text='Set as final', command=self._set_final)
        self._set_final_btn.grid(row=1,column=2)
        self._set_nonfinal_btn = Button(self, text='Set as non-final', command=self._set_nonfinal)
        self._set_nonfinal_btn.grid(row=1,column=3)
        self._del_state_btn = Button(self, text='Delete state', command=self._del_state)
        self._del_state_btn.grid(row=1,column=4)

    def _add_state(self):
        self.machine.add_state()
        self.info_manager.update_info()
        added_init_state = self.machine.init_state == self.machine.max_state_num
        self.display_manager.add_state(self.machine.max_state_num, added_init_state)

    def _del_state(self):
        try:
            target_state = int(self._state_entry.get())
            self.machine.del_state(target_state)
        except:
            # can update error message var here
            pass
        self._state_entry.delete(0, 'end')
        self.info_manager.update_info()
        self.display_manager.del_state(target_state)

    def _set_final(self):
        try:
            target_state = int(self._state_entry.get())
            self.machine.set_final_state(target_state)
        except:
            # can update error message var here
            pass
        self._state_entry.delete(0, 'end')
        self.info_manager.update_info()
        self.display_manager.set_final(target_state)

    def _set_nonfinal(self):
        try:
            target_state = int(self._state_entry.get())
            self.machine.set_nonfinal_state(target_state)
        except:
            # can update error message var here
            pass
        self._state_entry.delete(0, 'end')
        self.info_manager.update_info()
        self.display_manager.set_nonfinal(target_state)

class TransitionsPanel(Frame):
    def __init__(self, master, machine, info_manager, display_manager):
        super().__init__(master=master)
        self.pack(fill='x')
        self.machine = machine
        self.info_manager = info_manager
        self.display_manager = display_manager
        self._t_prompt1 = Label(self, text='Source state number')
        self._t_prompt1.grid(row=0,column=0)
        self._t_prompt2 = Label(self, text='Target state number')
        self._t_prompt2.grid(row=0,column=1)
        self._t_prompt3 = Label(self, text='Config.')
        self._t_prompt3.grid(row=0,column=2)
        self._f_state_entry = Entry(self, width=3)
        self._f_state_entry.grid(row=1,column=0)
        self._t_state_entry = Entry(self, width=3)
        self._t_state_entry.grid(row=1,column=1)
        self._cnf_entry = Entry(self, width=10)
        self._cnf_entry.grid(row=1,column=2)
        self._add_transition_btn = Button(self, text='Add', command=self._add_transition)
        self._add_transition_btn.grid(row=1,column=3)
        self._del_transition_btn = Button(self, text='Delete', command=self._del_transition)
        self._del_transition_btn.grid(row=1,column=4)
    
    def _add_transition(self):
        try:
            f_state = int(self._f_state_entry.get())
            t_state = int(self._t_state_entry.get())
            cnf = self._cnf_entry.get()
            self.machine.add_transition(f_state, t_state, cnf)
        except:
            # can update error message var here
            pass
        self._f_state_entry.delete(0, 'end')
        self._t_state_entry.delete(0, 'end')
        self._cnf_entry.delete(0, 'end')
        self.info_manager.update_info()
        self.display_manager.add_transition(f_state, t_state, cnf)

    def _del_transition(self):
        try:
            f_state = int(self._f_state_entry.get())
            t_state = int(self._t_state_entry.get())
            cnf = self._cnf_entry.get()
            self.machine.del_transition(f_state, t_state, cnf)
        except:
            # can update error message var here
            pass
        self._f_state_entry.delete(0, 'end')
        self._t_state_entry.delete(0, 'end')
        self._cnf_entry.delete(0, 'end')
        self.info_manager.update_info()
        self.display_manager.del_transition(f_state, t_state, cnf)

class TestingPanel(Frame):
    def __init__(self, master, machine):
        super().__init__(master=master)
        self.grid_columnconfigure(1, weight=1)
        self.pack(fill='x')
        self.machine = machine
        self._testing_state = None
        self._test_str_prompt = Label(self, text='Enter test string')
        self._test_str_prompt.grid(row=0,column=0)
        self._test_str_entry = Entry(self, width=50)
        self._test_str_entry.grid(stick='we',row=0,column=1)
        self._as_function_var = BooleanVar(self)
        self._as_func_btn = Checkbutton(self, text='as function', variable=self._as_function_var)
        self._as_func_btn.grid(row=0,column=2)
        self._seq_var = BooleanVar(self)
        self._seq_btn = Checkbutton(self, text='sequential test', variable=self._seq_var)
        self._seq_btn.grid(row=0,column=3)
        self._test_btn = Button(self, text='Run test', command=self._run_test)
        self._test_btn.grid(row=0,column=4)
        self._tape_result_lbl = Label(self, text='Tape result')
        self._tape_result_lbl.grid(row=1,column=0)
        self._tape_result = Label(self, width=50, bg='white')
        self._tape_result.grid(sticky='we',row=1,column=1)
        self._result = Label(self, width=10, fg='white')
        self._btn_og_color = self._result.cget('bg')
        self._result.grid(row=1,column=2)
        self._next_btn = Button(self, text='Next', command=self._next)
        self._next_btn.grid(row=1,column=3)
        self._next_btn.grid_remove()
        self._stop_btn = Button(self, text='Stop', command=self._stop)
        self._stop_btn.grid(row=1,column=4)
        self._stop_btn.grid_remove()

    def _run_test(self):
        self._result.config(text='', bg=self._btn_og_color)
        if self.machine.is_empty():
            raise Exception('empty machine')
        sequential = self._seq_var.get()
        as_function = self._as_function_var.get()
        if not sequential:
            results = self.machine.compute(self._test_str_entry.get(), as_function=as_function)
            if not as_function:
                self._tape_result.config(text=results[1])
                if results[0]:
                    self._result.config(text='Accepted', bg='green')
                else:
                    self._result.config(text='Rejected', bg='red')
            else:
                self._tape_result.config(text=results)
        else: # sequential test
            self._testing_state = TestingState(self._test_str_entry.get(), as_function, self.machine.init_state)
            self._tape_result.config(text=self._testing_state.tape if len(self._testing_state.tape) != 0 else '#')
            self._test_btn.config(state='disabled')
            self._next_btn.grid()
            self._stop_btn.grid()

    def _next(self):
        self.machine.compute_one(self._testing_state)
        self._tape_result.config(text=self._testing_state.tape)
        if self._testing_state.done:
            if not self._testing_state.as_function:
                if self._testing_state.result:
                    self._result.config(text='Accepted', bg='green')
                else:
                    self._result.config(text='Rejected', bg='red')
            self._next_btn.grid_remove()
            self._stop_btn.grid_remove()
            self._test_btn.config(state='normal')
            self._testing_state = None

    def _stop(self):
        self._testing_state = None
        self._tape_result.config(text='')
        self._next_btn.grid_remove()
        self._stop_btn.grid_remove()
        self._test_btn.config(state='normal')

class InfoManager(Frame):
    def __init__(self, master, machine):
        super().__init__(master=master)
        self.pack(side='right', fill='y')
        self.machine = machine
        self._info_var = StringVar(self)
        self._machine_info = Label(self, textvariable=self._info_var)
        self._machine_info.pack(fill='x')
        self._sn_var = StringVar(self)
        self._state_num_info = Label(self, textvariable=self._sn_var)
        self._state_num_info.pack(fill='x')
        self.update_info()

    def update_info(self):
        info = ''
        for desc, value in self.machine.get_info().items():
            info += '{}: {}'.format(desc, value) + '\n'
        self._info_var.set(info)

    def show_state_num(self, _, state_num):
        self._sn_var.set(str(state_num))

    def hide_state_num(self, _):
        self._sn_var.set('')

class Display(Canvas):
    def __init__(self, master, machine):
        super().__init__(master=master, bg='light gray')
        self.machine = machine
        self.info_manager = InfoManager(self, machine)
        self.pack(fill='both', expand=True)
        self._xsb = Scrollbar(self, orient='horizontal', command=self.xview)
        self._ysb = Scrollbar(self, orient='vertical', command=self.yview)
        self.config(xscrollcommand=self._xsb.set, yscrollcommand=self._ysb.set, scrollregion=(0,0,1000,1000))
        self._xsb.pack(side='bottom', fill='x')
        self._ysb.pack(side='right', fill='y')
        self.bind('<ButtonPress-1>', self._pan_start)
        self.bind('<B1-Motion>', self._pan_exec)
        self._moving_obj = False

    def _pan_start(self, event):
        if not self._moving_obj:
            self.scan_mark(event.x, event.y)

    def _pan_exec(self, event):
        if not self._moving_obj:
            self.scan_dragto(event.x, event.y, gain=1)
    
    def _drag(self, event, id):
        self._moving_obj = True
        coords = (
            self.canvasx(event.x)-12,
            self.canvasy(event.y)-12,
            self.canvasx(event.x)+13,
            self.canvasy(event.y)+13)
        self.coords(id, *coords)

    def _drop(self, event):
        self._moving_obj = False

    def add_state(self, state_num, as_init):
        state_id = self.create_oval(75,75,100,100, fill='linen')
        self.tag_bind(state_id, '<B1-Motion>', lambda e: self._drag(e,state_id))
        self.tag_bind(state_id, '<ButtonRelease-1>', self._drop)
        self.tag_bind(state_id, '<Enter>', lambda e: self.info_manager.show_state_num(e,state_num))
        self.tag_bind(state_id, '<Leave>', self.info_manager.hide_state_num)
        if as_init:
            pass # draw init arrow to show as init state

    def del_state(self, state_num):
        pass

    def set_final(self, state_num):
        pass

    def set_nonfinal(self, state_num):
        pass

    def add_transition(self, from_state, to_state, cnf):
        pass

    def del_transition(self, from_state, to_state, cnf):
        pass
