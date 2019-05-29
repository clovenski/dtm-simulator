"""
Classes to represent the DTM, transitions within it and a testing state
during computation
"""

import re

class Machine():
    """This is a class to simulate a semi-infinite deterministic Turing machine.

    Attributes:
        num_states (int): The number of states in the machine.
        max_state_num (int): The largest state number in the machine.
        blank (str): The character representing the blank symbol on the tape.
            (default '#')
        transitions (dict): Dictionary equivalent to an adjacency list, mapping
            their state numbers and storing a set of all transitions between
            them
        states (set): A set containing all the current state numbers.
        init_state (int): State number of the initial state. (default 0 for
            no inital state set)
        final_states (dict): Dictionary mapping each state number to True
            if it is a final state, False otherwise.
        abort (bool): Flag to indicate aborting a computation test. Should
            only be set to True to stop the machine from further executing
            an infinite loop during the compute() function.
    """

    def __init__(self, num_states, blank_symbol='#', init_state=0):
        """Initialize machine with the given number of states, blank symbol
        and inital state.

        Parameters:
            num_states (int): Initial number of states in the machine. Cannot
                be negative.
            blank_symbol (str): Character to represent the blank symbol on the
                tape. (default '#') Only first character of the string is set.
            init_state (int): State number of the initial state. (default 0)
                Must be in range(num_states+1), else set to 0.
        """
        if type(num_states) is not int:
            raise TypeError('num_states arg must be an integer')
        if num_states < 0:
            raise Exception('num_states arg cannot be less than zero')
        self.num_states = num_states
        self.max_state_num = num_states
        self.blank = blank_symbol[0]
        self.transitions = {}
        self.states = set([])
        self.init_state = init_state if init_state in range(num_states+1) else 0
        self.final_states = {}
        self.abort = False
        for i in range(1, num_states+1):
            self.transitions[i] = {}
            self.final_states[i] = False
            self.states.add(i)
    
    def get_info(self):
        """Return a dictionary containing machine information.

        Keys of the dictionary include: '# of states', 'Non-final states',
        'Final states', '# of non-final states', '# of final states',
        '# of transitions', 'Transitions'.
        """
        info = {}
        info['# of states'] = self.num_states
        final_states = []
        nonfinal_states = []
        for state_num in self.final_states:
            if self.final_states[state_num]:
                final_states.append(str(state_num))
            else:
                nonfinal_states.append(str(state_num))
        info['Non-final states'] = ' '.join(nonfinal_states)
        info['Final states'] = ' '.join(final_states)
        info['Initial state'] = self.init_state
        info['# of non-final states'] = len(nonfinal_states)
        info['# of final states'] = len(final_states)
        transition_cnt = 0
        for s in self.transitions.values():
            transition_cnt += len(s)
        info['# of transitions'] = transition_cnt
        transition_info = '\n'
        for from_state in self.transitions:
            for to_state in self.transitions[from_state]:
                transition_info += '  {} -> {}: '.format(from_state, to_state)
                for transition in self.transitions[from_state][to_state]:
                    transition_info += str(transition) + ' '
                transition_info += '\n'
        info['Transitions'] = transition_info[:-2] if transition_info != '\n' else 'None'
        return info

    def get_transitions(self, from_state, to_state):
        """Return a list containing the transitions in from_state -> to_state"""
        try:
            return list(str(t) for t in self.transitions[from_state][to_state])
        except KeyError:
            return []

    def get_transition_count(self, from_state, to_state):
        """Return the number of transitions in from_state -> to_state"""
        try:
            return len(self.transitions[from_state][to_state])
        except KeyError:
            return 0

    def add_state(self):
        """Add a state to the machine.

        The new state's number will be the current max_state_num + 1,
        setting the new max_state_num and becoming the initial state
        if it is the only state in the machine.
        """
        self.num_states += 1
        self.max_state_num += 1
        self.final_states[self.max_state_num] = False
        self.transitions[self.max_state_num] = {}
        self.states.add(self.max_state_num)
        if self.num_states == 1:
            self.init_state = self.max_state_num

    def del_state(self, state_num):
        """Delete the state with the specified number.

        Returns True if state_num is a valid state number, False otherwise;
        both cases representing whether or not the state was properly deleted.
        """
        if state_num not in self.states:
            return False
        else:
            self.states.remove(state_num)
            del self.final_states[state_num]
            self.num_states -= 1
            if state_num == self.init_state:
                self.init_state = min(self.states) if len(self.states) > 0 else 0
            if state_num == self.max_state_num:
                self.max_state_num = max(self.states) if len(self.states) > 0 else 0
            del self.transitions[state_num]
            for f in self.states:
                try:
                    del self.transitions[f][state_num]
                except:
                    continue
            return True

    def add_transition(self, from_state, to_state, cnf):
        """Add a transition to the machine.

        Parameters:
            from_state (int): The source of the transition. Must be a valid state
                number in the machine.
            to_state (int): The target of the transition. Must be a valid state
                number in the machine.
            cnf (str): The configuration of the transition. Must be of the form
                '(r,w,m)' where r is the input symbol, w is the write symbol and
                m is either 'l' or 'r' case-insensitive to indicate where to move.
        """
        if from_state not in range(1, self.num_states+1):
            raise Exception('Invalid source')
        if to_state not in range(1, self.num_states+1):
            raise Exception('Invalid target')
        if type(cnf) is not str:
            raise TypeError('Configuration must be string')
        transition = Transition(from_state, to_state, cnf)
        dup = False
        for s in self.transitions[from_state].values():
            dup = transition in s
            if dup: break
        if not dup:
            try:
                self.transitions[from_state][to_state].add(transition)
            except KeyError:
                self.transitions[from_state][to_state] = set([transition])
        else:
            raise Exception('Non-determinism')

    def del_transition(self, from_state, to_state, cnf):
        """Delete a transition in the machine.

        Returns True if a transition was successfully deleted, False otherwise.
        """
        try:
            target = next((x for x in self.transitions[from_state][to_state] if x.cnf == cnf))
        except (StopIteration, KeyError):
            return False
        self.transitions[from_state][to_state].remove(target)
        if len(self.transitions[from_state][to_state]) == 0:
            del self.transitions[from_state][to_state]
        return True

    def print_transitions(self):
        """Print each transition in the machine.

        What's printed on each line is 'f -> t: ' where f is the source and
        t is the target, followed be the configuration of each pertaining transition,
        separated by a whitespace.
        """
        for from_state in self.transitions:
            for to_state in self.transitions[from_state]:
                print(from_state, ' -> ', to_state, ': ', sep='', end='')
                for transition in self.transitions[from_state][to_state]:
                    print(str(transition), end=' ')
                print()

    def set_init_state(self, state_num):
        """Set the specified state as the inital state.

        The specified state_num must be valid, otherwise an Exception
        is raised.
        """
        if state_num in self.states:
            self.init_state = state_num
        else:
            raise Exception('Invalid state number')

    def set_final_state(self, state_num):
        """Set the specified state as a final state.

        The specified state_num must be valid, otherwise an Exception
        is raised.
        """
        if state_num in self.states:
            self.final_states[state_num] = True
        else:
            raise Exception('Invalid state number')

    def set_nonfinal_state(self, state_num):
        """Set the specified state as non-final

        The specified state_num must be valid, otherwise an Exception
        is raised.
        """
        if state_num in self.states:
            self.final_states[state_num] = False
        else:
            raise Exception('Invalid state number')

    def is_empty(self):
        """Return True if the machine has zero states, False otherwise"""
        return len(self.states) == 0

    def compute(self, string, as_function=False):
        '''Compute the given string.

        This function by default returns True if the string was accepted or False
        if it was rejected, along with the final state of the tape. If as_function=True
        then computation continues until the machine halts when no appropriate
        transition can be used. In this case, only the final state of the tape is returned.

        If the tape result is longer than 50 characters, only the first 50 are returned with
        a question mark at the end to indicate this was the case.
        '''
        if len(self.states) == 0:
            raise Exception('empty machine')
        string = list(string)
        string.append(self.blank)
        max_len = len(string)
        current_state = self.init_state
        index = 0
        done = False
        self.abort = False
        while not self.abort and not done and (as_function or not self.final_states[current_state]):
            target_sets = self.transitions[current_state].values()
            # find the target (transition) to use
            target = None
            for transition_set in target_sets:
                try:
                    target = next(x for x in transition_set if x.read == string[index])
                except StopIteration:
                    continue
                if target is not None:
                    break
            if target is not None:
                current_state = target.to_state
                string[index] = target.write
                index += 1 if target.move == 'r' or target.move == 'R' else -1
                if index < 0:
                    done = True
                elif index == max_len:
                    string.append(self.blank)
                    max_len += 1
            else: # no transition found
                done = True
        self.abort = False
        long_string = len(string) > 50
        if as_function:
            return (''.join(string[:50]) + '...?') if long_string else (''.join(string) + '...')
        elif index < 0 or not self.final_states[current_state]:
            return (False, ''.join(string[:50]) + '...?') if long_string else (False, ''.join(string) + '...')
        else:
            return (True, ''.join(string[:50]) + '...?') if long_string else (True, ''.join(string) + '...')

    def compute_one(self, testing_state):
        '''Compute one input in the given testing_state.

        This function adjusts the values in the testing state appropriately.

        Parameters:
            testing_state (TestingState): The state of a test to work on.
        '''
        if len(self.states) == 0:
            raise Exception('empty machine')
        string = list(testing_state.tape) if len(testing_state.tape) != 0 else ['#']
        index = testing_state.index
        max_len = len(string)
        as_function = testing_state.as_function
        current_state = testing_state.current_state
        if not as_function and self.final_states[current_state]:
            testing_state.done = True
            testing_state.result = True
            testing_state.tape += '#...'
            return
        target_sets = self.transitions[current_state].values()
        # find the target (transition) to use
        target = None
        for transition_set in target_sets:
            try:
                target = next(x for x in transition_set if x.read == string[index])
            except StopIteration:
                continue
            if target is not None:
                break
        if target is not None:
            testing_state.current_state = target.to_state
            if not as_function and self.final_states[target.to_state]:
                testing_state.done = True
                testing_state.result = True
            string[index] = target.write
            index += 1 if target.move == 'r' or target.move == 'R' else -1
            if index < 0:
                testing_state.done = True
                if not as_function: testing_state.result = False
            elif index == max_len:
                string.append(self.blank)
        else: # no transition found
            testing_state.done = True
            if not as_function: testing_state.result = False
        testing_state.tape = ''.join(string)
        testing_state.index = index
        if testing_state.done:
            testing_state.tape += '#...'

