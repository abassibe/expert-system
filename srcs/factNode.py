
class FactNode:
    def __init__(self, name, value=False, isFixed=False, isNot=False):
        self.name = name
        self.value = value
        self.linkedRules = []
        self.isFixed = isFixed
        self.isNot = isNot

    def addRule(self, rule):
        self.linkedRules.append(rule)

    def getLinkedRule(self):
        for rule in self.linkedRules:
            if rule.visited == False:
                rule.visited = True
                return rule
        return None
