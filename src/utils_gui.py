"""
Classes to organize the sections of the GUI: display, info and control.

Display implements a canvas for the user to graphically view the machine,
info shows the main information of the machine along with the currently
selected transition's info and a status bar, and control implements
three panels to control the states and transitions of the machine, along
with a panel to test some strings with the machine.
"""

from tkinter import Frame, Button, Label, Entry, OptionMenu, Checkbutton, StringVar, BooleanVar, Canvas, Scrollbar
from tkinter.ttk import LabelFrame
from utils import TestingState
from math import sqrt, atan, sin, cos
from random import randrange
import threading

class StatesPanel(Frame):
    """This is a class to represent the section where the user can
    manipulate the states of the machine.

    Attributes:
        machine (utils.Machine): The machine of the user.
        info_manager (InfoManager): The object that handles the info
            section of the GUI.
        display_manager (Display): The object that handles the display
            to the user.
    """

    def __init__(self, master, machine, info_manager, display_manager):
        """Initialize the states panel with the user's machine and appropriate
        managers.

        The states panel provides the interface for actions pertaining to the
        states of the machine. This panel implements an entry for the user to
        specify which state number to work on, and buttons to add a state, delete
        a state, set a state as initial, final and non-final.

        Parameters:
            machine (utils.Machine): The machine of the user.
            info_manager (InfoManager): The object that handles the info
                section of the GUI.
            display_manager (Display): The object that handles the display
                to the user.
        """
        super().__init__(master=master)
        self.pack(fill='x')
        self.machine = machine
        self.info_manager = info_manager
        self.display_manager = display_manager
        # first row
        self._add_state_btn = Button(self, text='Add state', command=self._add_state)
        self._add_state_btn.grid(row=0,column=0,pady=4)
        # second row
        self._state_entry_label = Label(self, text='Enter state number')
        self._state_entry_label.grid(row=1,column=0)
        self._state_entry = Entry(self, width=3)
        self._state_entry.grid(row=1,column=1)
        self._set_init_btn = Button(self, text='Set as initial', command=self._set_init)
        self._set_init_btn.grid(row=1,column=2,padx=2)
        self._set_final_btn = Button(self, text='Set as final', command=self._set_final)
        self._set_final_btn.grid(row=1,column=3,padx=2)
        self._set_nonfinal_btn = Button(self, text='Set as non-final', command=self._set_nonfinal)
        self._set_nonfinal_btn.grid(row=1,column=4,padx=2)
        self._del_state_btn = Button(self, text='Delete state', command=self._del_state)
        self._del_state_btn.grid(row=1,column=5,padx=2)

    def _add_state(self):
        # add a state to the machine, calling functions in the display and info
        # managers to update the GUI
        self.machine.add_state()
        self.info_manager.update_info()
        added_init_state = self.machine.init_state == self.machine.max_state_num
        self.display_manager.add_state(self.machine.max_state_num, as_init=added_init_state)

    def _del_state(self):
        # delete a state from the machine according to the user's entry
        # in the GUI, clearing the entry and updating the status bar appropriately
        try:
            target_state = int(self._state_entry.get())
            init_deleted = target_state == self.machine.init_state
            deleted = self.machine.del_state(target_state)
            if deleted: self.display_manager.del_state(target_state, init_deleted)
        except ValueError:
            self.info_manager.update_status('Enter state number')
        self._state_entry.delete(0, 'end')
        self.info_manager.update_info()
        self.info_manager.hide_transitions()

    def _set_init(self):
        # set the specified state in the GUI's entry as initial,
        # clearing the entry and updating the status bar appropriately
        try:
            target_state = int(self._state_entry.get())
            self.machine.set_init_state(target_state)
            self.display_manager.set_init(target_state)
        except ValueError:
            self.info_manager.update_status('Enter state number')
        except Exception as e:
            self.info_manager.update_status(str(e))
        self._state_entry.delete(0, 'end')
        self.info_manager.update_info()

    def _set_final(self):
        # set the specified state in the GUI's entry as final,
        # clearing the entry and updating the status bar appropriately
        try:
            target_state = int(self._state_entry.get())
            self.machine.set_final_state(target_state)
            self.display_manager.set_final(target_state)
        except ValueError:
            self.info_manager.update_status('Enter state number')
        except Exception as e:
            self.info_manager.update_status(str(e))
        self._state_entry.delete(0, 'end')
        self.info_manager.update_info()

    def _set_nonfinal(self):
        # set the specified state in the GUI's entry as non-final,
        # clearing the entry and updating the status bar appropriately
        try:
            target_state = int(self._state_entry.get())
            self.machine.set_nonfinal_state(target_state)
            self.display_manager.set_nonfinal(target_state)
        except ValueError:
            self.info_manager.update_status('Enter state number')
        except Exception as e:
            self.info_manager.update_status(str(e))
        self._state_entry.delete(0, 'end')
        self.info_manager.update_info()

