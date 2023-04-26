from constants import *
import os.path
from utils import *

class Transition:
    def __init__(self, start_state, symbol, accept_state):
        self.start_state = start_state
        self.symbol = symbol
        self.accept_state = accept_state

    def start(self, start_state):
        self.start_state = start_state

    def accept(self, accept_state):
        self.accept_state = accept_state

class State:
    def __init__(self, label=None):
        self.label = label
        self.accept = False

    def __repr__(self):
        return f"{self.label}"
    
class NFA:
    """
    Representa el NFA:
    -> q es el conjunto de estados
    -> expr es una expresión regular que define el lenguaje aceptado por el NFA
    -> alphabet es el alfabeto del lenguaje
    -> q0 es el estado inicial
    -> f es el conjunto de estados de aceptación 
    -> transitions es el conjunto de transiciones entre estados
    """
    def __init__(self, q, expr, alphabet, q0, f, transitions):
        self.q = q
        self.expr = expr
        self.alphabet = alphabet
        self.q0 = q0
        self.f = f
        self.transitions = transitions

    # true if the is any final state else False
    def simulate(self, input_string):
        current_states = self.e_closure(set([self.q0]))
        for symbol in input_string:
            new_states = set()
            for state in current_states:
                if state in self.transitions and symbol in self.transitions[state]:
                    new_states = new_states.union(self.e_closure(self.transitions[state][symbol]))
            current_states = new_states
        return bool(current_states.intersection(self.f))
    
    def e_closure(self, states):
        e_closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            if state in self.transitions and EPSILON in self.transitions[state]:
                for accept_state in self.transitions[state][EPSILON]:
                    if accept_state not in e_closure:
                        e_closure.add(accept_state)
                        stack.append(accept_state)
        return e_closure
    
    def showNFA(self,file_name):
        file_path = Utils.create_file_path(file_name)
        f = open(file_path+'.txt', 'w+', encoding="utf-8")
        f.write("---------------NFA---------------\n")
        f.write("Q: " + str(self.q))
        f.write('\n')
        f.write('Alphabet: ' + str(self.alphabet))
        f.write('\n')
        f.write('Inicio: ' +  str(self.q0))
        f.write('\n')
        f.write('Aceptacion: ' + str(self.f))
        f.write('\n')
        f.write("Transiciones: \n")
        for start, transition_dict in self.transitions.items():
            for symbol, accepts in transition_dict.items():
                for accept in accepts:
                    f.write(f'{start} -> {symbol} -> {accept}')
        return (self)
    
def build_thompson(postfix_expr):
    stack = []
    state_counter = 0

    for symbol in postfix_expr:
        if symbol in (KLEENE, ALTERNATIVE, DOT):  # Operators
            if symbol == KLEENE:
                nfa = stack.pop()
                start_state = State(state_counter)
                state_counter += 1
                accept_state = State(state_counter)
                state_counter += 1
                start_state.accept = False
                accept_state.accept = True

                new_transitions = {
                    start_state: {EPSILON: {nfa.q0, accept_state}},
                    accept_state: {},
                }

                for start, transition_dict in nfa.transitions.items():
                    new_transitions[start] = {}
                    for transition_symbol, accepts in transition_dict.items():
                        new_transitions[start][transition_symbol] = set()
                        for accept in accepts:
                            new_transitions[start][transition_symbol].add(accept)
                    if start in nfa.f:
                        if EPSILON in new_transitions[start]:
                            new_transitions[start][EPSILON].add(accept_state)
                        else:
                            new_transitions[start][EPSILON] = {accept_state}
                            
                        # Add the missing transitions here
                        if EPSILON in new_transitions[start]:
                            new_transitions[start][EPSILON].add(nfa.q0)
                        else:
                            new_transitions[start][EPSILON] = {nfa.q0}

                stack.append(NFA(set(nfa.q) | {start_state, accept_state}, postfix_expr, nfa.alphabet, start_state, {accept_state}, new_transitions))
            
            elif symbol == ALTERNATIVE:
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                start_state = State(state_counter)
                state_counter += 1
                accept_state = State(state_counter)
                state_counter += 1
                start_state.accept = False
                accept_state.accept = True

                new_transitions = {
                    start_state: {EPSILON: {nfa1.q0, nfa2.q0}},
                    accept_state: {},
                }

                for nfa in [nfa1, nfa2]:
                    for start, transition_dict in nfa.transitions.items():
                        new_transitions[start] = {}
                        for transition_symbol, accepts in transition_dict.items():
                            new_transitions[start][transition_symbol] = set()
                            for accept in accepts:
                                new_transitions[start][transition_symbol].add(accept)
                        if start in nfa.f:
                            if EPSILON in new_transitions[start]:
                                new_transitions[start][EPSILON].add(accept_state)
                            else:
                                new_transitions[start][EPSILON] = {accept_state}

                stack.append(NFA(nfa1.q | nfa2.q | {start_state, accept_state}, postfix_expr, nfa1.alphabet | nfa2.alphabet, start_state, {accept_state}, new_transitions))

            elif symbol == DOT:
                nfa2 = stack.pop()
                nfa1 = stack.pop()

                new_transitions = {}

                for start, transition_dict in nfa1.transitions.items():
                    new_transitions[start] = {}
                    for transition_symbol, accepts in transition_dict.items():
                        new_transitions[start][transition_symbol] = set()
                        for accept in accepts:
                            new_transitions[start][transition_symbol].add(accept)
                    if start in nfa1.f:
                        for symbol, accepts in nfa2.transitions[nfa2.q0].items():
                            if symbol in new_transitions[start]:
                                new_transitions[start][symbol] |= accepts
                            else:
                                new_transitions[start][symbol] = set(accepts)

                for start, transition_dict in nfa2.transitions.items():
                    if start == nfa2.q0:
                        continue
                    new_transitions[start] = {}
                    for transition_symbol, accepts in transition_dict.items():
                        new_transitions[start][transition_symbol] = set()
                        for accept in accepts:
                            new_transitions[start][transition_symbol].add(accept)

                stack.append(NFA(nfa1.q | nfa2.q, postfix_expr, nfa1.alphabet | nfa2.alphabet, nfa1.q0, nfa2.f, new_transitions))

        else:  # Literal
            start_state = State(state_counter)
            state_counter += 1
            accept_state = State(state_counter)
            state_counter += 1
            start_state.accept = False
            accept_state.accept = True

            new_transitions = {
                start_state: {symbol: {accept_state}},
                accept_state: {},
            }

            stack.append(NFA({start_state, accept_state}, postfix_expr, {symbol}, start_state, {accept_state}, new_transitions))

    return stack.pop()