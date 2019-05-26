#!/usr/bin/env python3

# Classes to represent the DTM and transitions within it

import re

class Machine():
    def __init__(self, num_states, blank_symbol='#'):
        if type(num_states) is not int:
            raise TypeError('num_states arg must be an integer')
        if num_states < 0:
            raise Exception('num_states arg cannot be less than zero')
        self.num_states = num_states
        self.max_state_num = num_states
        self.blank = blank_symbol
        self.transitions = {}
        self.states = set([])
        self.final_states = {}
        for i in range(1, num_states+1):
            self.transitions[i] = {}
            self.final_states[i] = False
            self.states.add(i)
    
    def get_info(self):
        info = {}
        info['Number of States'] = self.num_states
        final_states = []
        nonfinal_states = []
        for state_num in self.final_states:
            if self.final_states[state_num]:
                final_states.append(str(state_num))
            else:
                nonfinal_states.append(str(state_num))
        info['Final States'] = ' '.join(final_states)
        info['Non-final states'] = ' '.join(nonfinal_states)
        transition_count = 0
        transition_info = '\n'
        for from_state in self.transitions:
            for to_state in self.transitions[from_state]:
                transition_info += '  {} -> {}: '.format(from_state, to_state)
                for transition in self.transitions[from_state][to_state]:
                    transition_info += str(transition) + ' '
                transition_info += '\n'
        info['Transitions'] = transition_info[:-2] if transition_info != '\n' else 'None'
        return info

    def add_state(self):
        self.num_states += 1
        self.max_state_num += 1
        self.final_states[self.max_state_num] = False
        self.transitions[self.max_state_num] = {}
        self.states.add(self.max_state_num)

    def del_state(self, state_num):
        pass

    def add_transition(self, from_state, to_state, cnf):
        if from_state not in range(1, self.num_states+1):
            raise Exception('from_state arg out of range: [1...{}]'.format(self.num_states))
        if to_state not in range(1, self.num_states+1):
            raise Exception('to_state arg out of range: [1...{}]'.format(self.num_states))
        if type(cnf) is not str:
            raise TypeError('cnf arg must be of str type')
        transition = Transition(from_state, to_state, cnf)
        try:
            dup = transition in self.transitions[from_state][to_state]
        except KeyError:
            self.transitions[from_state][to_state] = set([])
            dup = False
        finally:
            if dup:
                raise Exception('transition {} would make the machine non-deterministic'.format(cnf))
            else:
                self.transitions[from_state][to_state].add(transition)

    def del_transition(self, from_state, to_state, cnf):
        try:
            target = next((x for x in self.transitions[from_state][to_state] if x.cnf == cnf))
        except (StopIteration, KeyError):
            return
        self.transitions[from_state][to_state].remove(target)

    def print_transitions(self):
        for from_state in self.transitions:
            for to_state in self.transitions[from_state]:
                print(from_state, ' -> ', to_state, ': ', sep='', end='')
                for transition in self.transitions[from_state][to_state]:
                    print(str(transition), end=' ')
                print()

    def set_final_state(self, state_num):
        if state_num in self.states:
            self.final_states[state_num] = True

    def set_nonfinal_state(self, state_num):
        if state_num in self.states:
            self.final_states[state_num] = False

    def compute(self, string, as_function=False):
        '''
        Computes the given string and by default returns True if the string
        was accepted or False if it was rejected, along with the final state of the
        tape. If as_function=True then computation continues until the machine halts
        when no appropriate transition can be used. In this case, only the final state
        of the tape is returned.
        '''
        string = list(string)
        string.append(self.blank)
        max_len = len(string)
        current_state = 1
        index = 0
        done = False
        while not done and (as_function or not self.final_states[current_state]):
            target_sets = self.transitions[current_state].values()
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
                if index == max_len:
                    string.append(self.blank)
                    max_len += 1
            else: # no transition found
                done = True
        if as_function:
            return ''.join(string) + '...'
        elif index < 0 or not self.final_states[current_state]:
            return False, ''.join(string) + '...'
        else:
            return True, ''.join(string) + '...'

class Transition():
    def __init__(self, from_state, to_state, cnf):
        '''
        Initialize a transition between from_state to to_state
        both from_state and to_state are assumed to be valid
        cnf: configuration for the transition, matching the regular
            expression: (r,w,m) where r is the input symbol, w is
            what to write, and m is either L or R case-insensitive
            (don't forget the parentheses, and spaces can separate
            the commas from the next character for readability; (r, w, m))
        '''
        match = re.fullmatch(r'\((\S),\s*(\S),\s*([lLrR])\)', cnf)
        if match is None:
            raise Exception('given cnf for transition is invalid: {}'.format(cnf))
        else:
            self.from_state = from_state
            self.to_state = to_state
            self.cnf = re.sub(' ', '', cnf)
            self.read = match[1]
            self.write = match[2]
            self.move = match[3]

    def __str__(self):
        return self.cnf
    
    def __hash__(self):
        return hash(self.read)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.read == other.read
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)