#!/usr/bin/env python3

# Main script for the terminal-driven version of DTM Simulator
# Currently a work in progress

from utils import Machine, Transition

class Simulator():
    def __init__(self):
        self.main_menu_opts = [
            'View machine info',
            'Add a state',
            'Delete a state',
            'Add a transition',
            'Delete a transition',
            'Set state as final',
            'Set state as non-final',
            'Test Machine',
            'Exit'
        ]
        self.main_menu_size = len(self.main_menu_opts)

    def print_welcome(self):
        print('  DTM Simulator')
        print('Test your designs of a simple Deterministic Turing Machine.', end='\n\n')

    def init_machine(self):
        while True:
            try:
                num_states = int(input('Enter number of states in the machine: '))
                self.machine = Machine(num_states)
                break
            except:
                print('INVALID INPUT')

    def print_menu_opts(self, opts):
        for i, option in enumerate(opts):
            print(i+1, '. ', option, sep='')

    def get_user_choice(self, prompt, menu_size):
        while True:
            try:
                choice = int(input(prompt))
                if choice not in range(1,menu_size+1):
                    raise Exception()
                else:
                    return choice
            except:
                print('INVALID INPUT')

    def get_user_int(self, prompt, range):
        while True:
            try:
                choice = int(input(prompt))
                if choice not in range:
                    raise Exception()
                else:
                    return choice
            except:
                print('INVALID INPUT')

    def get_user_str(self, prompt):
        return input(prompt)

    def process_add_transition(self):
        print('> Main Menu > Add Transition')
        prompt1 = 'Enter the state number for the source of this transition: '
        prompt2 = 'Enter the state number for the target of this transition: '
        target_range = self.machine.states
        from_state = self.get_user_int(prompt1, target_range)
        to_state = self.get_user_int(prompt2, target_range)
        print('Configuration: (r,w,m) where r is input symbol, w is symbol to write, m is "l" or "r" case-insensitive')
        print('** Don\'t forget the parentheses')
        cnf = self.get_user_str('Enter the transition config: ')
        try:
            self.machine.add_transition(from_state, to_state, cnf)
            print('Successfully added transition from {} to {}: {}'.format(from_state,to_state,cnf))
        except Exception as e:
            print('ERROR:', e)

    def process_del_transition(self):
        pass

    def test_machine(self):
        print('> Main Menu > Test Machine')
        prompt = 'Enter 0 to test whether the string is accepted or rejected,\n' \
            'otherwise enter 1 to compute the string as a function: '
        as_function = self.get_user_int(prompt, range(2)) == 1
        string = self.get_user_str('Enter the string: ')
        result = self.machine.compute(string, as_function)
        if as_function:
            print('Tape result:', result)
        else:
            print('String:', string)
            print('Result:', 'Accepted' if result[0] else 'Rejected')
            print('Tape result:', result[1])

    def run(self):
        self.print_welcome()
        self.init_machine()
        done = False
        while not done:
            print('> Main Menu')
            self.print_menu_opts(self.main_menu_opts)
            user_choice = self.get_user_choice('Enter choice: ', self.main_menu_size)
            if user_choice == self.main_menu_size: # user wants to exit
                done = True
            elif user_choice == 1: # view machine info
                info = self.machine.get_info()
                for description in info:
                    print('{}: {}'.format(description, info[description]))
            elif user_choice == 2: # add state
                self.machine.add_state()
                print('New state added, for a total of {} states'.format(self.machine.num_states))
            elif user_choice == 3: # del state
                print('> Main Menu > Delete State')
                target_state = self.get_user_int('Enter state number: ', self.machine.states)
                self.machine.del_state(target_state)
                print('Deleted state number {}'.format(target_state))
            elif user_choice == 4: # add transition
                self.process_add_transition()
            elif user_choice == 5: # del transition
                self.process_del_transition()
            elif user_choice == 6: # set final state
                print('> Main Menu > Set Final State')
                target_state = self.get_user_int('Enter the state number: ', self.machine.states)
                self.machine.set_final_state(target_state)
                print('Successfully set state number {} as final'.format(target_state))
            elif user_choice == 7: # set nonfinal state
                print('> Main Menu > Set Non-final State')
                target_state = self.get_user_int('Enter the state number: ', self.machine.states)
                self.machine.set_nonfinal_state(target_state)
                print('Successfully set state number {} as non-final'.format(target_state))
            else:                  # test machine
                self.test_machine()

if __name__ == '__main__':
    app = Simulator()
    app.run()
