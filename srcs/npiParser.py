import re
from stack import Stack


operator = {
    "(": 6,
    "!": 5,
    "+": 4,
    "|": 3,
    "^": 2,
    "=>":1
}


def isFact(token):
    return re.match("[A-Z]", token)


def topGreaterPrecedence(top_op, op):
    return operator[top_op] > operator[op]


def topEqualPrecedence(top_op, op):
    return operator[top_op] == operator[op]


def isLeftParenthesis(token):
    return token == '('


def isRightParenthesis(token):
    return token == ')'


def infixToPostfix(rule, output):
    operatorsStack = Stack()
    for token in rule:
        if isFact(token):
            output.push(token)
        elif token in operator:
            top_op = operatorsStack.peek()
            while operatorsStack.isEmpty() == False and (topGreaterPrecedence(top_op, token) or topEqualPrecedence(top_op, token)) and not isLeftParenthesis(top_op):
                output.push(operatorsStack.pop())
            operatorsStack.push(token)
        elif isLeftParenthesis(token):
            operatorsStack.push(token)
        elif isRightParenthesis(token):
            while not isLeftParenthesis(operatorsStack.peek()) and operatorsStack.isEmpty() == False:
                output.push(operatorsStack.pop())
            if isLeftParenthesis(operatorsStack.peek()):
                operatorsStack.pop()
            else:
                exit("Mismatched parenthesis")
    while operatorsStack.isEmpty() == False:
        if isLeftParenthesis(operatorsStack.peek()) or isRightParenthesis(operatorsStack.peek()):
            exit("Mismatched parenthesis")
        output.push(operatorsStack.pop())
