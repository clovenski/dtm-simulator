#!/usr/bin/env python3

# Classes to organize sections of the GUI

from tkinter import Frame, Button, Label, Entry, Checkbutton, StringVar, BooleanVar, Canvas, Scrollbar
from tkinter.ttk import LabelFrame
from utils import TestingState
from math import sqrt, atan, sin, cos
from random import randrange

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
        self._set_init_btn = Button(self, text='Set as initial', command=self._set_init)
        self._set_init_btn.grid(row=1,column=2)
        self._set_final_btn = Button(self, text='Set as final', command=self._set_final)
        self._set_final_btn.grid(row=1,column=3)
        self._set_nonfinal_btn = Button(self, text='Set as non-final', command=self._set_nonfinal)
        self._set_nonfinal_btn.grid(row=1,column=4)
        self._del_state_btn = Button(self, text='Delete state', command=self._del_state)
        self._del_state_btn.grid(row=1,column=5)

    def _add_state(self):
        self.machine.add_state()
        self.info_manager.update_info()
        added_init_state = self.machine.init_state == self.machine.max_state_num
        self.display_manager.add_state(self.machine.max_state_num, added_init_state)

    def _del_state(self):
        try:
            target_state = int(self._state_entry.get())
            self.machine.del_state(target_state)
            self.display_manager.del_state(target_state)
        except ValueError:
            self.info_manager.update_status('Enter state number')
        self._state_entry.delete(0, 'end')
        self.info_manager.update_info()

    def _set_init(self):
        try:
            target_state = int(self._state_entry.get())
            self.machine.set_init_state(target_state)
            self.display_manager.set_final(target_state)
        except ValueError:
            self.info_manager.update_status('Enter state number')
        self._state_entry.delete(0, 'end')
        self.info_manager.update_info()

    def _set_final(self):
        try:
            target_state = int(self._state_entry.get())
            self.machine.set_final_state(target_state)
            self.display_manager.set_final(target_state)
        except ValueError:
            self.info_manager.update_status('Enter state number')
        self._state_entry.delete(0, 'end')
        self.info_manager.update_info()

    def _set_nonfinal(self):
        try:
            target_state = int(self._state_entry.get())
            self.machine.set_nonfinal_state(target_state)
            self.display_manager.set_nonfinal(target_state)
        except ValueError:
            self.info_manager.update_status('Enter state number')
        self._state_entry.delete(0, 'end')
        self.info_manager.update_info()

