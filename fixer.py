from DFA import DFASubsets
from NFA import *

def push(stack, op):
    stack.append(op)


def pop(stack):
    if not isEmpty(stack):
        return stack.pop()
    else:
        BaseException("Error")
        

def last(stack):
    return stack[-1]


def isEmpty(stack):
    return len(stack) == 0


def replace_string(string, char, replace):
    result = ''
    for x in string:
        if x == char:
            result += replace
        else:
            result += x
    return result

def getMatches(postfix, string):
    #procesar la expresion regular
    postfix.checkErrors()
    postfix.replaceOperators()
    print("Processed regex: ", postfix.regex)
    postfix.toPostfix()
    print("Postfix expression: ", postfix.postfix)
    #construir el AFN primero para hacer luego AFD con subsets
    print('asdasdas')
    thompson = thompsonBuild(postfix.postfix)
    dfa = DFASubsets(thompson)
    newDFA = dfa.buildDFASubsets()
    matches = []
    #recorrer el string y buscar matches
    simulation = newDFA.simulate(string)
    if simulation:
        matches.append(string)
    return matches
'''

def thompsonBuild(postfix_expr):
    stack = []
    state_counter = 0
    prev_concat = False

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
                if prev_concat:
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
                    stack.append(NFA(nfa1.q | nfa2.q | {start_state, accept_state}, postfix_expr, nfa1.alphabet | nfa2.alphabet, start_state, {accept_state}, new_transitions))

                else:
                    nfa2 = stack.pop()
                    nfa1 = stack.pop()

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

                prev_concat = False

            elif symbol == DOT:
                prev_concat = True
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
            if symbol == ' ':  # Handling space character
                symbol = ' '
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
'''