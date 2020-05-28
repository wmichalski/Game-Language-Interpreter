class Function():
    def __init__(self, name, args, body):
        self.name = name
        self.body = body
        self.args = args
        self.returnStatus = 0

    def execute(self):
        return self.body.execute()

    def getVarDict(self, args):
        if len(self.args) != len(args):
            raise IndexError("Not enough arguments given to run a func")
        retDict = {}
        for name, value in zip(self.args, args):
            retDict[name] = value

        return retDict

    def getName(self):
        return self.name