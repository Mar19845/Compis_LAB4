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
from create_scanner import *
import json

def int_to_string(char):
    if isinstance(char, int):
        return str(char)
    return char

# (a|b)*(b|a)*abb
flag = True
while flag:
    
    print("1. Thompson Algorithm\n2. AFD Subconjuntos\n3. AFD Directo\n4. Yalex\n5. Create Scanner.py\n6. Exit")
    opc=input("Choose an option: ")
    
    if opc == "6":
        print("By")
        flag = False
    elif opc == "1":
        file_name = Utils.create_filename()
        postfix_exp = Utils.get_infix_expression()
        if postfix_exp is not False:
            nfaBuilt = build_thompson(postfix_exp.postfix)
            nfaBuilt.showNFA(file_name)
            Grapher.drawNFA(nfaBuilt,file_name)
            Utils.simulate_exp(nfaBuilt)
    
    elif opc == "2":
        file_name = Utils.create_filename()
        postfix_exp = Utils.get_infix_expression()
        if postfix_exp is not False:
            nfaBuilt = build_thompson(postfix_exp.postfix)
            dfa = DFASubsets(nfaBuilt)
            newAFD = dfa.create_DFASubset()
            newAFD.showDFASubset(file_name)
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
        postfixExp = Convert_Infix_Postfix(finalExp)
        postfixExp.toPostfix()
        tree = Tree(postfixExp.postfix)
        tree.generateTree(tree.tree)
        tree.create_tree_table(file_name)
    
    elif opc == "5":
        file_name = Utils.create_filename()
        file = input("Input the file name without of the .yal in the folder Yalex: ")
        file = file + ".yal"
        yalex = Lexer(file)
        
        # get rules and ops
        individualRules = yalex.getIndividualRules()
        operators = yalex.getOperators()
        regex = ""
        for key in operators.keys():
            if key != 'ws': 
                if key in individualRules:
                    regex += individualRules[key] + "|"
        #regex = individualRules['id'] + "|" + individualRules['digits'] + "|" + "=" + "|" + "<" + "|" + ";" + "|" + "/" 
        postfixExp = Convert_Infix_Postfix(regex)
        postfixExp.toPostfix()
        
        json_rules = json.dumps(individualRules, indent=4,
                            ensure_ascii=False,default=int_to_string)
    
        json_operators = json.dumps(operators, indent=4,ensure_ascii=False)
        test = 'a1 + a2'
        list_of_lines = []
        list_of_lines.append(f"rules = {json_rules}\n")
        list_of_lines.append(f"operators = {json_operators}\n")
        list_of_lines.append(f"regex = {repr(regex)}\n")
        
        list_of_lines.append(f"postfixExp = Convert_Infix_Postfix(regex)\npostfixExp.toPostfix()\nthompson = build_thompson(postfixExp.postfix)\ndfa = DFASubsets(thompson)\nnewAFD = dfa.create_DFASubset()\n#Utils.simulate_exp(newAFD)\n")
        #funct_reader =
        
        create_scanner_file("scanner.py",list_of_lines)
    elif opc !="":
      print("\nWrong option")
    else:
        break