class TransitionsPanel(Frame):
    """This is a class to represent the section where the user
    can add and delete transitions in the machine.

    Attributes:
        machine (utils.Machine): The machine of the user.
        info_manager (InfoManager): The object that handles the info
            section of the GUI.
        display_manager (Display): The object that handles the display
            to the user.
    """

    def __init__(self, master, machine, info_manager, display_manager):
        """Initialize the transitions panel with the user's machine and
        appropriate managers

        The transitions panel provides the interface where the user can
        add and delete transitions in the machine.

        Parameters:
            machine (utils.Machine): The machine of the user.
            info_manager (InfoManager): The object that handles the info
                section of the GUI.
            display_manager (Display): The object that handles the display
                to the user.
        """
        super().__init__(master=master)
        self.pack(fill='x')
        self.machine = machine
        self.info_manager = info_manager
        self.display_manager = display_manager
        # states prompts
        self._t_prompt1 = Label(self, text='Source state')
        self._t_prompt1.grid(row=0,column=0,padx=5)
        self._t_prompt2 = Label(self, text='Target state')
        self._t_prompt2.grid(row=0,column=1,padx=5)
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
        # configuration entry restrictions
        self._cnf_var1 = StringVar()
        self._cnf_var1.trace('w', lambda *args: self._restrict_entry(self._cnf_var1,*args))
        self._cnf_var2 = StringVar()
        self._cnf_var2.trace('w', lambda *args: self._restrict_entry(self._cnf_var2,*args))
        # configuration entries
        self._cnf_read_entry = Entry(self, width=2, textvariable=self._cnf_var1)
        self._cnf_read_entry.grid(row=1,column=2)
        self._cnf_write_entry = Entry(self, width=2, textvariable=self._cnf_var2)
        self._cnf_write_entry.grid(row=1,column=3)
        self._cnf_move_var = StringVar(self)
        self._cnf_move_var.set('R')
        self._cnf_move_entry = OptionMenu(self, self._cnf_move_var, 'L', 'R')
        self._cnf_move_entry.grid(row=1,column=4)
        # buttons
        self._add_transition_btn = Button(self, text='Add', command=self._add_transition)
        self._add_transition_btn.grid(row=1,column=5,padx=2)
        self._del_transition_btn = Button(self, text='Delete', command=self._del_transition)
        self._del_transition_btn.grid(row=1,column=6,padx=2)
    
    def _restrict_entry(self, entry, *args):
        # restrict the given entry to one character in length only
        val = entry.get()
        if len(val) > 1: entry.set(val[0])

    def _add_transition(self):
        # add a transition to the machine according to the info
        # specified by the user, clear the entries and update the statuse bar
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
                self._cnf_read_entry.get(),self._cnf_write_entry.get(),self._cnf_move_var.get())
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
        self.info_manager.update_info()

    def _del_transition(self):
        # delete a transition from the machine according to the info
        # specified by the user, clear the entries and update the status bar
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
                self._cnf_read_entry.get(),self._cnf_write_entry.get(),self._cnf_move_var.get())
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
        self._cnf_move_var.set('R')
        self.info_manager.update_info()

