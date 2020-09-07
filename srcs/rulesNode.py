from npiParser import infixToPostfix
from stack import Stack
from factNode import FactNode


oper = {
    "+": lambda a,b : a and b,
    "|": lambda a,b : a or b,
    "^": lambda a,b : a ^ b,
    "!": lambda a,b : False
}


class Rule:
    def __init__(self, leftRule:str, rightRule:str):
        self.output = Stack()
        infixToPostfix(list(leftRule), self.output)
        self.leftRule = {}
        self.rightRule = {}
        self.visited = False
        self.strLeftRule = leftRule
        self.strRightRule = rightRule
    

    def computeRule(self, to_compute:list):
        stack = []
        for token in self.output.stack:
            if token == '!':
                prec = stack.pop()
                prec.value = not prec.value
                stack.append(prec)
            elif token.isalpha():
                stack.append(self.leftRule[token])
            else:
                fact2 = stack.pop()
                fact1 = stack.pop()
                tmp = FactNode("tmp", oper[token](fact1.value, fact2.value))
                if token == '+' and fact1.isFixed and fact2.isFixed:
                    tmp.isFixed = True
                elif token == '|' and (fact1.isFixed or fact2.isFixed):
                    tmp.isFixed = True
                stack.append(tmp)
        ret = stack.pop()
        return ret.value, ret.isFixed


    def fillRule(self, rule, factsList):
        tmp = Stack()
        infixToPostfix(list(rule), tmp)
        toFill = {}
        for token in tmp.stack:
            if token in factsList:
                toFill[token] = factsList[token]
        return toFill