class TransitionsPanel(Frame):
    def __init__(self, master, machine, info_manager, display_manager):
        super().__init__(master=master)
        self.pack(fill='x')
        self.machine = machine
        self.info_manager = info_manager
        self.display_manager = display_manager
        # states prompts
        self._t_prompt1 = Label(self, text='Source state number')
        self._t_prompt1.grid(row=0,column=0)
        self._t_prompt2 = Label(self, text='Target state number')
        self._t_prompt2.grid(row=0,column=1)
        # configuration prompts
        self._cnf_prompt1 = Label(self, text='R')
        self._cnf_prompt1.grid(row=0,column=2)
        self._cnf_prompt2 = Label(self, text='W')
        self._cnf_prompt2.grid(row=0,column=3)
        self._cnf_prompt3 = Label(self, text='M')
        self._cnf_prompt3.grid(row=0,column=4)
        # state entries
        self._f_state_entry = Entry(self, width=3)
        self._f_state_entry.grid(row=1,column=0)
        self._t_state_entry = Entry(self, width=3)
        self._t_state_entry.grid(row=1,column=1)
        # configuration entries
        self._cnf_var1 = StringVar()
        self._cnf_var1.trace('w', lambda *args: self._restrict_entry(self._cnf_var1,*args))
        self._cnf_var2 = StringVar()
        self._cnf_var2.trace('w', lambda *args: self._restrict_entry(self._cnf_var2,*args))
        self._cnf_var3 = StringVar()
        self._cnf_var3.trace('w', lambda *args: self._restrict_entry(self._cnf_var3,*args))
        self._cnf_read_entry = Entry(self, width=2, textvariable=self._cnf_var1)
        self._cnf_read_entry.grid(row=1,column=2)
        self._cnf_write_entry = Entry(self, width=2, textvariable=self._cnf_var2)
        self._cnf_write_entry.grid(row=1,column=3)
        self._cnf_move_entry = Entry(self, width=2, textvariable=self._cnf_var3)
        self._cnf_move_entry.grid(row=1,column=4)
        # buttons
        self._add_transition_btn = Button(self, text='Add', command=self._add_transition)
        self._add_transition_btn.grid(row=1,column=5)
        self._del_transition_btn = Button(self, text='Delete', command=self._del_transition)
        self._del_transition_btn.grid(row=1,column=6)
    
    def _restrict_entry(self, entry, *args):
        val = entry.get()
        if len(val) > 1: entry.set(val[0])

    def _add_transition(self):
        try:
            f_state = self._f_state_entry.get()
            if f_state == '':
                raise Exception('Enter source')
            else:
                f_state = int(f_state)
            t_state = self._t_state_entry.get()
            if t_state != '':
                t_state = int(t_state)
            else:
                raise Exception('Enter target')
            cnf = '({},{},{})'.format(
                self._cnf_read_entry.get(),self._cnf_write_entry.get(),self._cnf_move_entry.get())
            self.machine.add_transition(f_state, t_state, cnf)
            self.display_manager.add_transition(f_state, t_state, cnf)
            self.info_manager.update_status('Added transition')
            self.info_manager.show_transitions(f_state, t_state)
        except ValueError:
            self.info_manager.update_status('Invalid input')
        except Exception as e:
            self.info_manager.update_status(str(e))
        self._f_state_entry.delete(0, 'end')
        self._t_state_entry.delete(0, 'end')
        self._cnf_read_entry.delete(0, 'end')
        self._cnf_write_entry.delete(0, 'end')
        self._cnf_move_entry.delete(0, 'end')
        self.info_manager.update_info()

    def _del_transition(self):
        try:
            f_state = self._f_state_entry.get()
            if f_state == '':
                raise Exception('Enter source')
            else:
                f_state = int(f_state)
            t_state = self._t_state_entry.get()
            if t_state != '':
                t_state = int(t_state)
            else:
                raise Exception('Enter target')
            cnf = '({},{},{})'.format(
                self._cnf_read_entry.get(),self._cnf_write_entry.get(),self._cnf_move_entry.get())
            deleted = self.machine.del_transition(f_state, t_state, cnf)
            self.display_manager.del_transition(f_state, t_state, cnf)
            result = 'Deleted transition' if deleted else 'Transition not found'
            self.info_manager.update_status(result)
            if deleted: self.info_manager.show_transitions(f_state, t_state)
        except ValueError:
            self.info_manager.update_status('Invalid input')
        except Exception as e:
            self.info_manager.update_status(str(e))
        self._f_state_entry.delete(0, 'end')
        self._t_state_entry.delete(0, 'end')
        self._cnf_read_entry.delete(0, 'end')
        self._cnf_write_entry.delete(0, 'end')
        self._cnf_move_entry.delete(0, 'end')
        self.info_manager.update_info()

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
        self._info_frame = LabelFrame(self, text='Main Info', labelanchor='n')
        self._info_frame.pack()
        # number of states
        self._info_label1 = Label(self._info_frame, text='# of states')
        self._info_label1.grid(row=0,column=0)
        self._info_var1 = StringVar(self._info_frame)
        self._machine_info1 = Label(self._info_frame, textvariable=self._info_var1, width=3)
        self._machine_info1.grid(row=0,column=1)
        # init state
        self._info_label2 = Label(self._info_frame, text='Initial state')
        self._info_label2.grid(row=1,column=0)
        self._info_var2 = StringVar(self._info_frame)
        self._machine_info2 = Label(self._info_frame, textvariable=self._info_var2, width=3)
        self._machine_info2.grid(row=1,column=1)
        # nonfinal states
        self._info_label3 = Label(self._info_frame, text='# of non-final states')
        self._info_label3.grid(row=2,column=0)
        self._info_var3 = StringVar(self._info_frame)
        self._machine_info3 = Label(self._info_frame, textvariable=self._info_var3, width=3)
        self._machine_info3.grid(row=2,column=1)
        # final states
        self._info_label4 = Label(self._info_frame, text='# of final states')
        self._info_label4.grid(row=3,column=0)
        self._info_var4 = StringVar(self._info_frame)
        self._machine_info4 = Label(self._info_frame, textvariable=self._info_var4, width=3)
        self._machine_info4.grid(row=3,column=1)
        # number of transitions
        self._info_label5 = Label(self._info_frame, text='# of transitions')
        self._info_label5.grid(row=4,column=0)
        self._info_var5 = StringVar(self._info_frame)
        self._machine_info5 = Label(self._info_frame, textvariable=self._info_var5, width=3)
        self._machine_info5.grid(row=4,column=1)
        # transitions info
        self._trans_frame = LabelFrame(self, text='Transitions Info', labelanchor='n')
        self._trans_frame.pack(fill='both', expand=True)
        self._trans_info1 = Label(self._trans_frame, anchor='n')
        self._trans_info1.pack(side='top')
        self._trans_info2 = Label(self._trans_frame, anchor='n')
        self._trans_info2.pack(side='top')
        # status bar
        self._status_bar = Label(self)
        self._status_bar.pack()
        self.update_info()

    def update_info(self):
        info = self.machine.get_info()
        self._info_var1.set(info['# of states'])
        self._info_var2.set(info['Initial state'])
        self._info_var3.set(info['# of non-final states'])
        self._info_var4.set(info['# of final states'])
        self._info_var5.set(info['# of transitions'])

    def update_status(self, text):
        self._status_bar.config(text=text)

    def clear_status(self):
        self._status_bar.config(text='')

    def show_transitions(self, from_state, to_state):
        info1 = '{} -> {}\n'.format(from_state, to_state)
        info1 += '\n'.join(self.machine.get_transitions(from_state,to_state))
        info2 = None
        try:
            if from_state != to_state and from_state in self.machine.transitions[to_state]:
                info2 = '{} -> {}\n'.format(to_state,from_state)
                info2 += '\n'.join(self.machine.get_transitions(to_state,from_state))
        except KeyError: pass
        self._trans_info1.config(text=info1)
        if info2 is not None:
            self._trans_info2.config(text=info2)

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
        self._tags_map = {} # maps tags to set of line_ids
        self._id_map = {} # maps state_num to state_id
        self._mini_lines = set([]) # set of line_ids of lines between two states close to each other
        self._lines_map = {} # maps state pairs to line_id for that pair
        self._loops = set([]) # set of all loop transitions

    def _pan_start(self, event):
        if not self._moving_obj:
            self.scan_mark(event.x, event.y)

    def _pan_exec(self, event):
        if not self._moving_obj:
            self.scan_dragto(event.x, event.y, gain=1)
    
    def _get_line_dist(self, *coords):
        return sqrt((coords[2]-coords[0])**2 + (coords[3]-coords[1])**2)

    def _get_raw_linecoords(self, *coords):
        head = (coords[2], coords[3])
        tail = (coords[0], coords[1])
        y = head[1] - tail[1]
        y_sgn = -1 if y < 0 else 1
        x = head[0] - tail[0]
        x_sgn = -1 if x < 0 else 1
        try:
            theta = atan(abs(y)/abs(x))
            x_offset = x_sgn * 13 * cos(theta)
            y_offset = y_sgn * 13 * sin(theta)
        except ZeroDivisionError:
            x_offset = 0
            y_offset = y_sgn * 13
        return (tail[0]-x_offset, tail[1]-y_offset, head[0]+x_offset, head[1]+y_offset)

    def _get_mod_linecoords(self, *coords):
        head = (coords[2], coords[3])
        tail = (coords[0], coords[1])
        dist = sqrt((head[0]-tail[0])**2 + (head[1]-tail[1])**2)
        if dist <= 35: return coords
        ratio = 13 / dist
        x_offset = ratio * (head[0] - tail[0])
        y_offset = ratio * (head[1] - tail[1])
        return (tail[0]+x_offset, tail[1]+y_offset, head[0]-x_offset, head[1]-y_offset)

    def _drag_line_head(self, line_id, event):
        line_coords = self.coords(line_id)
        raw_linecoords = (line_coords[0],line_coords[1],self.canvasx(event.x),self.canvasy(event.y))
        if line_id not in self._mini_lines: # states are separated enough
            raw_linecoords = self._get_raw_linecoords(*line_coords)
            new_coords = (raw_linecoords[0],raw_linecoords[1],self.canvasx(event.x),self.canvasy(event.y))
            mod_linecoords = self._get_mod_linecoords(*new_coords)
            if mod_linecoords == new_coords: # line became small enough
                self._mini_lines.add(line_id)
        elif self._get_line_dist(*raw_linecoords) >= 35: # new line is large enough
            self._mini_lines.remove(line_id)
            mod_linecoords = self._get_mod_linecoords(*raw_linecoords)
        else: # keep drawing small line
            mod_linecoords = raw_linecoords
        self.coords(line_id, *mod_linecoords)

    def _drag_loop(self, line_id, event):
        event_coords = (self.canvasx(event.x), self.canvasy(event.y))
        coords = (
            event_coords[0]+-7,event_coords[1]-11,
            event_coords[0]-22,event_coords[1]-36,
            event_coords[0]+18,event_coords[1]-36,
            event_coords[0]+3,event_coords[1]-11)
        self.coords(line_id, *coords)

    def _drag_line_tail(self, line_id, event):
        if line_id in self._loops:
            return self._drag_loop(line_id, event)
        line_coords = self.coords(line_id)
        raw_linecoords = (self.canvasx(event.x),self.canvasy(event.y),line_coords[2],line_coords[3])
        if line_id not in self._mini_lines: # states are separated enough
            raw_linecoords = self._get_raw_linecoords(*line_coords)
            new_coords = (self.canvasx(event.x),self.canvasy(event.y),raw_linecoords[2],raw_linecoords[3])
            mod_linecoords = self._get_mod_linecoords(*new_coords)
            if mod_linecoords == new_coords: # line became small enough
                self._mini_lines.add(line_id)
        elif self._get_line_dist(*raw_linecoords) >= 35: # new line is large enough
            self._mini_lines.remove(line_id)
            mod_linecoords = self._get_mod_linecoords(*raw_linecoords)
        else: # keep drawing small line
            mod_linecoords = raw_linecoords
        self.coords(line_id, *mod_linecoords)

    def _drag(self, event, state_id):
        self._moving_obj = True
        coords = (
            self.canvasx(event.x)-12,
            self.canvasy(event.y)-12,
            self.canvasx(event.x)+13,
            self.canvasy(event.y)+13)
        self.coords(state_id, *coords)
        self.coords(str(state_id)+'t', coords[0]+12, coords[1]+12)
        try:
            for line_id in self._tags_map['-'+str(state_id)]:
                self._drag_line_head(line_id, event)
        except KeyError: pass
        try:
            for line_id in self._tags_map[str(state_id)+'-']:
                self._drag_line_tail(line_id, event)
        except KeyError: pass

    def _drop(self, event):
        self._moving_obj = False

    def _update_status(self, state_num):
        if not self._moving_obj:
            self.info_manager.update_status('State {}'.format(state_num))

    def _clear_status(self):
        if not self._moving_obj:
            self.info_manager.clear_status()

    def add_state(self, state_num, as_init):
        x,y = self.canvasx(75+randrange(150)),self.canvasy(75+randrange(200))
        coords = (x, y, x+25, y+25)
        state_id = self.create_oval(*coords, fill='linen')
        tag = str(state_id) + 't'
        self.create_text(coords[0]+13,coords[1]+13, text=str(state_num), tags=tag)
        self._id_map[state_num] = state_id
        self.tag_bind(state_id, '<B1-Motion>', lambda e: self._drag(e,state_id))
        self.tag_bind(state_id, '<ButtonRelease-1>', self._drop)
        self.tag_bind(state_id, '<Enter>', lambda e: self._update_status(state_num))
        self.tag_bind(state_id, '<Leave>', lambda e: self._clear_status())
        self.tag_bind(tag, '<B1-Motion>', lambda e: self._drag(e,state_id))
        self.tag_bind(tag, '<ButtonRelease-1>', self._drop)
        self.tag_bind(tag, '<Enter>', lambda e: self._update_status(state_num))
        self.info_manager.update_status('Added State {}'.format(state_num))
        if as_init:
            pass # draw init arrow to show as init state

    def del_state(self, state_num):
        pass

    def set_init(self, state_num):
        pass

    def set_final(self, state_num):
        pass

    def set_nonfinal(self, state_num):
        pass

    def _add_loop(self, state_num):
        state_coords = self.coords(self._id_map[state_num])
        coords = (
            state_coords[0]+6,state_coords[1]+2,
            state_coords[0]-9,state_coords[1]-23,
            state_coords[0]+31,state_coords[1]-23,
            state_coords[0]+16,state_coords[1]+2)
        tag = str(self._id_map[state_num]) + '-'
        line_id = self.create_line(*coords, smooth=True, arrow='last', tags=tag)
        self._lines_map['{}-{}'.format(state_num,state_num)] = line_id
        self.tag_bind(line_id, '<ButtonPress-1>', lambda e: self.info_manager.show_transitions(state_num,state_num))
        self._loops.add(line_id)
        try: self._tags_map[tag].add(line_id)
        except: self._tags_map[tag] = set([line_id])

    def add_transition(self, from_state, to_state, cnf):
        # may not need cnf
        if '{}-{}'.format(from_state,to_state) in self._lines_map:
            return
        elif '{}-{}'.format(to_state,from_state) in self._lines_map:
            line_id = self._lines_map['{}-{}'.format(to_state,from_state)]
            self.itemconfig(line_id, arrow='both')
            return
        if from_state == to_state:
            return self._add_loop(from_state)
        f_coords = self.coords(self._id_map[from_state])
        f_coords = (f_coords[0]+13, f_coords[1]+13)
        t_coords = self.coords(self._id_map[to_state])
        t_coords = (t_coords[0]+13, t_coords[1]+13)
        line_coords = self._get_mod_linecoords(f_coords[0], f_coords[1], t_coords[0], t_coords[1])
        tag1 = str(self._id_map[from_state]) + '-'
        tag2 = '-' + str(self._id_map[to_state])
        line_id = self.create_line(line_coords, arrow='last', tags=(tag1,tag2))
        self._lines_map['{}-{}'.format(from_state,to_state)] = line_id
        self.tag_bind(line_id, '<ButtonPress-1>', lambda e: self.info_manager.show_transitions(from_state,to_state))
        try: self._tags_map[tag1].add(line_id)
        except: self._tags_map[tag1] = set([line_id])
        try: self._tags_map[tag2].add(line_id)
        except: self._tags_map[tag2] = set([line_id])

    def del_transition(self, from_state, to_state, cnf):
        pass