class TestingPanel(Frame):
    """This is a class to represent the interface where the user can
    test strings with the machine.

    The user can test their given string with the machine for acceptance or
    rejection, or work on that string using the machine as a function to just
    output the results. In both cases the user can optionally choose to run
    the test sequentially; as in they can see the machine in-action with a
    button to advance it.

    Attributes:
        machine (utils.Machine): The machine of the user.
        info_manager (InfoManager): The object that handles the info
            section of the GUI.
        display_manager (Display): The object that handles the display
            to the user.
    """

    def __init__(self, master, machine, info_manager, display_manager):
        """Initialize this testing panel with the user's machine and
        the necessary managers.

        Parameters:
            machine (utils.Machine): The machine of the user.
            info_manager (InfoManager): The object that handles the info
                section of the GUI.
            display_manager (Display): The object that handles the display
                to the user.
        """
        super().__init__(master=master)
        self.grid_columnconfigure(1, weight=1)
        self.pack(fill='x')
        self.machine = machine
        self.info_manager = info_manager
        self.display_manager = display_manager
        # TestingState object to be used in sequential tests
        self._testing_state = None
        # prompt and entry for the test string
        self._test_str_prompt = Label(self, text='Enter test string')
        self._test_str_prompt.grid(row=0,column=0)
        self._test_str_entry = Entry(self, width=50)
        self._test_str_entry.grid(stick='we',row=0,column=1)
        # check boxes for "as function" and "sequential test"
        self._as_function_var = BooleanVar(self)
        self._as_func_btn = Checkbutton(self, text='as function', variable=self._as_function_var)
        self._as_func_btn.grid(row=0,column=2)
        self._seq_var = BooleanVar(self)
        self._seq_btn = Checkbutton(self, text='sequential test', variable=self._seq_var)
        self._seq_btn.grid(row=0,column=3,columnspan=2)
        # run test button
        self._test_btn = Button(self, text='Run test', command=self._run_test)
        self._test_btn.grid(row=0,column=5)
        # tape result label
        self._tape_result_lbl = Label(self, text='Tape result')
        self._tape_result_lbl.grid(row=1,column=0)
        self._tape_result = Label(self, width=50, bg='white')
        self._tape_result.grid(sticky='we',row=1,column=1,pady=6)
        # result label (acceptance/rejection)
        self._result = Label(self, width=10, fg='white')
        self._btn_og_color = self._result.cget('bg')
        self._result.grid(row=1,column=2)
        # buttons to be used during the tests
        self._next_btn = Button(self, text='Next', command=self._next)
        self._next_btn.grid(row=1,column=3)
        self._next_btn.grid_remove()
        self._stop_btn = Button(self, text='Stop', command=self._stop)
        self._stop_btn.grid(row=1,column=4)
        self._stop_btn.grid_remove()
        self._clear_btn = Button(self, text='Clear', command=self._clear)
        self._clear_btn.grid(row=1,column=5)
        self._clear_btn.grid_remove()
        # testing thread that is running the test,
        # meant to allow the user to exit infinite loop machines
        self._test_thread = None

    def _test_task(self, as_function):
        # task function to be executed by the testing thread;
        # execute the computation and update the appropriate labels
        self._stop_btn.grid()
        results = self.machine.compute(self._test_str_entry.get(), as_function=as_function)
        self._stop_btn.grid_remove()
        self._test_btn.config(state='normal')
        if not as_function:
            self._tape_result.config(text=results[1])
            if results[0]:
                self._result.config(text='Accepted', bg='green')
            else:
                self._result.config(text='Rejected', bg='red')
        else:
            self._tape_result.config(text=results)
        self._test_thread = None

    def _run_test(self):
        # run the test according to the data given by the user
        self._result.config(text='', bg=self._btn_og_color)
        if self.machine.is_empty():
            self.info_manager.update_status('Empty machine')
            return
        sequential = self._seq_var.get()
        as_function = self._as_function_var.get()
        self.info_manager.update_status('{} is blank symbol'.format(self.machine.blank))
        self._test_btn.config(state='disabled')
        self.display_manager.clear_highlight()
        self._clear_btn.grid_remove()
        if not sequential:
            self._tape_result.config(text='')
            self._test_thread = threading.Thread(target=self._test_task, args=(as_function,))
            self._test_thread.daemon = True
            self._test_thread.start()
        else: # sequential test
            self._testing_state = TestingState(self._test_str_entry.get(), as_function, self.machine.init_state)
            self._tape_result.config(
                text=self._testing_state.tape if len(self._testing_state.tape) != 0 else self.machine.blank,
                underline=0)
            self._next_btn.grid()
            self._stop_btn.grid()
            self.display_manager.clear_highlight()
            self.display_manager.highlight_state(self._testing_state.current_state)

    def _next(self):
        # advance the machine; "next" computation in the sequential test
        self.machine.compute_one(self._testing_state)
        self._tape_result.config(text=self._testing_state.tape, underline=self._testing_state.index)
        self.display_manager.highlight_state(self._testing_state.current_state)
        if self._testing_state.done:
            if not self._testing_state.as_function:
                if self._testing_state.result:
                    self._result.config(text='Accepted', bg='green')
                else:
                    self._result.config(text='Rejected', bg='red')
            self._next_btn.grid_remove()
            self._stop_btn.grid_remove()
            self._clear_btn.grid()
            self._test_btn.config(state='normal')
            self._testing_state = None

    def _stop(self):
        # stop the test; aborting the computation of the testing thread's machine
        if self._test_thread is not None: # non-sequential test
            self.machine.abort = True
            self._test_thread = None
            self._stop_btn.grid_remove()
            self._test_btn.config(state='normal')
            self.info_manager.update_status('Aborted test')
        else: # sequential test
            self._testing_state = None
            self._tape_result.config(text='', underline=-1)
            self._next_btn.grid_remove()
            self._stop_btn.grid_remove()
            self._test_btn.config(state='normal')
            self.display_manager.clear_highlight()
            self.info_manager.update_status('Stopped test')

    def _clear(self):
        # clear the highlighted state in the display, if any
        self.display_manager.clear_highlight()
        self._clear_btn.grid_remove()

