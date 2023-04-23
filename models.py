from typing import List, Dict
from constants import *
from utils import *

class InfixToPostfix:
    def __init__(self, regex):
        self.regex = regex
        self.postfix = []
        self.lastChar = None
        self.precedence = {
            ALTERNATIVE: 1,
            DOT: 2,
            OPTIONAL: 3,
            KLEENE: 3
        }
        self.alphabet = []
        self.stack = []
        self.alphabet = ALPHABET
        #agregamos epsilon al alfabeto
        # self.alphabet.append(EPSILON)
        self.replaceOperators()

    def __str__(self):
        return self.postfix if self.postfix else self.toPostfix()

    # Metodos para el manejo del stack 
    def isEmpty(self):
        return len(self.stack) == 0

    def last(self):
        return self.stack[-1]

    def pop(self):
        if not self.isEmpty():
            return self.stack.pop()
        else:
            BaseException("Error")

    def push(self, op):
        self.stack.append(op)

    #balanceo, aumentacion, reemplazo de operadores
    def isBalanced(self):
        stack = []
        for char in self.regex:
            if char == OPEN_PARENTESIS or char == OPEN_CORCHETE_CERRADO or char == OPEN_CORCHETE :
                stack.append(char)
            elif char == CLOSED_PARENTESIS or char == CLOSED_ORCHETE_CERRADO or char == CLOSED_CORCHETE:
                if not stack:
                    return False
                stack.pop()
        return not stack
    
    # Aumenta la expresión regular para el manejo de DFA directo
    def augmentRegex(self):
        self.regex = self.regex + '#' + DOT
        self.augmentedExp = self.regex

    # Chequea que la expresión regular no tenga errores
    def checkErrors(self):
        errors = []
        if not self.isBalanced() :
            errors.append('Error: La expresión regular no está balanceada')
        return errors

    # Reemplaza los operadores 
    def replaceOperators(self):
        # quitamos espacios
        self.regex = ''.join([c for c in self.regex if c != ' '])
        i = 0
        while i < len(self.regex):
            # Manejo de casos especiales de ?
            if self.regex[i] == OPTIONAL and self.regex[i-1] != CLOSED_PARENTESIS:
                self.regex = self.regex[:i-1] + OPEN_PARENTESIS + self.regex[i-1] + \
                    ALTERNATIVE + EPSILON + CLOSED_PARENTESIS + self.regex[i+1:]
            elif self.regex[i] == OPTIONAL and self.regex[i-1] == CLOSED_PARENTESIS:
                # Si tenemos una operacion dentro  ((a|t)?) solo convertimos ? a |ε
                if self.regex[i-3] == ALTERNATIVE:
                    self.regex = self.regex[:i] + \
                        ALTERNATIVE + EPSILON + self.regex[i+1:]
                # si solo hay un operando o una cerradura de KLEENE simple como (a)? o (a*)?
                else:
                    self.regex = self.regex[:i-1] + ALTERNATIVE + \
                        EPSILON + self.regex[i-1] + self.regex[i+1:]
            # Manejo de casos especiales de + +
            elif self.regex[i] == PLUS_OPERATOR:
                if self.regex[i-1] == CLOSED_PARENTESIS:
                    j = i - 2
                    paren_count = 1
                    while j >= 0:
                        if self.regex[j] == CLOSED_PARENTESIS:
                            paren_count += 1
                        elif self.regex[j] == OPEN_PARENTESIS:
                            paren_count -= 1
                        if paren_count == 0:
                            break
                        j -= 1
                    if j >= 0:
                        replacement = self.regex[j+1:i-1]
                        self.regex = self.regex[:j+1] + replacement + CLOSED_PARENTESIS + \
                            OPEN_PARENTESIS + replacement + CLOSED_PARENTESIS + \
                            KLEENE + self.regex[i+1:]
                        i += len(replacement) + 3
                    else:
                        raise ValueError(
                            f"Invalid use of {PLUS_OPERATOR} at position {i}")
                else:
                    self.regex = self.regex[:i] + \
                        self.regex[i-1] + KLEENE + self.regex[i+1:]
            i += 1
        # reemplazamos * por ∗ para evitar problemas con la jerarquía de operadores
        self.regex = ''.join([KLEENE if c == '∗' else c for c in self.regex])

    # Shunting Yard Algorithm
    # Evalua el token y lo agrega a postfix
    def getPrecedence(self, i):
        try:
            return self.precedence[i] <= self.precedence[self.last()]
        except:
            BaseException("Error en la precedencia")

    # Se agrega el operador al stack
    def concatOperator(self, c):
        # Si el último caracter es un operando y el actual es un operando, se agrega un operador de concatenación
        if (c in [*self.alphabet, OPEN_PARENTESIS, CLOSED_CORCHETE,OPEN_CORCHETE, OPEN_CORCHETE_CERRADO] and
                self.lastChar in [*self.alphabet, *CLOSE_LIST, OPTIONAL, KLEENE]):
            # Si el último caracter es un operando y el actual es un operando, se agrega un operador de concatenación
            if self.lastChar == KLEENE and c == KLEENE:
                self.processToken(KLEENE)
            # Agregamos el operador de concatenación
            self.processToken(DOT)

    # Se agrega a postfix hasta que haya un operador con menor jerarquía en el stack
    def processOperator(self, c):
        while (not self.isEmpty() and self.getPrecedence(c)):
            self.postfix.append(self.pop())
        self.push(c)

    # Maneja el token actual y lo agrega a postfix
    def processToken(self, c):
        # Si el token es un caracter de escape, se agrega el siguiente caracter a postfix
        if c.startswith('\\'):
            self.postfix.append(c)
            self.lastChar = c
            return
        
        # Si es algun simbolo o un ( o { o [ se extraen todos los operadores de un solo simbolo ? o *
        if c in [*self.alphabet, *OPEN_LIST]:
            while (not self.isEmpty() and self.last() in [OPTIONAL, KLEENE]):
                self.postfix.append(self.pop())
        
        # Si el token es un símbolo del alfabeto, lo agrega a la lista postfix
        if c in self.alphabet:
            self.postfix.append(c)

        # Si el token es un paréntesis de apertura, llave o corchete, lo agrega a la pila
        elif c in OPEN_LIST:
            self.push(c)

        # Si el token es un paréntesis de cierre, extrae elementos de la pila y los agrega a postfix
        # hasta que se encuentre un paréntesis de apertura en la pila
        elif c == CLOSED_PARENTESIS:
            while not self.isEmpty() and self.last() != OPEN_PARENTESIS:
                a = self.pop()
                self.postfix.append(a)
            if self.isEmpty() or self.last() != OPEN_PARENTESIS:
                BaseException("Error en el parentesis")
            else:
                self.pop()

        # Lo mismo ocurre con las llaves y los corchetes
        elif c == CLOSED_CORCHETE:
            while not self.isEmpty() and self.last() != OPEN_CORCHETE:
                a = self.pop()
                self.postfix.append(a)
            if self.isEmpty() and self.last() != OPEN_CORCHETE:
                BaseException("Error en las llaves")
            else:
                self.pop()
                self.processOperator(KLEENE)

        elif c == CLOSED_ORCHETE_CERRADO:
            while not self.isEmpty() and self.last() != OPEN_CORCHETE_CERRADO:
                a = self.pop()
                self.postfix.append(a)
            if self.isEmpty() and self.last() != OPEN_CORCHETE_CERRADO:
                BaseException("Error en el corchete")
            else:
                self.pop()
                self.processOperator(OPTIONAL)

        # Si el token es un operador ALTERNATIVE, DOT, OPTIONAL o KLEENE, llama al método processOperator
        else:
            self.processOperator(c)
        # El atributo lastChar almacena el último carácter procesado
        self.lastChar = c

    # Maneja los caracteres de escape
    def processEscapeSeq(self, i):
        if i + 1 < len(self.regex) and self.regex[i + 1] in ['t', 'n', '\\', ALTERNATIVE, 'r', 's', 'f']:
            if self.regex[i + 1] == 't':
                return '\t', i + 1
            elif self.regex[i + 1] == 'n':
                return '\n', i + 1
            elif self.regex[i + 1] == 'r':
                return '\r', i + 1
            elif self.regex[i + 1] == 's':
                return ' ', i + 1
            elif self.regex[i + 1] == 'f':
                return '\f', i + 1
            elif self.regex[i + 1] == '\\':
                return '\\\\', i + 1
            elif self.regex[i + 1] == ALTERNATIVE:
                return ALTERNATIVE, i + 1
        else:
            print(f"Unexpected character after backslash: {self.regex[i+1]}")
            raise ValueError(f"Invalid escape sequence at position {i}")



    # Se convierte la expresión regular a postfix 
    # Se utiliza el algoritmo de Shunting Yard
    def toPostfix(self):
        self.lastChar = None
        i = 0
        while i < len(self.regex):
            c = self.regex[i]
            # Manejo de caracteres de escape
            if c == '\\':
                c, i = self.processEscapeSeq(i)
            self.concatOperator(c)
            self.processToken(c)
            i += 1

        # Se extraen todos los operadores de la pila y se agregan a postfix
        while not self.isEmpty():
            self.postfix.append(self.pop())
        self.postfix = ''.join(self.postfix)
        return self.postfix