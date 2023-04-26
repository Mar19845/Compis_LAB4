from constants import *

class Lexer:
    def __init__(self, file):
        self.file = file
        self.rules = {}
        self.individual_rules = {}
        self.operators = set()
        self.convertYalex()

    """Returns the YALex specification file"""
    def convertYalex(self):
        self.extractRules()
        self.buildIndividualRules()
        self.buildRegexnOper()

    def extractRules(self):
        with open(YALEX_DIRECTORY + self.file, "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("let"):
                    ruleName, ruleBody = self.getRule(line)
                    reRule = self.convertRegex(ruleBody)
                    self.rules[ruleName] = reRule

    def buildIndividualRules(self):
        for ruleName, reRule in self.rules.items():
            updateRule = self.replaceRules(reRule)
            expanded_rule = self.handleChars(updateRule)
            self.individual_rules[ruleName] = expanded_rule

    def buildRegexnOper(self):
        self.regex = self.buildRegex()
        self.final_expression = self.handleChars(self.regex)

    def buildRegex(self):
        regex = ""
        operators = set()
        in_rule_tokens = False
        operator_rules = {} 
        rules_tokes = {} 

        with open(YALEX_DIRECTORY + self.file, "r") as file:
            lines = file.readlines()
            for line in lines:
                # Remove leading and trailing whitespaces
                start_index = 0
                end_index = len(line) - 1

                while start_index < len(line) and line[start_index] in (" ", "\t"):
                    start_index += 1

                while end_index >= 0 and line[end_index] in (" ", "\t"):
                    end_index -= 1

                line = line[start_index:end_index + 1]

                if len(line) >= len(COMMENT_START1) and len(line) >= len(COMMENT_END1) and line[:len(COMMENT_START1)] == COMMENT_START1 and line[-len(COMMENT_END1):] == COMMENT_END1:
                    continue
                if len(line) >= len(COMMENT_START2) and len(line) >= len(COMMENT_END2) and line[:len(COMMENT_START2)] == COMMENT_START2 and line[-len(COMMENT_END2):] == COMMENT_END2:
                    continue
                
                if line.startswith("rule tokens".lower()):
                    #print(line)
                    in_rule_tokens = True
                    # when reading the rule tokens, if 'id' is found, replace it with the regex for an identifier
                    if 'id' in self.individual_rules:
                        operator_rules['id'] = self.individual_rules['id']

                    # when reading the rule tokens, if 'ws' is found, replace it with the regex for whitespace
                    if 'ws' in self.individual_rules:
                        operator_rules['ws'] = self.individual_rules['ws']

                    # when reading the rule tokens, if 'digit' is found, replace it with the regex for a number
                    if 'digit' in self.individual_rules:
                        operator_rules['digit'] = self.individual_rules['digit']

                    # when reading the rule tokens, if 'letter' is found, replace it with the regex for a letter
                    if 'letter' in self.individual_rules:
                        operator_rules['letter'] = self.individual_rules['letter']

                    # when reading the rule tokens, if an operator is found, replace it with the regex for that operator
                    if 'operators' in self.individual_rules:
                        operator_rules['operators'] = self.individual_rules['operators']

                elif in_rule_tokens:
                    # case after reading the rule tokens string
                    operator_line = line.lstrip()
                    #print(operator_line)
                    if operator_line.startswith(ALTERNATIVE):
                        # if line starts with | then drop it
                        operator_line = operator_line[1:]
                        #print(operator_line)
                        # while first char in line is space or  \t then drop it
                        while operator_line[0] in (' ', '\t'):
                            operator_line = operator_line[1:]
                            #print(operator_line.rstrip())
                        operator_line = operator_line.rstrip()

                    else:
                        operator_line  = operator_line.rstrip()

                    #print(operator_line)
                    operator_line_list = operator_line.split(' ')
                    
                    if operator_line.find(OPEN_CORCHETE) and operator_line.find(CLOSED_CORCHETE):
                        # get index of { and } in string
                        OPEN_CORCHETE_index = operator_line.find(OPEN_CORCHETE)
                        CLOSED_CORCHETE_index = operator_line.find(CLOSED_CORCHETE)
                        
                        # if indexes are found then 
                        if OPEN_CORCHETE_index > 0 and CLOSED_CORCHETE_index > 0:
                            # sumns len of yal return + 2 spaces
                            OPEN_CORCHETE_index += len(TOKEN_RETURN) + 2
                            
                            # get the real return value and delete blanks spaces
                            values_token = operator_line[OPEN_CORCHETE_index:CLOSED_CORCHETE_index].lstrip().rstrip()
                        else:
                            # if indexes are not found in operator line the return None
                            values_token = 'None'
                    
                    
                    
                    operator = ''
                    for c in operator_line:
                        if c in (' ', '\t'):
                            break
                        operator += c
                    # esta malo pero no se como hacerlo bien sin quemarlo
                    # replace ' and " in operator
                    operator = operator.replace("'","")
                    operator = operator.replace('"','')
                    #print(operator)
                    if operator:
                        if operator not in rules_tokes:
                            rules_tokes[operator] = values_token
                        #print(operator,values_token)
                        operators.add(operator)

                    rule_name = ""
                    for c in operator_line[len(operator):]:
                        if c == " ":
                            continue
                        rule_name += c

                    if rule_name.strip() in self.individual_rules:
                        operator_rules[operator] = self.individual_rules[rule_name.strip()]

                    if operator_line.startswith("let") or operator_line.startswith("rule"):
                        in_rule_tokens = False
                elif not in_rule_tokens:
                    continue

        self.operators = operators
        self.rules_tokes = rules_tokes

        for operator, reRule in operator_rules.items():
            #print(operator,reRule,'\n')
            regex += reRule + "|"
        #print(operator_rules.keys())
        #print(regex)
        return regex[:-1]

    """Extracts a rule name and rule body from a line in the YALex specification"""
    def getRule(self, line):
        partition_index = -1
        for i, c in enumerate(line):
            if c == '=':
                partition_index = i
                break
        
        #print(line[4: partition_index],line[partition_index + 1:])
        ruleName = self.removeSpaces(line[4: partition_index])
        ruleBody = self.removeSpaces(line[partition_index + 1:])
        #ruleBody = ruleBody.replace('E',EPSILON)
        #print(ruleName,ruleBody)
        # Returns a tuple containing the rule name and rule body.
        return ruleName, ruleBody

    """Removes whitespace characters from a string"""
    def removeSpaces(self, s):
        result = ""
        in_single_quotes = False
        in_double_quotes = False
        escape_next = False
        for c in s:
            if c == "\\" and not escape_next:
                escape_next = True
                result += c
                continue

            if escape_next:
                escape_next = False
                result += c
                continue

            if c == "'":
                in_single_quotes = not in_single_quotes
            if c == '"':
                in_double_quotes = not in_double_quotes
            if not c.isspace() or in_single_quotes or in_double_quotes:
                if c != "'":
                    result += c
        
        return result

    """Expands character ranges in a regular expression"""
    def expandExp(self, expression):
        expanded = []
        i = 0
        
        while i < len(expression):
            if expression[i] == '\\':
                if expression[i+1] == 't':
                    expanded.append(f'\t')
                elif expression[i+1] == 'n':
                    expanded.append(f'\n')
                else:
                    expanded.append(expression[i:i+2])
                i += 2
            elif i + 2 < len(expression) and expression[i + 1] == '-':
                start_char = expression[i]
                end_char = expression[i + 2]
                if (start_char.isupper() and end_char.isupper()) or (start_char.islower() and end_char.islower()) or (start_char.isdigit() and end_char.isdigit()):
                    for char_code in range(ord(start_char), ord(end_char) + 1):
                        expanded.append(chr(char_code))
                else:
                    expanded.append(expression[i])
                i += 3
            else:
                expanded.append(expression[i])
                i += 1
        return expanded

    """Converts character class notation to regular expression notation in a rule body"""
    def handleChars(self, rule_body):
        result = ""
        i = 0
        
        while i < len(rule_body):
            #print(rule_body[i])
            if rule_body[i] == '\\':
                if rule_body[i+1] == 't':
                    result += f'\\t'
                elif rule_body[i+1] == 'n':
                    result += f'\\n'
                elif rule_body[i+1] == 's':
                    result += f'\\s'
                else:
                    result += '\\\\' + rule_body[i+1]
                i += 2
            elif rule_body[i] == OPEN_CORCHETE_CERRADO:
                i += 1
                inside_brackets = ""
                while rule_body[i] != CLOSED_ORCHETE_CERRADO:
                    inside_brackets += rule_body[i]
                    i += 1
                expanded_exp = self.expandExp(inside_brackets)
                result += OPEN_PARENTESIS + ALTERNATIVE.join(expanded_exp) + CLOSED_PARENTESIS
                i += 1
            else:
                result += rule_body[i]
                i += 1
        return result


    """Replaces rule names in a regular expression with their corresponding regular expressions"""
    def replaceRules(self, reRule):
        sorted_rule_names = sorted(self.rules.keys(), key=len, reverse=True)
        for ruleName in sorted_rule_names:
            ruleBody = self.rules[ruleName]
            updateRule = ""
            i = 0
            while i < len(reRule):
                found = False
                if reRule[i:].startswith(ruleName):
                    next_char = reRule[i + len(ruleName):i + len(ruleName) + 1]
                    if not next_char or not (next_char.isalnum() or next_char == '_'):
                        found = True
                        if reRule[i + len(ruleName):].startswith("†"):
                            if ruleBody.startswith(OPEN_PARENTESIS) and ruleBody.endswith(CLOSED_PARENTESIS):
                                updateRule += f"{ruleBody}†"
                            else:
                                updateRule += f"({ruleBody})†"
                            i += len(ruleName) + 1
                        else:
                            updateRule += ruleBody
                            i += len(ruleName)
                if not found:
                    updateRule += reRule[i]
                    i += 1
            reRule = updateRule
        return reRule

    """Converts a rule body in the YALex specification to a regular expression"""
    def convertRegex(self, ruleBody):
        # Rule body defined in YALex specification
        ruleBody = self.handleChars(ruleBody)
        #print(ruleBody)
        reRule = self.replaceRules(ruleBody)

        # Expand expressions after replacing the rules
        expanded_rule = ""
        i = 0
        while i < len(reRule):
            if reRule[i] == '\\':
                expanded_rule += reRule[i:i+2]
                i += 2
            elif reRule[i] == OPEN_CORCHETE_CERRADO:
                i += 1
                inside_brackets = ""
                while reRule[i] != CLOSED_ORCHETE_CERRADO:
                    inside_brackets += reRule[i]
                    i += 1
                expanded_exp = self.expandExp(inside_brackets)
                expanded_rule += ALTERNATIVE.join(expanded_exp)
                i += 1
            else:
                expanded_rule += reRule[i]
                i += 1

        return expanded_rule

    """ Get methods for the class"""
    def getFinalExp(self):
        return self.final_expression

    def getIndividualRules(self):
        return self.individual_rules

    # def getExpandedRules(self):
    #     return self.expanded_rules

    def getOperators(self):
        #return self.operators
        return self.rules_tokes