class InfoManager(Frame):
    """This is a class to manage the information panel in the GUI.

    The information panel shows the main information of the machine, all the
    transitions in the selected transition, if any, and the status bar.

    Attributes:
        machine (utils.Machine): The machine of the user.
    """

    def __init__(self, master, machine):
        """Initialize this manager with the given machine and update the info
        that is shown to the user.

        Parameters:
            machine (utils.Machine): The machine of the user.
        """
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
        # update the info
        self.update_info()

    def update_info(self):
        """Update the info that is shown to the user."""
        info = self.machine.get_info()
        self._info_var1.set(info['# of states'])
        self._info_var2.set(info['Initial state'])
        self._info_var3.set(info['# of non-final states'])
        self._info_var4.set(info['# of final states'])
        self._info_var5.set(info['# of transitions'])

    def update_status(self, text):
        """Update the status bar with the given text

        Parameters:
            text (str): The text to be displayed in the status bar.
        """
        self._status_bar.config(text=text)

    def clear_status(self):
        """Clear the status bar."""
        self._status_bar.config(text='')

    def show_transitions(self, from_state, to_state):
        """Show the transitions pertaining to (from_state -> to_state).

        Parameters:
            from_state (int): The state number of the source of the transition.
            to_state (int): The state number of the target of the transition.
        """
        info1 = None
        info2 = None
        if self.machine.get_transition_count(from_state, to_state) > 0:
            info1 = '{} -> {}\n'.format(from_state, to_state)
            info1 += '\n'.join(self.machine.get_transitions(from_state,to_state))
        try:
            if from_state != to_state and from_state in self.machine.transitions[to_state]:
                info2 = '{} -> {}\n'.format(to_state,from_state)
                info2 += '\n'.join(self.machine.get_transitions(to_state,from_state))
        except KeyError: pass
        if info2 is not None and info1 is None:
            self._trans_info1.config(text=info2)
            self._trans_info2.config(text='')
        elif info2 is None and info1 is not None:
            self._trans_info1.config(text=info1)
            self._trans_info2.config(text='')
        elif info1 is None and info2 is None:
            self._trans_info1.config(text='')
            self._trans_info2.config(text='')
        else:
            if from_state > to_state:
                temp = info1
                info1 = info2
                info2 = temp
            self._trans_info1.config(text=info1)
            self._trans_info2.config(text=info2)

    def hide_transitions(self):
        """Clear the transition info shown to the user."""
        self._trans_info1.config(text='')
        self._trans_info2.config(text='')

