import sys
from constants import *
from create_scanner import *
from DFA import *
from utils import Utils
import re

def read_file(file_name):
   with open(YALEX_TEST + file_name, 'r') as file:
       lines = file.readlines()
       for line in lines:
           line = re.findall(r'\S+', line)
           
           for char in line:
               for key in operators:
                   if key in rules:
                       key = 'digits' if key == 'number' else key
                       regex = rules[key]
                       postfixExp = Convert_Infix_Postfix(regex)
                       postfixExp.toPostfix()
                       try:
                           thompson = build_thompson(postfixExp.postfix)
                           dfa = DFASubsets(thompson)
                           newAFD = dfa.create_DFASubset()
                           simulated = newAFD.simulate(char)
                           if simulated: print(char,' ',operators[key])
                           else:
                               pass
                               #print(char,' not found :(')
                       except:
                           pass
                           #print( str(key) + ' regex failed')
                           
                   else:
                       if char == key: print(char,' ',operators[key])
                    


rules = {
    "delim": "( |\t|\n)",
    "ws": "( |\t|\n)+",
    "letter": "(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)",
    "str": "(_)*",
    "digit": "(0|1|2|3|4|5|6|7|8|9)",
    "digits": "(0|1|2|3|4|5|6|7|8|9)+",
    "id": "(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)((A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)|(_)*|(0|1|2|3|4|5|6|7|8|9))*",
    "number": "(0|1|2|3|4|5|6|7|8|9)+(.(0|1|2|3|4|5|6|7|8|9)+)?(E(+|-)?(0|1|2|3|4|5|6|7|8|9)+)?"
}
operators = {
    "ws": "None",
    "id": "ID",
    "number": "NUMBER",
    ";": "SEMICOLON",
    ":=": "ASSIGNOP",
    "<": "LT",
    "=": "EQ",
    "+": "PLUS",
    "-": "MINUS",
    "*": "TIMES",
    "/": "DIV",
    "(": "LPAREN",
    ")": "RPAREN"
}
regex = '(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)((A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)|(_)*|(0|1|2|3|4|5|6|7|8|9))*|(0|1|2|3|4|5|6|7|8|9)+|=|<|;|/'
postfixExp = Convert_Infix_Postfix(regex)
postfixExp.toPostfix()
thompson = build_thompson(postfixExp.postfix)
dfa = DFASubsets(thompson)
newAFD = dfa.create_DFASubset()
#Utils.simulate_exp(newAFD)

# Get the command line arguments
args = sys.argv
if len(args) < 2:
   print('Please provide the file in the command line')
   sys.exit()
else:
   read_file(args[-1])
