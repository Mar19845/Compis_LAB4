from constants import *


'''
def read_file(file_name):
    with open(YALEX_TEST + file_name, "r") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            print(repr(line))
        print(lines)
'''      
            
def create_scanner_file(file_name,list_of_lines):
    func_name = 'read_file' #replace print for the actual function
    with open(file_name, "w", encoding='utf-8') as file:
        file.write(f"import sys\nfrom constants import *\nfrom create_scanner import *\n")
        file.write(f"from DFA import *\n")
        file.write(f"from utils import Utils\n")
        file.write(f"import re\n")
        file.write(f"\n")
        
        file.write(f"def read_file(file_name):\n")
        file.write(f"   with open(YALEX_TEST + file_name, 'r') as file:\n")
        file.write(f"       lines = file.readlines()\n")
        file.write(f"       for line in lines:\n")
        file.write(f"           line = re.findall(r'\S+', line)\n")
        file.write(f"           for char in line:\n")
        file.write(f"               for key in operators:\n")
        file.write(f"                   if key in rules:\n")
        file.write(f"                       key = 'digits' if key == 'number' else key\n")
        file.write(f"                       regex = rules[key]\n")
        file.write(f"                       postfixExp = Convert_Infix_Postfix(regex)\n")
        file.write(f"                       postfixExp.toPostfix()\n")
        file.write(f"                       try:\n")
        file.write(f"                           thompson = build_thompson(postfixExp.postfix)\n")
        file.write(f"                           dfa = DFASubsets(thompson)\n")
        file.write(f"                           newAFD = dfa.create_DFASubset()\n")
        file.write(f"                           simulated = newAFD.simulate(char)\n")
        file.write(f"                           if simulated: print(char,' ',operators[key])\n")
        file.write(f"                           else:\n")
        file.write(f"                               pass\n")
        file.write(f"                               #print(char,' not found :(')\n")
        file.write(f"                       except:\n")
        file.write(f"                           pass\n")
        file.write(f"                           #print( str(key) + ' regex failed')\n")
        file.write(f"                   else:\n")
        file.write(f"                       if char == key: print(char,' ',operators[key])\n")
        
        file.write(f"\n")
        for line in list_of_lines:
            file.write(line)
        file.write(f"\n")
        
        file.write(f"# Get the command line arguments\nargs = sys.argv\n")
        file.write(f"if len(args) < 2:\n")
        file.write(f"   print('Please provide the file in the command line')\n   sys.exit()\n")
        file.write(f"else:\n   {func_name}(args[-1])\n")
    print('Created scanner file')
    
