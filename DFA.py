from NFA import *
from constants import *
from utils import *
import os.path

class DFASubsets:
    def __init__(self, nfa: NFA):
        self.nfa = nfa
        self.states = []
        self.initial_state = None
        self.transitions = {}
        self.symbols = None
        self.final_states = []
    
    def accepts(self, string):
        state = self.initial_state
        for symbol in string:
            state = self.transitions[state][symbol]
        return state in self.final_states
    
    def eClosure(self, states):
        eClosure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            if state in self.nfa.transitions and EPSILON in self.nfa.transitions[state]:
                for accept_state in self.nfa.transitions[state][EPSILON]:
                    if accept_state not in eClosure:
                        eClosure.add(accept_state)
                        stack.append(accept_state)
        return eClosure

    def move(self, states, symbol):
        move = set()
        for state in states:
            if state in self.nfa.transitions and symbol in self.nfa.transitions[state]:
                move.update(self.nfa.transitions[state][symbol])
        return self.eClosure(move) 

    def create_DFASubset(self):
        initial_state = frozenset(self.eClosure([self.nfa.q0]))
        self.states.append(initial_state)
        self.initial_state = initial_state
        stack = [initial_state]
        while stack:
            state = stack.pop()
            for symbol in self.nfa.alphabet:
                if symbol != EPSILON:  # Ignore epsilon transitions
                    move = self.move(state, symbol)
                    if move:
                        eClosure = frozenset(self.eClosure(move))
                        if eClosure not in self.states:
                            self.states.append(eClosure)
                            stack.append(eClosure)
                        self.transitions[(state, symbol)] = eClosure

        self.symbols = self.nfa.alphabet - {EPSILON} 

        for state in self.states:
            for nfa_final_state in self.nfa.f:
                if nfa_final_state in state:
                    self.final_states.append(state)
                    break

        return self

    def simulate(self, input_string):
        current_state = self.initial_state
        for symbol in input_string:
            if symbol not in self.symbols:
                return False
            current_state = self.transitions.get((current_state, symbol), None)
            if current_state is None:
                return False
        return current_state in self.final_states
    
    def min_DFASubset(self):
        partition = [set(self.final_states), set(self.states) - set(self.final_states)]
        worklist = [set(self.final_states)]

        while worklist:
            A = worklist.pop()
            for symbol in self.symbols:
                affected_states = set()
                for state in self.states:
                    if (state, symbol) in self.transitions and self.transitions[(state, symbol)] in A:
                        affected_states.add(state)

                for Y in partition.copy():
                    if not Y & affected_states:
                        continue

                    X1 = Y & affected_states
                    X2 = Y - X1

                    partition.remove(Y)
                    partition.extend([X1, X2])

                    if Y in worklist:
                        worklist.remove(Y)
                        worklist.extend([X1, X2])
                    else:
                        worklist.append(X1 if len(X1) <= len(X2) else X2)

        # Update the DFA states and transitions using the minimized partitions
        new_states = [frozenset(P) for P in partition if P]  # Add "if P" to filter out empty states
        new_initial_state = next(s for s in new_states if self.initial_state in s)
        new_final_states = [s for s in new_states if s & set(self.final_states)]
        new_transitions = {}

        for symbol in self.symbols:
            for new_state in new_states:
                old_state = next(iter(new_state))
                if (old_state, symbol) in self.transitions:
                    new_target_state = next(s for s in new_states if self.transitions[(old_state, symbol)] in s)
                    new_transitions[(new_state, symbol)] = new_target_state

        self.states = new_states
        self.initial_state = new_initial_state
        self.final_states = new_final_states
        self.transitions = new_transitions

    def showDFASubset(self,file_name):
        file_path = Utils.create_file_path(file_name)
        f = open(file_path+'.txt', 'w+', encoding="utf-8")
        f.write("---------------DFA---------------\n")
        # Print the initial state
        initial_state_id = self.states.index(self.initial_state)
        f.write(f"Initial State: {initial_state_id}")
        f.write('\n')
        # Print the final states
        f.write("Final States:\n")
        for state_set in self.final_states:
            state_id = self.states.index(state_set)
            f.write(f"  State {state_id}")
            f.write('\n')
        
        # Print the transitions
        f.write("Transitions:\n")
        for (state_set, symbol), target_state_set in self.transitions.items():
            state_id = self.states.index(state_set)
            target_state_id = self.states.index(target_state_set)
            f.write(f"  {state_id} --({symbol})--> {target_state_id}")
            f.write('\n')

    def showMinimized(self,file_name):
        file_path = Utils.create_file_path(file_name)
        f = open(file_path+'.txt', 'w+', encoding="utf-8")
        f.write("---------------DFA MINIMIZED---------------\n")
        # Print the states
        f.write("States:\n")
        for state_set in self.states:
            state_id = self.states.index(state_set)
            f.write(f"  State {state_id}: {state_set}")
            f.write('\n')
        
        # Print the initial state
        initial_state_id = self.states.index(self.initial_state)
        f.write(f"Initial State: {initial_state_id}")
        f.write('\n')
        # Print the final states
        f.write("Final States:\n")
        for state_set in self.final_states:
            state_id = self.states.index(state_set)
            f.write(f"  State {state_id}")
            f.write('\n')
        
        # Print the transitions
        f.write("Transitions:\n")
        for (state_set, symbol), target_state_set in self.transitions.items():
            state_id = self.states.index(state_set)
            target_state_id = self.states.index(target_state_set)
            f.write(f"  {state_id} --({symbol})--> {target_state_id}")
            f.write('\n')