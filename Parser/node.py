from Lexer.token import Token, header_names
from Parser.function import Function
from copy import deepcopy
from Parser.player import Player
from random import randrange

# localVarDict keeps either a dict of variables from the "RUN" section or from the called function
localVarDict = {}
gameVarDict = {}

breakStatus = 0
analysedFunc = Function("placeholder", "placeholder", "placeholder")
analysedHeader = ""
functions = []
analysedPlayer = None
players = []

def pairwise(iterable):
    # https://stackoverflow.com/questions/4628290/pairs-from-single-list
    a = iter(iterable)
    return zip(a, a)

def callFunction(funcObject, args):
    global localVarDict
    global analysedFunc

    lastFunc = analysedFunc
    lastVarDict = localVarDict

    analysedFunc = deepcopy(funcObject)
    localVarDict = analysedFunc.getVarDict(args)
    retValue = analysedFunc.execute()

    analysedFunc = lastFunc
    localVarDict = lastVarDict

    return retValue

class Node():
    def __init__(self, tokens):
        self.tokens = tokens
        self.value = None
        self.looped = -1

    def peekToken(self, depth = -1):
        return self.tokens[depth].type

    def popToken(self):
        return self.tokens.pop()

    def create_subtree(self, tokens):
        self.tokens = tokens
        if self.peekToken() == "IF":
            return IfNode(self.tokens)

        if self.peekToken() == "WHILE":
            return WhileNode(self.tokens)

        if self.peekToken() == "FUNCTION_DEF":
            return FunctionInitNode(self.tokens)

        if self.peekToken() == "VARIABLE_ASSIGN":
            return VariableInitNode(self.tokens)

        if self.peekToken() == "BREAK":
            return BreakNode(self.tokens)

        if self.peekToken() == "CHOICE":
            return ChoiceStatementNode(self.tokens)

        if self.peekToken() == "RETURN":
            return ReturnNode(self.tokens)

        if self.peekToken() == "PLAYERS":
            return PlayersHeaderNode(self.tokens)

        if self.peekToken() == "GAME":
            return GameHeaderNode(self.tokens)

        if self.peekToken() == "INDIVIDUAL":
            return IndividualHeaderNode(self.tokens)

        if self.peekToken() == "FUNCTIONS":
            return FunctionsHeaderNode(self.tokens)

        if self.peekToken() == "RUN":
            return RunHeaderNode(self.tokens)  

        if self.peekToken() == "WIN":
            return WinHeaderNode(self.tokens)  

        if self.peekToken() == "PRINT":
            return PrintNode(self.tokens)

        if self.peekToken() == "FOR_EACH_PLAYER":
            return ForEachPlayerNode(self.tokens)

        if self.peekToken() == "LEFT_ROUND":
            return BracketedExpression(self.tokens)

        if self.peekToken() == "IDENTIFIER" and self.peekToken(-2) == "END_OF_FILE":
            return VariableAssignmentNode(self.tokens)

        if self.peekToken() == "IDENTIFIER" and self.peekToken(-2) == "ASSIGNMENT":
            return VariableAssignmentNode(self.tokens)

        if self.peekToken() in ["REAL_NUMBER", "NATURAL_NUMBER", "IDENTIFIER", "ROLL", "MINUS", "LOGICAL_NOT"]:
            return LogicalOrNode(self.tokens)

        if self.looped == len(self.tokens):
            if self.peekToken() == "SEMICOLON":
                self.popToken()
                return doNothing(self.tokens)
            else:
                raise SyntaxError("Infinite loop. Some issue with a token: " + self.tokens[-1].type + " - " + self.tokens[-1].value)

        self.looped = len(self.tokens)
        return self.create_subtree(self.tokens)
        
        
class doNothing(Node):
    def __init__(self, tokens):
        super().__init__(tokens)

    def execute(self):
        return None

class WhileNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()

    def parse(self):
        if self.popToken().type != "WHILE":
            raise SyntaxError("WHILE seems not to have a WHILE. How?")
        if self.popToken().type != "LEFT_ROUND":
            raise SyntaxError("WHILE seems not to have a (")

        self.children.append(Condition(self.tokens))

        if self.popToken().type != "RIGHT_ROUND":
            raise SyntaxError("WHILE seems not to have a )")
        if self.popToken().type != "LEFT_CURLY":
            raise SyntaxError("WHILE seems not to have a {")

        self.children.append(BlockOfCode(self.tokens))

        if self.popToken() == "RIGHT_CURLY":
            raise SyntaxError("WHILE seems not to have a }")

    def execute(self):
        global breakStatus
        while breakStatus == 0:
            if self.children[0].execute():
                self.children[1].execute()
            else:
                break

        breakStatus = 0
        
class BlockOfCode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()

    def parse(self):
        while self.peekToken() != "RIGHT_CURLY":
            self.children.append(super().create_subtree(self.tokens)) 
            if self.peekToken() == "SEMICOLON":
                self.popToken()
            if self.peekToken() == "WIN":
                break
            if self.peekToken() == "END_OF_FILE":
                break

    def execute(self):
        toReturn = None
        for child in self.children:
            if breakStatus == 0 and analysedFunc.returnStatus == 0:
                toReturn = child.execute()
        
        return toReturn

class RollNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()
    
    def parse(self):
        self.popToken() # ROLL
        if self.popToken().type != "LEFT_ROUND":
            raise SyntaxError("ROLL seems not to have a (")
        self.children.append(super().create_subtree(self.tokens)) 
        if self.popToken() == "RIGHT_ROUND":
            raise SyntaxError("ROLL seems not to have a )")

    def execute(self):
        return randrange(self.children[0].execute())

class PrintNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()
    
    def parse(self):
        self.popToken() # PRINT
        if self.popToken().type != "LEFT_ROUND":
            raise SyntaxError("PRINT seems not to have a (")
        self.children.append(super().create_subtree(self.tokens)) 
        if self.popToken() == "RIGHT_ROUND":
            raise SyntaxError("PRINT seems not to have a )")

    def execute(self):
        print(self.children[0].execute())

class BreakNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)

        self.parse()

    def parse(self):
        self.popToken()

    def execute(self):
        global breakStatus
        breakStatus = 1

class ReturnNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()

    def parse(self):
        self.popToken() # RETURN
        self.children.append(super().create_subtree(self.tokens)) 

    def execute(self):
        analysedFunc.returnStatus = 1
        return self.children[0].execute()
        # i jak dojdziemy do return to warto by bylo jakies info zwrocic do execute w block of code zeby dalej nie grzebac i od razu zakonczyc
        # ale sraka boze
        # tylko uwazac na zagniezdzenia damn

class VariableInitNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.name = None
        self.parse(tokens)
    
    def parse(self, tokens):
        if self.popToken().type != "VARIABLE_ASSIGN":
            raise SyntaxError("VAR seems not to have a VAR. How?")

        self.name = self.popToken().value
        if self.peekToken() == "ASSIGNMENT":
            self.popToken()
            self.children.append(super().create_subtree(self.tokens))

    def get_name(self):
        return self.name

    def execute(self):
        if "player." in self.name:
            for player in players:
                player.addVariable([self.name, self.children[0].execute()])
        elif "game." in self.name:
            gameVarDict[self.name] = self.children[0]
        else:
            value = self.children[0].execute()
            localVarDict[self.name] = value

class VariableAssignmentNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.name = None
        self.parse(tokens)
    
    def parse(self, tokens):
        self.name = self.popToken().value
        if self.peekToken() == "ASSIGNMENT":
            self.popToken()
            self.children.append(super().create_subtree(self.tokens))

    def get_name(self):
        return self.name

    def execute(self):
        if "player." in self.name:
            if analysedPlayer.getValue(self.name) is not None:
                analysedPlayer.setValue(self.name, self.children[0].execute())
            else:
                raise KeyError("Player doesn't have such a variable.", self.name)
        elif "game." in self.name:
            if self.name in gameVarDict:
                gameVarDict[self.name] = self.children[0]
            else:
                raise KeyError("Game doesn't have such a variable.", self.name)
        else:
            if self.name in localVarDict:
               localVarDict[self.name] = self.children[0].execute()
            else:
               KeyError("Variable" + self.name + "was not found")

class FunctionInitNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.name = None
        self.children = [] # args
        self.parse()

    def parse(self):
        if(self.popToken().type != "FUNCTION_DEF"):
            raise SyntaxError("FUNCTION_DEF seems not to have a FUNCTION_DEF. How?")

        if(self.peekToken() == "IDENTIFIER"):
            self.name = self.popToken().value

        if(self.popToken().type != "LEFT_ROUND"):
            raise SyntaxError("FUNCTION_DEF seems not to have a (")

        while(self.peekToken() != "RIGHT_ROUND"):
            self.children.append(self.popToken())
            if self.peekToken() == "COMMA":
                self.popToken()
                
        if(self.popToken().type != "RIGHT_ROUND"):
            raise SyntaxError("FUNCTION_DEF seems not to have a )")

        if(self.popToken().type != "LEFT_CURLY"):
            raise SyntaxError("FUNCTION_DEF seems not to have a {")

        self.children.append(BlockOfCode(self.tokens))

        if(self.popToken().type != "RIGHT_CURLY"):
            raise SyntaxError("FUNCTION_DEF seems not to have a }")

    def get_name(self):
        return self.name

    def execute(self):
        parameters = [token.value for token in self.children[:-1]]
        functions.append(Function(self.name, parameters, self.children[-1]))

class ForEachPlayerNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()

    def parse(self):
        if self.popToken().type != "FOR_EACH_PLAYER":
            raise SyntaxError("FOREACHPLAYER seems not to have a FOREACHPLAYER. How?")
        if self.popToken().type != "LEFT_ROUND":
            raise SyntaxError("FOREACHPLAYER seems not to have a (.")

        self.children.append(Condition(self.tokens))

        if self.popToken().type != "RIGHT_ROUND":
            raise SyntaxError("FOREACHPLAYER seems not to have a ).")
        if self.popToken().type != "LEFT_CURLY":
            raise SyntaxError("FOREACHPLAYER seems not to have a {.")

        self.children.append(BlockOfCode(self.tokens))

        if self.popToken() == "RIGHT_CURLY":
            raise SyntaxError("FOREACHPLAYER seems not to have a }.")

    def execute(self):
        # not sure yet if breakStatus will collide with WhileNode if nested or not
        global breakStatus
        global analysedPlayer

        if self.children[0].execute():
            for player in players:
                if breakStatus == 0:
                    analysedPlayer = player
                    self.children[1].execute()

        breakStatus = 0
        analysedPlayer = None

class IfNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()

    def parse(self):
        if self.popToken().type != "IF":
            raise SyntaxError("IF seems not to have an IF. How?")
        if self.popToken().type != "LEFT_ROUND":
            raise SyntaxError("IF seems not to have a (.")

        self.children.append(Condition(self.tokens))

        if self.popToken().type != "RIGHT_ROUND":
            raise SyntaxError("IF seems not to have a ).")
        if self.popToken().type != "LEFT_CURLY":
            raise SyntaxError("IF seems not to have a {.")

        self.children.append(BlockOfCode(self.tokens))

        if self.popToken() == "RIGHT_CURLY":
            raise SyntaxError("IF seems not to have a }.")

        if self.peekToken() == "ELSE":
            self.popToken() 
            if self.popToken().type != "LEFT_CURLY":
                raise SyntaxError("ELSE seems not to have a {.")

            self.children.append(BlockOfCode(self.tokens))

            if self.popToken().type != "RIGHT_CURLY":
                raise SyntaxError("ELSE seems not to have a }.")

    def execute(self):
        if self.children[0].execute():
            return self.children[1].execute()
        else:
            if len(self.children) == 3:
                return self.children[2].execute()


