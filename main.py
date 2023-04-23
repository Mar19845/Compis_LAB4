from utils import Utils,Grapher
import re
from models import *
from constants import *
from NFA import *
from DFA import *
from DFA_DIRECT import *
from LEXER import *
import uuid
import sys

# (a|b)*(b|a)*abb
flag = True
while flag:
    
    print("1. Thompson Algorithm\n2. AFD Subconjuntos\n3. AFD Directo\n4. Yalex\n5. Exit")
    opc=input("Choose an option: ")
    
    if opc == "5":
        print("By")
        flag = False
    elif opc == "1":
        file_name = Utils.create_filename()
        postfix_exp = Utils.get_infix_expression()
        if postfix_exp is not False:
            nfaBuilt = thompsonBuild(postfix_exp.postfix)
            nfaBuilt.showNFA(file_name)
            Grapher.drawNFA(nfaBuilt,file_name)
            Utils.simulate_exp(nfaBuilt)
    
    elif opc == "2":
        file_name = Utils.create_filename()
        postfix_exp = Utils.get_infix_expression()
        if postfix_exp is not False:
            nfaBuilt = thompsonBuild(postfix_exp.postfix)
            dfa = DFASubsets(nfaBuilt)
            newAFD = dfa.buildDFASubsets()
            newAFD.showSubsetDFA(file_name)
            Grapher.drawSubsetDFA(newAFD,file_name)
            Utils.simulate_exp(newAFD)
    elif opc == "3":
        file_name = Utils.create_filename()
        postfix_exp = Utils.get_infix_expression()
        if postfix_exp is not False:
            augmented_exp = postfix_exp.augmentRegex()
            direct = DFAfromTree(augmented_exp)
            newAFD = direct.buildDFADirect()
            newAFD.showDFADirect(file_name)
            Grapher.drawDirectDFA(newAFD,file_name)
            Utils.simulate_exp(newAFD)
    elif opc == "4":
        file_name = Utils.create_filename()
        file = input("Input the file name without of the .yal in the folder Yalex: ")
        file = file + ".yal"
        yalex = Lexer(file)
        # add the yalex to txt 
        finalExp = yalex.getFinalExp()
        postfixExp = InfixToPostfix(finalExp)
        postfixExp.toPostfix()
        tree = Tree(postfixExp.postfix)
        tree.generateTree(tree.tree)
        tree.showTable(file_name)
        
    elif opc !="":
      print("\nWrong option")
    else:
        break