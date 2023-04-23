from constants import *
from NFA import *
from DFA import *
from models import *
from LEXER import *
from DFA_DIRECT import *
from utils import Grapher
import uuid

def testNFA():
    # r = ("a(a?b*|c+)b|baa")
    file_name = str(uuid.uuid4().fields[-1])[:5]
    r = ('(x|t)+((a|m)?)+')
    postfixExp = InfixToPostfix(r)
    postfixExp.replaceOperators() 
    postfixExp.toPostfix()
    print("Format expression: ", postfixExp.regex)
    print("Postfix expression: ", postfixExp.postfix)
    ########## NFA ##########
    nfaBuilt = thompsonBuild(postfixExp.postfix)
    nfaBuilt.showNFA(file_name)
    Grapher.drawNFA(nfaBuilt,file_name)
    
#testNFA()

# testNFA()
# drawMinDFASubsets
def testDFASubsets():
    file_name = str(uuid.uuid4().fields[-1])[:5]
    r = ("0? (1? )? 0 ∗")
    postfixExp = InfixToPostfix(r)
    postfixExp.replaceOperators() 
    postfixExp.toPostfix()
    thompson = thompsonBuild(postfixExp.postfix)
    dfa = DFASubsets(thompson)
    newAFD = dfa.buildDFASubsets()
    print("postfix: ", postfixExp.postfix)
    newAFD.showSubsetDFA(file_name)
    Grapher.drawSubsetDFA(newAFD,file_name)

#testDFASubsets()

# subsets minimzed
def testHoffman():
    file_name = str(uuid.uuid4().fields[-1])[:5]
    file_name = file_name+'_min'
    #r = ("(a|b)*a(a|b)(a|b)")
    r = ("0? (1? )? 0 ∗")
    print('min')
    postfixExp = InfixToPostfix(r)
    postfixExp.replaceOperators() 
    postfixExp.toPostfix()
    nfa = thompsonBuild(postfixExp.postfix)
    dfa_subsets = DFASubsets(nfa)
    dfa_subsets.buildDFASubsets()
    dfa_subsets.minimizeSubsetAFD()
    dfa_subsets.showMinimized(file_name)
    Grapher.drawSubsetDFA(dfa_subsets,file_name)

#testHoffman()

def testTree():
    file_name = str(uuid.uuid4().fields[-1])[:5]
    r = ("(a|b)*(b|a)*abb")
    postfixExp = InfixToPostfix(r)
    augmented_exp = postfixExp.augmentRegex()
    
    direct = DFAfromTree(augmented_exp)
    newAFD = direct.buildDFADirect()
    newAFD.showDFADirect(file_name)
    
    Grapher.drawDirectDFA(newAFD,file_name)


#testTree()

# yalex
def testYalex():
    file_name = str(uuid.uuid4().fields[-1])[:5]
    yalexFile = "slr-4.yal"
    yalex = Lexer(yalexFile)
    individualRules = yalex.getIndividualRules()
    print("individualRules: ", individualRules)
    print()
    finalExp = yalex.getFinalExp()
    operators = yalex.getOperators()
    print("expression----")
    print(repr(finalExp))
    print()
    print("operators in use: ")
    print(operators)
    print()
    postfixExp = InfixToPostfix(finalExp)
    postfixExp.toPostfix()
    print("postfixExp----")
    print(repr(postfixExp.postfix))
    print()

    tree = Tree(postfixExp.postfix)
    tree.generateTree(tree.tree)
    tree.showTable(file_name)

testYalex()