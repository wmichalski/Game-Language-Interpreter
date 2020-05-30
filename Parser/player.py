class Player():
    def __init__(self, name):
        self.name = name
        self.variables = dict()
        self.addVariable(["player.name", self.name])
        pass

    def getValue(self, varName):
        for key in self.variables:
            if key == varName:
                return self.variables[key]
        raise KeyError(varName + " was not found")

    def setValue(self, varName, varValue):
        for key in self.variables:
            if key == varName:
                self.variables[key] = varValue
                return 0
        raise KeyError(varName + " was not found")

    def addVariable(self, varPair):
        self.variables[varPair[0]] = varPair[1]

    def printInfo(self, isWon):
        print(self.name, end='')
        
        if isWon == 1:
            print(" - WINNER")
        else:
            print("")

        for key in self.variables:
            if key != "player.name":
                print("   " + key + " -- " + str(self.variables[key]))
        print("")
