#!/usr/bin/env python3

# Main script for the terminal-driven version of DTM Simulator
# Currently a work in progress

from utils import Machine, Transition

if __name__ == '__main__':
    # example code to test classes in utils.py
    m = Machine(6)
    m.add_transition(1,2,'(a,X,r)')
    m.add_transition(2,2,'(B,B,r)')
    m.add_transition(2,2,'(a,a,r)')
    m.add_transition(2,3,'(b,B,l)')
    m.add_transition(3,3,'(a,a,l)')
    m.add_transition(3,3,'(B,B,L)')
    m.add_transition(3,1,'(X, X, R)')
    m.add_transition(1,4,'(#,    #, R)')
    m.add_transition(1,5,'(B, B,R)')
    m.add_transition(5,5,'(B,B, r)')
    m.add_transition(5,6,'(#,#,r)')
    m.set_final_state(4)
    m.set_final_state(6)
    m.print_transitions()
    result = m.compute('aaaaabbbbb')
    print('Accepted' if result[0] else 'Rejected')
    print('Tape result:', result[1])
