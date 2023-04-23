from constants import *
from typing import List, Dict
from graphviz import Digraph
from utils import *
import os.path

# node class for new tree structure
class Node:
    def __init__(self, value:str):
        self.value = value
        self.left = None
        self.right = None
        self.id = None

    def __str__(self):
        return str(self.value)
    
# tree structure class for nfa and dfa representation
class Tree:
    def __init__(self, postfix_exp: str):
        self.postfix = postfix_exp
        self.stack = []
        self.tree = None
        self.nodes = {}
        self.nullable = {}
        self.firstpos = {}
        self.lastpos = {}
        self.nextpos = {}
        self.getTree()
        if self.tree is None:
            raise ValueError("Failed to construct the expression tree. Please check the input postfix expression.")

    """
    This method generates the expression tree using a depth-first search approach.
    It calculates the nullable, firstpos, lastpos, and nextpos values for each node,
    and assigns the node's id.
    """
    def generateTree(self, node: Node, index: int = 0):
        if node is None:
            return index

        node.id = index
        self.nodes[index] = node.value

        # Calculate nullable(n), firstpos(n), and lastpos(n)
        self.calcNodes(node)

        # Check nullable dictionary
        if self.nullable.get(node.id, False):
            self.nodes[node.id] = EPSILON

        # Calculate nextpos(n)
        self.calcNextPos(node)

        index += 1

        if node.left is not None:
            index = self.generateTree(node.left, index)

        if node.right is not None:
            index = self.generateTree(node.right, index)

        return index

    """Calculate nullable, firstpos, and lastpos values for a given node."""
    def calcNodes(self, node):
        if node is None:
            return

        # Various cases are handled depending on the type of node (symbol, EPSILON, operators)
        if node.value == EPSILON:
            self.nullable[node.id] = True
            self.firstpos[node.id] = []
            self.lastpos[node.id] = []

        elif node.value in SYMBOLS:
            self.nullable[node.id] = False
            self.firstpos[node.id] = [node.id]
            self.lastpos[node.id] = [node.id]

        elif node.value == ALTERNATIVE:
            if node.left and node.right:
                self.nullable[node.id] = self.nullable.get(node.left.id, False) or self.nullable.get(node.right.id, False)
                self.firstpos[node.id] = [
                    *self.firstpos.get(node.left.id, []), *self.firstpos.get(node.right.id, [])]
                self.lastpos[node.id] = [
                    *self.lastpos.get(node.left.id, []), *self.lastpos.get(node.right.id, [])]
            else:
                self.nullable[node.id] = False
                self.firstpos[node.id] = []
                self.lastpos[node.id] = []

        elif node.value == DOT:
            self.nullable[node.id] = self.nullable.get(node.left.id, False) and self.nullable.get(node.right.id, False)
            self.firstpos[node.id] = [*self.firstpos.get(node.left.id, []), *self.firstpos.get(node.right.id, [])
                                        ] if self.nullable.get(node.left.id, False) else self.firstpos.get(node.left.id, [])
            self.lastpos[node.id] = [*self.lastpos.get(node.left.id, []), *self.lastpos.get(node.right.id, [])
                                        ] if self.nullable.get(node.right.id, False) else self.lastpos.get(node.right.id, [])

        elif node.value in [KLEENE, OPTIONAL]:
            self.nullable[node.id] = True
            self.firstpos[node.id] = self.firstpos.get(node.left.id, [])
            self.lastpos[node.id] = self.lastpos.get(node.left.id, [])


    """Calculate nextpos values for a given node."""
    def calcNextPos(self, node):

        # Calculate nextpos based on the node's value
        if node.value == DOT:
            if node.left and node.right:
                for lastpos in self.lastpos.get(node.left.id, []):
                    if lastpos in self.nextpos.keys():
                        self.nextpos[lastpos] = list(dict.fromkeys([
                            *self.nextpos[lastpos], *self.firstpos[node.right.id]]))
                    else:
                        self.nextpos[lastpos] = self.firstpos[node.right.id]
                    self.nextpos[lastpos].sort()

        elif node.value == KLEENE:
            if node.left:
                for lastpos in self.lastpos.get(node.left.id, []):
                    if lastpos in self.nextpos.keys():
                        self.nextpos[lastpos] = list(dict.fromkeys([
                            *self.nextpos[lastpos], *self.firstpos[node.left.id]]))
                    else:
                        self.nextpos[lastpos] = self.firstpos[node.left.id]
                    self.nextpos[lastpos].sort()

    """Construct the expression tree using a postfix expression.""" 
    def getTree(self):
        for c in self.postfix:
            if c in SYMBOLS:
                self.push(Node(c))
            else:
                op = Node(c)
                if c in [OPTIONAL, KLEENE]:
                    x = self.pop()
                else:
                    y = self.pop()
                    x = self.pop()
                    op.right = y
                op.left = x
                if c == '•':  
                    op.value = DOT
                self.push(op)
        self.tree = self.pop()
        self.generateTree(self.tree)

    def pop(self):
        if not self.isEmpty():
            return self.stack.pop()
        else:
            BaseException("Error")

    def push(self, op):
        self.stack.append(op)

    def isEmpty(self):
        return len(self.stack) == 0

    """Handle the tree traversal and rendering"""
    def showTable(self, file_name,node=None):
        file_path = Utils.create_file_path(file_name)
        if node is None:
            node = self.tree
            self.DOT = Digraph('Expression Tree', format='pdf')
            self.DOT.attr(rankdir='TB')
            self.DOT.attr('node', shape='circle')

        if node.left:
            left_node_name = f"{node.left.value}_{node.left.id}"
            left_node_label = ''.join(['\\\\' if c == '\\' else c for c in str(node.left.value)])
            self.DOT.node(left_node_name, left_node_label)  
            self.DOT.edge(f"{node.value}_{node.id}", left_node_name)
            self.showTable(file_name,node=node.left)

        if node.right:
            right_node_name = f"{node.right.value}_{node.right.id}"
            right_node_label = ''.join(['\\\\' if c == '\\' else c for c in str(node.right.value)])
            self.DOT.node(right_node_name, right_node_label)  
            self.DOT.edge(f"{node.value}_{node.id}", right_node_name)
            self.showTable(file_name,node=node.right)

        if node.id == self.tree.id:
            tree_node_name = f"{node.value}_{node.id}"
            tree_node_label = ''.join(['\\\\' if c == '\\' else c for c in str(node.value)])
            self.DOT.node(tree_node_name, tree_node_label)
            self.DOT.render(file_path, view=True)