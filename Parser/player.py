class Player():
    def __init__(self, vars):
        self.variables = vars

    def getValue(self, varName):
        for var in self.variables:
            if var[0] == varName:
                return var[1]
        KeyError(varName + " was not found")
        return 0

    def setValue(self, varName, varValue):
        for var in self.variables:
            if var[0] == varName:
                var[1] = varValue
        KeyError(varName + " was not found")
        return 0

    def addVariable(self, varPair):
        self.variables[varPair[0]] = varPair[1]