class Display(Canvas):
    """This is a class that manages the display of the GUI.

    The display of the GUI implements a canvas where the user can visually
    see the states of the machine and the transitions between them. The user
    is able to freely move around the states for a better view and select
    transitions to view their information.

    Attributes:
        machine (utils.Machine): The machine of the user.
        info_manager (InfoManager): THe object that handles the info section
            of the GUI.
    """

    def __init__(self, master, machine):
        """Initialize this display with the user's machine.

        Parameters:
            machine (utils.Machine): The machine of the user.
        """
        super().__init__(master=master, bg='light gray')
        self.machine = machine
        self.info_manager = InfoManager(self, machine)
        self.pack(fill='both', expand=True)
        # scrollbars for the canvas
        self._xsb = Scrollbar(self, orient='horizontal', command=self.xview)
        self._ysb = Scrollbar(self, orient='vertical', command=self.yview)
        self.config(xscrollcommand=self._xsb.set, yscrollcommand=self._ysb.set, scrollregion=(0,0,1000,1000))
        self._xsb.pack(side='bottom', fill='x')
        self._ysb.pack(side='right', fill='y')
        # bindings to allow a pannable canvas
        self.bind('<ButtonPress-1>', self._pan_start)
        self.bind('<B1-Motion>', self._pan_exec)
        # boolean to indicate the user is moving a state instead of panning the canvas
        self._moving_obj = False
        # maps state_num to state_id
        self._id_map = {}
        # set of line_ids of lines between two states close to each other
        self._mini_lines = set([])
        # set of all loop transitions
        self._loops = set([])
        # id of init state
        self._init_id = None
        # config used by lines/transitions in the canvas
        self._lines_config = {
            'arrow': 'last',
            'width': 2,
            'activewidth': 4,
            'activefill': 'gray40'
        }
        # id of highlighted state, for sequential tests
        self._highlighted_state_id = None
        # default color of states
        self._default_state_fill = 'linen'
        # color of a highlighted state
        self._highlight_fill = 'gold'
        # lines less than threshold are mini lines, connecting states center to center
        self._line_thrshld = 35

    def _pan_start(self, event):
        # start the panning of the canvas if the user is not moving a state
        if not self._moving_obj:
            self.scan_mark(event.x, event.y)

    def _pan_exec(self, event):
        # execute the panning of the canvas is the user is not moving a state
        if not self._moving_obj:
            self.scan_dragto(event.x, event.y, gain=1)
    
    def _get_line_dist(self, x1, y1, x2, y2):
        # return the distance between two points
        return sqrt((x2-x1)**2 + (y2-y1)**2)

    def _get_raw_linecoords(self, *coords):
        # return the centers of the circles the coordinates pertain to;
        # lines drawn on the canvas do not overlap the circles/states, so
        # this function returns the coordinates as if they were center to center
        head = (coords[2], coords[3])
        tail = (coords[0], coords[1])
        y = head[1] - tail[1]
        y_sgn = -1 if y < 0 else 1
        x = head[0] - tail[0]
        x_sgn = -1 if x < 0 else 1
        try:
            theta = atan(abs(y)/abs(x))
            # circle radius = 13
            x_offset = x_sgn * 13 * cos(theta)
            y_offset = y_sgn * 13 * sin(theta)
        except ZeroDivisionError:
            x_offset = 0
            y_offset = y_sgn * 13
        return (tail[0]-x_offset, tail[1]-y_offset, head[0]+x_offset, head[1]+y_offset)

    def _get_mod_linecoords(self, *coords):
        # return the modified line coordinates to draw on the canvas,
        # pertaining to the two circles/states specified by the given coords
        head = (coords[2], coords[3])
        tail = (coords[0], coords[1])
        dist = sqrt((head[0]-tail[0])**2 + (head[1]-tail[1])**2)
        if dist <= self._line_thrshld: return coords
        ratio = 13 / dist
        x_offset = ratio * (head[0] - tail[0])
        y_offset = ratio * (head[1] - tail[1])
        return (tail[0]+x_offset, tail[1]+y_offset, head[0]-x_offset, head[1]-y_offset)

    def _drag_line_head(self, line_id, event):
        # drag the head of the line specified by the line_id
        # to the coordinates of the event
        line_coords = self.coords(line_id)
        raw_linecoords = (line_coords[0],line_coords[1],self.canvasx(event.x),self.canvasy(event.y))
        if line_id not in self._mini_lines: # states are separated enough
            raw_linecoords = self._get_raw_linecoords(*line_coords)
            new_coords = (raw_linecoords[0],raw_linecoords[1],self.canvasx(event.x),self.canvasy(event.y))
            mod_linecoords = self._get_mod_linecoords(*new_coords)
            if mod_linecoords == new_coords: # line became small enough
                self._mini_lines.add(line_id)
        elif self._get_line_dist(*raw_linecoords) >= self._line_thrshld: # new line is large enough
            self._mini_lines.remove(line_id)
            mod_linecoords = self._get_mod_linecoords(*raw_linecoords)
        else: # keep drawing small line
            mod_linecoords = raw_linecoords
        self.coords(line_id, *mod_linecoords)

    def _drag_loop(self, line_id, event):
        # drag a loop specified by the line_id to the coordinates of the event
        event_coords = (self.canvasx(event.x), self.canvasy(event.y))
        coords = (
            event_coords[0]-7,event_coords[1]-11,
            event_coords[0]-22,event_coords[1]-36,
            event_coords[0]+18,event_coords[1]-36,
            event_coords[0]+3,event_coords[1]-11)
        self.coords(line_id, *coords)

    def _drag_line_tail(self, line_id, event):
        # drag the tail of a line specified by the line_id
        # to the coordinates of the event
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
        elif self._get_line_dist(*raw_linecoords) >= self._line_thrshld: # new line is large enough
            self._mini_lines.remove(line_id)
            mod_linecoords = self._get_mod_linecoords(*raw_linecoords)
        else: # keep drawing small line
            mod_linecoords = raw_linecoords
        self.coords(line_id, *mod_linecoords)

    def _drag(self, event, state_id):
        # drag the state around the canvas
        self._moving_obj = True
        coords = (
            self.canvasx(event.x)-12,
            self.canvasy(event.y)-12,
            self.canvasx(event.x)+13,
            self.canvasy(event.y)+13)
        self.coords(state_id, *coords)
        self.coords(str(state_id)+'t', coords[0]+12, coords[1]+12)
        self.coords(str(state_id)+'f', coords[0]-3, coords[1]-3, coords[2]+3, coords[3]+3)
        self.coords(str(state_id)+'i', coords[0]-20, coords[1]-20, coords[0], coords[1])
        try:
            for line_id in self.find_withtag('-'+str(state_id)):
                self._drag_line_head(line_id, event)
        except KeyError: pass
        try:
            for line_id in self.find_withtag(str(state_id)+'-'):
                self._drag_line_tail(line_id, event)
        except KeyError: pass

    def _drop(self, event):
        # drop the state
        self._moving_obj = False

    def _update_status(self, state_num):
        # update the status bar with the specified state number
        if not self._moving_obj:
            self.info_manager.update_status('State {}'.format(state_num))

    def _clear_status(self):
        # clear the status bar if not moving a state
        if not self._moving_obj:
            self.info_manager.clear_status()

    def add_state(self, state_num, as_init):
        """Add a state to the display.

        Parameters:
            state_num (int): The state number of the newly added state.
            as_init (bool): Whether or not the newly added state is an initial state.
        """
        x,y = self.canvasx(75+randrange(150)),self.canvasy(75+randrange(200))
        coords = (x, y, x+25, y+25)
        state_id = self.create_oval(*coords, fill=self._default_state_fill)
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
            # draw init arrow to show as init state
            self.create_line(x-20,y-20,x,y,
                arrow=self._lines_config['arrow'], tags=str(state_id)+'i', width=self._lines_config['width'])
            self._init_id = state_id

    def del_state(self, state_num, init_deleted):
        """Delete a state from the display.

        Parameters:
            state_num (int): The number of the state to delete.
            init_deleted (bool): Whether or not the state to delete is an initial state.
        """
        state_id = self._id_map[state_num]
        core_tag = str(state_id)
        self.delete(state_id)
        for line_id in self.find_withtag(core_tag+'-'):
            self._mini_lines.discard(line_id)
            self._loops.discard(line_id)
            self.delete(line_id)
        for line_id in self.find_withtag('-'+core_tag):
            self._mini_lines.discard(line_id)
            self.delete(line_id)
        self.delete(core_tag+'f')
        self.delete(core_tag+'t')
        if init_deleted:
            self.delete(str(state_id)+'i')
            if self.machine.init_state != 0:
                self.set_init(self.machine.init_state)

    def set_init(self, state_num):
        """Set the specified state as initial.

        The initial state has an arrow pointing to it with no source,
        indicating the entry point of the machine.

        Parameters:
            state_num (int): The number of the state to set as initial.
        """
        self.delete(str(self._init_id)+'i')
        state_id = self._id_map[state_num]
        tag = str(state_id) + 'i'
        x,y,_,_ = self.coords(state_id)
        self.create_line(x-20,y-20,x,y,
            arrow=self._lines_config['arrow'], tags=tag, width=self._lines_config['width'])
        self._init_id = state_id

    def set_final(self, state_num):
        """Set the specified state as final.

        A final state is enclosed in another circle. In other words, a final state
        is indicated with another circle forming the outer edge of the original inner
        circle.

        Parameters:
            state_num (int): The number of the state to set as final.
        """
        state_id = self._id_map[state_num]
        tag = str(state_id) + 'f'
        if len(self.find_withtag(tag)) == 0:
            state_coords = self.coords(state_id)
            coords = (state_coords[0]-3, state_coords[1]-3, state_coords[2]+3, state_coords[3]+3)
            self.create_oval(*coords, tags=tag)

    def set_nonfinal(self, state_num):
        """Set the specified state as non-final.

        Parameters:
            state_num (int): The number of the state to set as non-final.
        """
        state_id = self._id_map[state_num]
        tag = str(state_id) + 'f'
        self.delete(tag)

    def _add_loop(self, state_num):
        # add a loop transition to the specified state
        state_coords = self.coords(self._id_map[state_num])
        coords = (
            state_coords[0]+6,state_coords[1]+2,
            state_coords[0]-9,state_coords[1]-23,
            state_coords[0]+31,state_coords[1]-23,
            state_coords[0]+16,state_coords[1]+2)
        tag1 = str(self._id_map[state_num]) + '-'
        tag2 = '{}-{}'.format(state_num,state_num)
        line_id = self.create_line(*coords, smooth=True, tags=(tag1,tag2), **self._lines_config)
        self.tag_bind(line_id, '<ButtonPress-1>', lambda e: self.info_manager.show_transitions(state_num,state_num))
        self._loops.add(line_id)

    def add_transition(self, from_state, to_state, cnf):
        """Add a transition to the display.

        Parameters:
            from_state (int): The state number of the source of the transition.
            to_state (int): The state number of the target of the transition.
            cnf (str): The configuration of the transition.
        """
        # may not need cnf
        find_result = self.find_withtag('{}-{}'.format(from_state,to_state))
        if len(find_result) == 1:
            line = find_result[0]
            if self.itemcget(line, 'arrow') == 'first':
                self.itemconfig(line, arrow='both')
            return
        elif len(self.find_withtag('{}-{}'.format(to_state,from_state))) == 1:
            line_id = self.find_withtag('{}-{}'.format(to_state,from_state))[0]
            self.itemconfig(line_id, arrow='both')
            return
        if from_state == to_state:
            return self._add_loop(from_state)
        f_coords = self.coords(self._id_map[from_state])
        f_coords = (f_coords[0]+13, f_coords[1]+13)
        t_coords = self.coords(self._id_map[to_state])
        t_coords = (t_coords[0]+13, t_coords[1]+13)
        coords = (f_coords[0], f_coords[1], t_coords[0], t_coords[1])
        mini_line = self._get_line_dist(*coords) <= self._line_thrshld
        line_coords = self._get_mod_linecoords(*coords) if not mini_line else coords
        tag1 = str(self._id_map[from_state]) + '-'
        tag2 = '-' + str(self._id_map[to_state])
        tag3 = '{}-{}'.format(from_state,to_state)
        line_id = self.create_line(line_coords, tags=(tag1,tag2,tag3), **self._lines_config)
        if mini_line: self._mini_lines.add(line_id)
        self.tag_bind(line_id, '<ButtonPress-1>', lambda e: self.info_manager.show_transitions(from_state,to_state))

    def del_transition(self, from_state, to_state, cnf):
        """Delete a transition to the display.

        Parameters:
            from_state (int): The state number of the source of the transition.
            to_state (int): The state number of the target of the transition.
            cnf (str): The configuration of the transition.
        """
        # may not need cnf
        if self.machine.get_transition_count(from_state, to_state) != 0:
            return
        find_result1 = self.find_withtag('{}-{}'.format(from_state,to_state))
        find_result2 = self.find_withtag('{}-{}'.format(to_state,from_state))
        if len(find_result1) == 0 and len(find_result2) == 0: # transition does not exist
            return
        elif len(find_result1) == 1: # 'from_state-to_state' is tag
            line_id = find_result1[0]
            arrow_cnf = self.itemcget(line_id, 'arrow')
            if arrow_cnf == 'both':
                self.itemconfig(line_id, arrow='first')
            elif arrow_cnf == 'first': # line exists, but transition does not exist
                return
            else:
                self._mini_lines.discard(line_id)
                self._loops.discard(line_id)
                self.delete(line_id)
        else: # 'to_state-from_state' is tag
            line_id = find_result2[0]
            arrow_cnf = self.itemcget(line_id, 'arrow')
            if arrow_cnf == 'both':
                self.itemconfig(line_id, arrow='last')
            elif arrow_cnf == 'last': # line exists, but transition does not exist
                return
            else:
                self._mini_lines.discard(line_id)
                self._loops.discard(line_id)
                self.delete(line_id)
    
    def highlight_state(self, state_num):
        """Highlight the specified state in the display.

        This is used during the sequential tests to indicate which state the
        machine is currently in.

        Parameters:
            state_num (int): The state number to highlight.
        """
        if self._highlighted_state_id is not None:
            self.itemconfig(self._highlighted_state_id, fill=self._default_state_fill)
        state_id = self._id_map[state_num]
        self.itemconfig(state_id, fill=self._highlight_fill)
        self._highlighted_state_id = state_id

    def clear_highlight(self):
        """Clear the  highlighted state, if any."""
        if self._highlighted_state_id is not None:
            self.itemconfig(self._highlighted_state_id, fill=self._default_state_fill)
            self._highlighted_state_id = None