class Condition(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse(tokens)
    
    def parse(self, tokens):
        self.children.append(super().create_subtree(self.tokens))

    def execute(self):
        return self.children[0].execute()

class ProgramNode(Node):
    # note for self: ignore "RUN:" tokens etc
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.varDict = {}
        global localVarDict
        localVarDict = self.varDict

        self.parse()

    def parse(self):
        while(self.peekToken() != "END_OF_FILE"):
            self.children.append(super().create_subtree(self.tokens))

    def execute(self):
        for child in self.children:
            child.execute()
        
class ChoiceStatementNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()
    
    def parse(self):
        self.popToken() # CHOICE
        if self.popToken().type != "LEFT_ROUND":
            raise SyntaxError("Choice init seems not to have a (")

        self.children.append(super().create_subtree(self.tokens))

        if self.popToken().type != "RIGHT_ROUND":
            raise SyntaxError("Choice init seems not to have a )")
        if self.popToken().type != "LEFT_CURLY":
            raise SyntaxError("Choice init seems not to have a {")

        while self.peekToken() != "RIGHT_CURLY":
            self.children.append(ChoiceNode(self.tokens))

        if self.popToken().type != "RIGHT_CURLY":
            raise SyntaxError("Choice init seems not to have a }")

    def execute(self):
        selectable = []
        for child in self.children:
            if child.children[0].execute():
                selectable.append(child)
        # TODO select

class ChoiceNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []

        self.parse()

    def parse(self):
        if self.popToken().type != "LEFT_SQUARE":
            raise SyntaxError("Choice seems not to have a [")

        self.children.append(Condition(self.tokens))

        if self.popToken().type != "RIGHT_SQUARE":
            raise SyntaxError("Choice seems not to have a ]")
        if self.popToken().type != "LEFT_CURLY":
            raise SyntaxError("Choice seems not to have a {")

        self.children.append(BlockOfCode(self.tokens))

        if self.popToken().type != "RIGHT_CURLY":
            raise SyntaxError("Choice seems not to have a }")

class LogicalOrNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.value = None
        self.children = []

        self.children.append(LogicalAndNode(tokens))
        self.parse()

    def parse(self):
        while(self.peekToken() == "LOGICAL_OR"):
            self.popToken()
            self.children.append(LogicalAndNode(self.tokens))

    def execute(self):
        if len(self.children) == 1:
            return self.children[0].execute()
        else:
            for element in self.children:
                if element.__class__ != Token:
                    if element.execute() == 1:
                        return 1
            return 0


class LogicalAndNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.value = None
        self.children = []

        self.children.append(LogicalCompareNode(tokens))
        self.parse()

    def parse(self):
        while(self.peekToken() == "LOGICAL_AND"):
            self.popToken()
            self.children.append(LogicalCompareNode(self.tokens))

    def execute(self):
        if len(self.children) == 1:
            return self.children[0].execute()
        else:
            for element in self.children:
                if element.__class__ != Token:
                    if element.execute() == 0:
                        return 0
            return 1

class LogicalNegationNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []

        self.parse()

    def parse(self):
        if(self.peekToken() == "LOGICAL_NOT"):
            self.popToken()
            self.children.append(LogicalNot(self.tokens))
        self.children.append(FullMathExpressionNode(self.tokens))

    def execute(self):
        if self.children[0].__class__ == LogicalNot:
            if self.children[1].execute() != 0:
                return 0
            else:
                return 1
        else:
            return self.children[0].execute()

class LogicalCompareNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = [LogicalNegationNode(tokens)]

        self.parse()

    def parse(self):
        if(self.peekToken() in ["EQUAL_TO", "NOT_EQUAL_TO", "LOWER_OR_EQUAL", "GREATER_OR_EQUAL", "LOWER", "GREATER"]):
            self.children.append(self.popToken())
            self.children.append(LogicalNegationNode(self.tokens))

        # if len(self.children) == 1:
        #     try:
        #         self.children = list(self.children[0].children)
        #     except:
        #         pass

    def execute(self):
        if len(self.children) == 1:
            return self.children[0].execute()
        else:
            lvalue = self.children[0].execute()
            rvalue = self.children[2].execute()
            return {
                "EQUAL_TO": lvalue== rvalue,
                "NOT_EQUAL_TO": lvalue != rvalue,
                "LOWER_OR_EQUAL": lvalue <= rvalue,
                "GREATER_OR_EQUAL": lvalue >= rvalue,
                "LOWER": lvalue < rvalue,
                "GREATER": lvalue > rvalue
            }[self.children[1].type]


class FunctionCallNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.name = None
        self.children = [] # args
        self.parse()

    def parse(self):
        if(self.peekToken() == "IDENTIFIER"):
            self.name = self.popToken().value

        if(self.popToken().type != "LEFT_ROUND"):
            raise SyntaxError("Function call seems not to have a (")

        while(self.peekToken() != "RIGHT_ROUND"):
            self.children.append(super().create_subtree(self.tokens))
            if self.peekToken() == "COMMA":
                self.popToken()

        if(self.popToken().type != "RIGHT_ROUND"):
            raise SyntaxError("Function call seems not to have a )")

    def get_name(self):
        return self.name

    def execute(self):
        parameters = [child.execute() for child in self.children]
        for function in functions:
            if function.name == self.name:
                return callFunction(function, parameters)

class LogicalNot(Node):
    def __init__(self, tokens):
        super().__init__(tokens)

class FullMathExpressionNode(Node):
    # fullMathExpression = multiplication, { additionOperator, multiplication } ;
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []

        self.children.append(MultiplicationNode(tokens))
        self.parse()

    def parse(self):
        while(self.peekToken() in ["PLUS", "MINUS"]):
            self.children.append(self.popToken())
            self.children.append(MultiplicationNode(self.tokens))

    def execute(self):
        self.to_return = self.children[0].execute()
        if len(self.children) > 1:
            for operation, element in pairwise(self.children[1:]):
                if operation.value == "+":
                    self.to_return += element.execute()
                if operation.value == "-":
                    self.to_return -= element.execute()

        return self.to_return
        # if len(self.children) == 1:
        #     self.children = list(self.children[0].children)

class MultiplicationNode(Node):
    # multiplication = partMathExpression, { multiplicationOperator, partMathExpression } ;
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []

        self.children.append(PartMathExpressionNode(tokens))
        self.parse()

    def parse(self):
        while(self.peekToken() in ["MULTIPLICATION", "DIVISION"]):
            self.children.append(self.popToken())
            self.children.append(PartMathExpressionNode(self.tokens))
    
    def execute(self):
        self.to_return = self.children[0].execute()
        if len(self.children) > 1:
            for operation, element in pairwise(self.children[1:]):
                if operation.value == "*":
                    self.to_return *= element.execute()
                if operation.value == "/":
                    self.to_return /= element.execute()

        return self.to_return

class PartMathExpressionNode(Node):
# partMathExpression = [ "-" ], ( number | variableName | functionCall | bracketedExpression ) ;
    def __init__(self, tokens):
        super().__init__(tokens)
        self.is_negative = False
        self.children = []

        self.parse()

    def parse(self):
        if(self.peekToken() == "MINUS"):
            self.popToken()
            self.children.append(NegativeNumber(self.tokens))
            self.is_negative = True

        if(self.peekToken() == "LEFT_ROUND"):
            self.children.append(BracketedExpression(self.tokens))
        elif(self.peekToken() in ["REAL_NUMBER", "NATURAL_NUMBER"]):
            self.children.append(ValueNode(self.tokens))
        elif(self.peekToken() == "ROLL"):
            self.children.append(RollNode(self.tokens))
        elif(self.peekToken() == "IDENTIFIER"):
            if self.tokens[-2].type == "LEFT_ROUND":
                self.children.append(FunctionCallNode(self.tokens))
            else:
                self.children.append(ValueNode(self.tokens))

    def get_value(self):
        return self.value

    def execute(self):
        if self.is_negative:
            return -1*self.children[1].execute()
        else:
            return self.children[0].execute()

class ValueNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.type = self.peekToken()
        self.parse()

    def parse(self):
        self.value = self.popToken().value

    def get_value(self):
        return self.value

    def execute(self):
        if self.type in ["REAL_NUMBER", "NATURAL_NUMBER"]:
            if "." in self.value:
               return float(self.value)
            else:
                return int(self.value)

        if self.type in ["IDENTIFIER"]:
            if "player." in self.value:
                return analysedPlayer.getValue(self.value)
            elif "game." in self.value:
                try:
                    global gameVarDict
                    return gameVarDict[self.value]
                except:
                    raise NameError("Variable not found in gamedict", self.value)
            else:
                try:
                    global localVarDict
                    return localVarDict[self.value]
                except:
                    raise NameError(self.value + " was not found in variable dict")
        return self.value

class NegativeNumber(Node):
    def __init__(self, tokens):
        super().__init__(tokens)

class BracketedExpression(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()

    def parse(self):
        if self.popToken().type != "LEFT_ROUND":
            raise SyntaxError("Bracketed expression seems not to be open")

        self.children.append(super().create_subtree(self.tokens))

        if self.popToken().type != "RIGHT_ROUND":
            raise SyntaxError("Bracketed expression seems not to be closed")

    def execute(self):
        return self.children[0].execute()

class PlayersHeaderNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()

    def parse(self):
        if self.popToken().type != "PLAYERS":
            raise SyntaxError("Missing PLAYERS in PLAYERS. How?")
        
        self.children.append(super().create_subtree(self.tokens))

    def execute(self):
        for i in range(self.children[0].execute()):
            players.append(Player("Player " + str(i)))

class GameHeaderNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()

    def parse(self):
        if self.popToken().type != "GAME":
            raise SyntaxError("Missing GAME in GAME. How?")
        if self.popToken().type != "COLON":
            raise SyntaxError("Missing COLON after WIN. How?")

        while self.peekToken() not in header_names:
            self.children.append(VariableInitNode(self.tokens))
            if self.peekToken() == "SEMICOLON":
                self.popToken()

    def execute(self):
        for child in self.children:
            child.execute()

class IndividualHeaderNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()

    def parse(self):
        if self.popToken().type != "INDIVIDUAL":
            raise SyntaxError("Missing INDIVIDUAL in INDIVIDUAL. How?")
        if self.popToken().type != "COLON":
            raise SyntaxError("Missing colon after  WIN.")

        while self.peekToken() not in header_names:
            self.children.append(VariableInitNode(self.tokens))
            if self.peekToken() == "SEMICOLON":
                self.popToken()

    def execute(self):
        for child in self.children:
            child.execute()

class FunctionsHeaderNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()

    def parse(self):
        if self.popToken().type != "FUNCTIONS":
            raise SyntaxError("Missing FUNCTIONS in FUNCTIONS. How?")
        if self.popToken().type != "COLON":
            raise SyntaxError("Missing colon after FUNCTIONS.")

        while self.peekToken() not in header_names:
            self.children.append(FunctionInitNode(self.tokens))
            if self.peekToken() == "SEMICOLON":
                self.popToken()

    def execute(self):
        for child in self.children:
            child.execute()

class RunHeaderNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()

    def parse(self):
        if self.popToken().type != "RUN":
            raise SyntaxError("Missing RUN in RUN. How?")
        if self.popToken().type != "COLON":
            raise SyntaxError("Missing colon after RUN.")

        self.children.append(BlockOfCode(self.tokens))

    def execute(self):
        for child in self.children:
            child.execute()

class WinHeaderNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()

    def parse(self):
        if self.popToken().type != "WIN":
            raise SyntaxError("Missing WIN in WIN. How?")
        if self.popToken().type != "COLON":
            raise SyntaxError("Missing colon after WIN.")
        if self.popToken().type != "LEFT_SQUARE":
            raise SyntaxError("Missing [ after WIN:.")

        self.children.append(Condition(self.tokens))

        if self.popToken().type != "RIGHT_SQUARE":
            raise SyntaxError("Missing ] after WIN.")

    def execute(self):
        global analysedPlayer
        for player in players:
            analysedPlayer = player
            if self.children[0].execute():
                player.printInfo(1)
            else:
                player.printInfo(0)
            
