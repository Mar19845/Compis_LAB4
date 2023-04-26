import re
from graphviz import Digraph
import collections
from models import *
from constants import *
import os.path
import uuid


class Utils():
    @staticmethod
    def create_file_path(file_name):
        file_path = os.path.join(DIRECTORY, file_name)
        if not os.path.isdir(DIRECTORY):
            os.mkdir(DIRECTORY)
        return file_path
    
    @staticmethod
    def get_infix_expression():
        expression = input('Enter infix expression: ')
        #expression = expression.replace('ε','ε')
        errors = Convert_Infix_Postfix(expression).checkErrors()
        if errors:
            print(errors)
            return False
        
        postfix_exp = Convert_Infix_Postfix(expression)
        postfix_exp.replaceOperators()
        postfix_exp.toPostfix()
        print("Postfix expression: ", postfix_exp)
        return postfix_exp
    
    @staticmethod
    def create_filename():
        return str(uuid.uuid4().fields[-1])[:5]
    
    @staticmethod
    def simulate_exp(object_to_sim):
        simulation_flag = True
        while simulation_flag:
            exp = input("Type exp to simulate or type break to leave: ")
            if  exp.lower() =="break":
                print("By\n")
                simulation_flag = False
            else:
                simulation = object_to_sim.simulate(exp)
                if simulation:
                    print("The expression "+ str(exp)+" is accepted\n")
                else:
                    print("The expression "+ str(exp)+" is not accepted\n")
    
    @staticmethod
    def clean_yalex_files(yales_files):
        yales_files = [name.replace(".\\","") for name in yales_files]
        return yales_files
    
class Grapher():
    def drawNFA(nfa,file_name):
        file_path = Utils.create_file_path(file_name)
        # Create a new directed graph
        dot = Digraph(comment='NFA')

        # Set the graph attributes
        dot.attr(rankdir='LR')
        
        # Add states only when there is a transition involving them
        added_states = set()
        for start, transition_dict in nfa.transitions.items():
            for symbol, accepts in transition_dict.items():
                for accept in accepts:
                    if start not in added_states:
                        if start == nfa.q0:
                            dot.attr('node', shape='ellipse')
                        elif start in nfa.f:
                            dot.attr('node', shape='doublecircle', style='bold')
                        else:
                            dot.attr('node', shape='circle', style='', fillcolor='')
                        dot.node(str(start))
                        added_states.add(start)
                    
                    if accept not in added_states:
                        if accept in nfa.f:
                            dot.attr('node', shape='doublecircle', style='bold')
                        else:
                            dot.attr('node', shape='circle', style='', fillcolor='')
                        dot.node(str(accept))
                        added_states.add(accept)

                    dot.edge(str(start), str(accept), label=symbol)

        # Render the graph
        dot.format = 'png'
        dot.render(file_path, view=True)

    def drawSubsetDFA(dfa,file_name):
        file_path = Utils.create_file_path(file_name)
        # Create a new directed graph
        dot = Digraph('Subset-DFA', format='png')
        dot.attr(rankdir='LR')

        state_id_mapping = {state: i for i, state in enumerate(dfa.states)}

        # Add the initial state with a special shape and color
        initial_state_id = state_id_mapping[dfa.initial_state]
        if initial_state_id in dfa.final_states:
            dot.node(str(initial_state_id), shape='ellipse', style='bold')
        else:
            dot.node(str(initial_state_id), shape='ellipse')
        dot.node('fake', style='invisible')
        dot.edge('fake', str(initial_state_id), style='bold')

        # Add the final states with a double circle shape
        for final_state in dfa.final_states:
            final_state_id = state_id_mapping[final_state]
            dot.node(str(final_state_id), shape='doublecircle')

        # Add the non-final states
        for state in dfa.states:
            state_id = state_id_mapping[state]
            if state not in dfa.final_states and state != dfa.initial_state:
                dot.node(str(state_id), shape='circle')

        # Add the transitions
        for (start_state, symbol), end_state in dfa.transitions.items():
            start_state_id = state_id_mapping[start_state]
            end_state_id = state_id_mapping[end_state]
            dot.edge(str(start_state_id), str(end_state_id), label=symbol)

        # Render the graph
        dot.render(file_path, view=True)

        return dot

    def drawDirectDFA(dfa,file_name):
        file_path = Utils.create_file_path(file_name)
        # Create a new directed graph
        dot = Digraph('Direct-DFA', format='png')
        dot.attr(rankdir='LR')

        state_id_mapping = {state: i for i, state in enumerate(dfa.states)}
        
        # Add the initial state with a special shape and color
        initial_state_id = state_id_mapping[frozenset({dfa.initial_state})]
        if initial_state_id in dfa.final_states:
            dot.node(str(initial_state_id), shape='ellipse', style='bold')
        else:
            dot.node(str(initial_state_id), shape='ellipse')
        dot.node('fake', style='invisible')
        dot.edge('fake', str(initial_state_id), style='bold')

        # Add the final states with a double circle shape
        for final_state in dfa.final_states:
            final_state_id = state_id_mapping[frozenset({final_state})]
            dot.node(str(final_state_id), shape='doublecircle')

        # Add the non-final states
        for state in dfa.states:
            state_id = state_id_mapping[state]
            if state not in dfa.final_states and state != dfa.initial_state:
                dot.node(str(state_id), shape='circle')

        # Add the transitions
        for (start_state, symbol), end_state in dfa.transitions.items():
            start_state_id = state_id_mapping[start_state]
            end_state_id = state_id_mapping[end_state]
            dot.edge(str(start_state_id), str(end_state_id), label=symbol)

        # Render the graph
        dot.render(file_path, view=True)

        return dot