class Transition():
    """This is a class to represent a transition in the machine.

    Attributes:
        from_state (int): The source of this transition.
        to_state (int): The target of this transition.
        cnf (str): The configuration of this transition.
        read (str): The character in which represents the input.
        write (str): The character in which represent the output
            onto the tape.
        move (str): Either 'l' or 'r' case-insensitive indicating
            the move the machine will make.
    """

    def __init__(self, from_state, to_state, cnf):
        '''Initialize this transition with the given arguments.

        Initialize a transition between from_state to to_state.
        Both from_state and to_state are assumed to be valid.
        cnf: configuration for the transition, matching the regular
            expression: (r,w,m) where r is the input symbol, w is
            what to write, and m is either L or R case-insensitive
            (don't forget the parentheses, and spaces can separate
            the commas from the next character for readability; (r, w, m))
        '''
        match = re.fullmatch(r'\((\S),\s*(\S),\s*([lLrR])\)', cnf)
        if match is None:
            raise Exception('Invalid configuration')
        else:
            self.from_state = from_state
            self.to_state = to_state
            self.cnf = re.sub(' ', '', cnf)
            self.read = match[1]
            self.write = match[2]
            self.move = match[3]

    def __str__(self):
        """Return the configuration of this transition."""
        return self.cnf
    
    def __hash__(self):
        """Return a hash of this transition's input/read symbol"""
        return hash(self.read)

    def __eq__(self, other):
        """Return whether or not this transition is equal to other.

        Two transitions are equivalent if and only if their input/read
        symbols are equivalent.
        """
        if isinstance(other, self.__class__):
            return self.read == other.read
        else:
            return False

    def __ne__(self, other):
        """Return True if this transition is not equal to other, False otherwise."""
        return not self.__eq__(other)

class TestingState():
    """This is a class to represent a testing state in the sequential tests.

    Attributes:
        result (bool): The result of the test; True indicating acceptance and
            False indicating rejection. This will not be None only if
            done is True. If as_function is True, then this will always be None.
        done (bool): Boolean to indicate the test is done.
        index (int): The current index on the tape.
        current_state (int): The current state of the machine.
        tape (str): The current status of the tape of the machine.
        as_function (bool): Boolean value to indicate the machine is
            being used as a function.
    """

    def __init__(self, string, as_function, init_state):
        """Initialize this testing state.

        The test always starts at index 0 on the string/tape.

        Parameters:
            string (str): The string that the machine will test.
            as_function (bool): Boolean value to indicate the machine is
                being used as a function.
            init_state (int): The state number of the initial state of the machine.
        """
        self.result = None
        self.done = False
        self.index = 0
        self.current_state = init_state
        self.tape = string
        self.as_function = as_function
