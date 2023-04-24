from NFA import *
from constants import *
from tree import *
from models import *
from utils import *
import os.path



class DFAfromTree:
    def __init__(self, augmented_exp: str):
        self.augmentedExp = augmented_exp
        self.tree = None
        self.states = []
        self.alphabet = []

    def computePositions(self):
        nullable = self.tree.nullable
        firstpos = self.tree.firstpos
        lastpos = self.tree.lastpos
        followpos = {k: set(v) for k, v in self.tree.nextpos.items()}

        return nullable, firstpos, lastpos, followpos

    def buildDFADirect(self):
        self.tree = Tree(self.augmentedExp)
        # Collect the symbols from the nodes
        self.symbols = set(self.tree.nodes.values()) - set([EPSILON, KLEENE, DOT, OPTIONAL, ALTERNATIVE])

        # Calculate the DFA states and transitions
        Dstates = {}
        Dtran = {}
        start_state = frozenset(self.tree.firstpos[self.tree.tree.id])
        Dstates[start_state] = 0
        unmarked_states = [start_state]
        state_num = 1

        while unmarked_states:
            T = unmarked_states.pop()
            for a in self.symbols:
                U = set()
                for p_id in T:
                    node_value = self.tree.nodes[p_id]
                    if node_value == a:
                        U = U.union(self.followpos[p_id])
                if U:
                    U = frozenset(U)
                    if U not in Dstates:
                        Dstates[U] = state_num
                        state_num += 1
                        unmarked_states.append(U)
                    Dtran[(Dstates[T], a)] = Dstates[U]

        # Set the DFA attributes
        self.states = [s for s in Dstates]
        self.initial_state = Dstates[start_state]
        self.transitions = Dtran
        self.final_states = [Dstates[frozenset([p])] for p in self.tree.lastpos[self.tree.tree.id] if frozenset([p]) in Dstates]

        # Return the DFA
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
    
    def showDFADirect(self,file_name):
        file_path = Utils.create_file_path(file_name)
        f = open(file_path+'.txt', 'w+', encoding="utf-8")
        f.write("---------------DFA DIRECT---------------\n")
        f.write(f"States: {len(self.states)}")
        f.write('\n')
        f.write("States list:\n")
        for state in self.states:
            f.write(f"State:  {state}")
            f.write('\n')
        f.write(f"Initial State: {self.initial_state}")
        f.write('\n')
        f.write("Final States:" + str(self.final_states))
        f.write('\n')
        f.write("Transitions:\n")
        for (src, symbol), dest in self.transitions.items():
            f.write(f"  {src} --{symbol}--> {dest}")
            f.write('\n')

        return self