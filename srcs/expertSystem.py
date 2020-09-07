import sys
import re
from factNode import FactNode
from rulesNode import Rule


factsList = {}
queries = {}
rulesList = []


def removeComment(line):
    if line.find('#') != -1:
        start = len(line) - (len(line) - line.find('#'))
        line = line[:start]
    line = line.replace(" ", "")
    line = line.replace("\t", "")
    line = line.replace("\n", "")
    return line


def checkSyntax(val):
    i = 0
    if len(val) <= 0:
        return False
    while i < len(val):
        if val[i] == '(' or val[i] == ')':
            i +=1
            continue
        if val[i] == '!':
            i += 1
        if not val[i].isalpha():
            return False
        if i + 1 >= len(val):
            return True
        if val[i + 1] == '(' or val[i + 1] == ')':
            i += 1
        if i + 1 < len(val) and not re.match(r"(\+|\||\^|\!)", val[i + 1]):
            return False
        i += 2
    return True


def getRules(line, count):
    if line.find("=>") == -1:
        if not line.startswith('?') and not line.startswith('='):
            print("Error: Malformatted file.")
            print(f"       Line: {count}: {line}")
            exit()
        return
    try:
        left, right = line.split('>')
        left = left.replace('=', '')
    except ValueError:
        print("Error: Syntax error.")
        print(f"       Line: {count}: {line}")
        exit()
    if len(left) == 0 or len(right) == 0:
        print("Error: Syntax error.")
        print(f"       Line: {count}: {line}")
        exit()
    left = left.upper()
    right = right.upper()
    if not checkSyntax(left) or not checkSyntax(right):
        print("Error: Syntax error.")
        print(f"       Line: {count}: {line}")
        exit()
    newRule = Rule(left, right)
    rulesList.append(newRule)
    if line.find("<=>") != -1:
        print("Error: This version doesn't support biconditional rules.")
        print(f"       Line: {count}: {line}")
        exit()


def keyExist(c):
    try:
        factsList[c]
    except KeyError:
        return False
    return True


def fillFactList(initialFact):
    isNot = False
    for elem in rulesList:
        for c in elem.strLeftRule:
            if c == '!':
                isNot = True
            elif c.isalpha() and not keyExist(c):
                if initialFact == None:
                    isInitial = False
                else:
                    isInitial = False if c not in initialFact else True
                factsList[c.upper()] = FactNode(c.upper(), isInitial, isInitial, isNot)
                isNot = False
        for c in elem.strRightRule:
            if c == '!':
                isNot = True
            elif c.isalpha() and not keyExist(c):
                if initialFact == None:
                    isInitial = False
                else:
                    isInitial = False if c not in initialFact else True
                factsList[c.upper()] = FactNode(c.upper(), isInitial, isInitial, isNot)
                isNot = False
    if initialFact != None:
        for c in initialFact:
            if c.isalpha() and c.upper() not in factsList:
                print("Error: Initial fact refer to unknown fact. -> " + c)
                exit()
    for elem in rulesList:
        elem.leftRule = elem.fillRule(elem.strLeftRule, factsList)
        elem.rightRule = elem.fillRule(elem.strRightRule, factsList)


def filQueriesList(initialQueries):
    for c in initialQueries:
        if c.isalpha():
            if c.upper() not in factsList:
                print("Error: One or more querie(s) refer to an unknown fact. -> " + c)
                exit()
            queries[c.upper()] = factsList[c.upper()]


def checkError():
    if len(queries) == 0:
        print("Error: There is no queries.")
        exit()
    for elem1 in rulesList:
        for elem2 in rulesList:
            if elem1 is elem2:
                continue
            if elem1.strLeftRule == elem2.strLeftRule:
                print("Error: This rule appear twice.")
                print(f"       Rules: {elem1.strLeftRule} => {elem1.strRightRule}")
                print(f"       And:   {elem2.strLeftRule} => {elem2.strRightRule}")
                exit()


def getAssociatedRule():
    for elem in factsList.values():
        for rule in rulesList:
            for obj in rule.rightRule:
                if elem.name == obj:
                    elem.addRule(rule)


def parseFile(input):
    lines = input.readlines()
    count = 0
    initialFact = None
    initialQueries = None
    for line in lines:
        count += 1
        line = removeComment(line)
        if line.startswith('='):
            if initialFact != None:
                print("Error: Initial fact has been already set.")
                print(f"       Line: {count}: {line}")
                exit()
            initialFact = line
            continue
        elif line.startswith('?'):
            if initialQueries != None:
                print("Error: Queries has been already set.")
                print(f"       Line: {count}: {line}")
                exit()
            initialQueries = line
            continue
        elif len(line) == 0 or line.startswith('\n'):
            continue
        getRules(line, count)
    if initialQueries == None:
        print("Error: No queries found.")
        exit()
    fillFactList(initialFact)
    filQueriesList(initialQueries)
    checkError()
    getAssociatedRule()


def ruleToList(rule):
    for elem in rule.leftRule.values():
        if elem.isFixed:
            continue
        runGraph(elem)


def runGraph(elem):
    while not elem.isFixed:
        if len(elem.linkedRules) == 0:
            return
        rule = elem.getLinkedRule()
        if rule == None:
            return
        ruleToList(rule)
        if len(rule.rightRule) > 1 and rule.strRightRule[1] == '+':
            ret, fixed = rule.computeRule(rule)
            for val in rule.rightRule.values():
                if val.isNot:
                    val.value = not ret
                else:
                    val.value = ret
                val.isFixed = fixed
        else:
            fixed = False
            if elem.isNot:
                elem.value, fixed = rule.computeRule(rule)
                elem.value = not elem.value
            else:
                elem.value, fixed = rule.computeRule(rule)
            elem.isFixed = fixed


def cleanPath():
    for elem in rulesList:
        elem.visited = False


def main():
    if len(sys.argv) < 2:
        print("Error: You must provide a file.")
        exit()
    try:
        with open(sys.argv[1]) as input:
        # with open("/Users/abassibe/rendu/Expert-System/tests/test/examples/bad_files/rules/bad_rule3.txt") as input:
            parseFile(input)
    except FileNotFoundError:
        print("Error: File not found.")
        exit()
    except IsADirectoryError:
        print("Error: This is a directory...")
        exit()
    for elem in queries.values():
        runGraph(elem)
        cleanPath()
    for elem in queries.values():
        print(elem.name + ": " + str(bool(elem.value)))


if __name__ == "__main__":
    main()
