from Lexer.token import Token, header_names
from Parser.function import Function
from copy import deepcopy
from Parser.player import Player
from random import randrange
from Parser import error_manager
import random

# localVarDict keeps either a dict of variables from the "RUN" section or from the called function
localVarDict = {}
gameVarDict = {}
functions = []
players = []

breakStatus = 0
analysedFunc = Function("placeholder", "placeholder", "placeholder")
analysedHeader = ""

analysedPlayer = None
chosenPlayer = None
filemanager = None


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


def ChoosePolicy(selectables):
    return random.choice(selectables)


def ChoosePlayer():
    global analysedPlayer
    randomed = random.choice(players)

    while randomed == analysedPlayer:
        randomed = random.choice(players)

    return randomed


def raise_error(message, token):
    global filemanager
    error_manager.manage_error(filemanager, token)
    raise error_manager.ErrorManager(message)


class Node():
    def __init__(self, tokens):
        self.tokens = tokens
        self.value = None
        self.looped = -1

    def peekTokenType(self, depth=-1):
        return self.tokens[depth].type

    def peekTokenPosition(self, depth=-1):
        return self.tokens[depth].position-len(self.tokens[depth].value)

    def popToken(self):
        return self.tokens.pop()

    def create_subtree(self, tokens):
        self.tokens = tokens
        if self.peekTokenType() == "IF":
            return IfNode(self.tokens)

        if self.peekTokenType() == "WHILE":
            return WhileNode(self.tokens)

        if self.peekTokenType() == "FUNCTION_DEF":
            return FunctionInitNode(self.tokens)

        if self.peekTokenType() == "VARIABLE_ASSIGN":
            return VariableInitNode(self.tokens)

        if self.peekTokenType() == "BREAK":
            return BreakNode(self.tokens)

        if self.peekTokenType() == "CHOICE":
            return ChoiceStatementNode(self.tokens)

        if self.peekTokenType() == "RETURN":
            return ReturnNode(self.tokens)

        if self.peekTokenType() == "PLAYERS":
            return PlayersHeaderNode(self.tokens)

        if self.peekTokenType() == "GAME":
            return GameHeaderNode(self.tokens)

        # if self.peekTokenType() == "TEXT":
        #     return TextNode(self.tokens)

        if self.peekTokenType() == "INDIVIDUAL":
            return IndividualHeaderNode(self.tokens)

        if self.peekTokenType() == "FUNCTIONS":
            return FunctionsHeaderNode(self.tokens)

        if self.peekTokenType() == "RUN":
            return RunHeaderNode(self.tokens)

        if self.peekTokenType() == "WIN":
            return WinHeaderNode(self.tokens)

        if self.peekTokenType() == "PRINT":
            return PrintNode(self.tokens)

        if self.peekTokenType() == "FOR_EACH_PLAYER":
            return ForEachPlayerNode(self.tokens)

        if self.peekTokenType() == "LEFT_ROUND":
            return BracketedExpression(self.tokens)

        if self.peekTokenType() == "IDENTIFIER" and self.peekTokenType(-2) == "ASSIGNMENT":
            return VariableAssignmentNode(self.tokens)

        if self.peekTokenType() in ["REAL_NUMBER", "NATURAL_NUMBER", "IDENTIFIER", "ROLL", "MINUS", "LOGICAL_NOT"]:
            return LogicalOrNode(self.tokens)

        if self.looped == len(self.tokens):
            if self.peekTokenType() == "SEMICOLON":
                self.popToken()
                return doNothing(self.tokens)
            else:
                raise SyntaxError("Infinite loop. Some issue with a token: " +
                                  self.tokens[-1].type + " - " + self.tokens[-1].value)

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
        self.position = self.peekTokenPosition()

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
        self.position = self.peekTokenPosition()

        while self.peekTokenType() != "RIGHT_CURLY":
            new_child = super().create_subtree(self.tokens)
            if new_child.__class__ is not doNothing:
                self.children.append(new_child)
            if self.peekTokenType() == "SEMICOLON":
                self.popToken()
            if self.peekTokenType() == "WIN":
                break
            if self.peekTokenType() == "END_OF_FILE":
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
        self.position = self.peekTokenPosition()

        self.popToken()  # ROLL
        if self.popToken().type != "LEFT_ROUND":
            raise_error("ROLL seems not to have a (", self.position)
        self.children.append(LogicalOrNode(self.tokens))
        if self.popToken() == "RIGHT_ROUND":
            raise_error("ROLL seems not to have a )", self.position)

    def execute(self):
        return randrange(self.children[0].execute())


class PrintNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()

    def parse(self):
        self.position = self.peekTokenPosition()

        self.popToken()  # PRINT
        if self.popToken().type != "LEFT_ROUND":
            raise_error("PRINT seems not to have a (", self.position)
        self.children.append(LogicalOrNode(self.tokens))
        if self.popToken() == "RIGHT_ROUND":
            raise_error("PRINT seems not to have a )", self.position)

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
        self.popToken()  # RETURN
        self.children.append(LogicalOrNode(self.tokens))

    def execute(self):
        analysedFunc.returnStatus = 1
        return self.children[0].execute()

class VariableInitNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.name = None
        self.parse(tokens)

    def parse(self, tokens):
        self.position = self.peekTokenPosition()

        if self.popToken().type != "VARIABLE_ASSIGN":
            raise_error("VAR seems not to have a VAR. How?", self.position)

        self.name = self.popToken().value
        if self.peekTokenType() == "ASSIGNMENT":
            self.popToken()
            self.children.append(LogicalOrNode(self.tokens))

    def get_name(self):
        return self.name

    def execute(self):
        if "player." in self.name:
            for player in players:
                player.addVariable([self.name, self.children[0].execute()])
        elif "game." in self.name:
            gameVarDict[self.name] = self.children[0].execute()
        elif "rolled" == self.name:
            raise_error(
                "Rolled cannot have a user-assigned value.", self.position)
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
        self.position = self.peekTokenPosition()

        self.name = self.popToken().value
        if self.peekTokenType() == "ASSIGNMENT":
            self.popToken()
            self.children.append(LogicalOrNode(self.tokens))

    def get_name(self):
        return self.name

    def execute(self):
        if "player." in self.name:
            if analysedPlayer.getValue(self.name) is not None:
                analysedPlayer.setValue(self.name, self.children[0].execute())
            else:
                raise KeyError(
                    "Player doesn't have such a variable.", self.name)
        elif "chosen." in self.name:
            if chosenPlayer.getValue(self.name.replace("chosen.", "player.")) is not None:
                chosenPlayer.setValue(self.name.replace(
                    "chosen.", "player."), self.children[0].execute())
            else:
                raise KeyError(
                    "Chosen player doesn't have such a variable.", self.name)
        elif "game." in self.name:
            if self.name in gameVarDict:
                gameVarDict[self.name] = self.children[0].execute()
            else:
                raise KeyError("Game doesn't have such a variable.", self.name)
        else:
            if self.name in localVarDict:
                localVarDict[self.name] = self.children[0].execute()
            else:
                raise KeyError("Variable " + self.name + " was not found")


class FunctionInitNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.name = None
        self.children = []  # args
        self.parse()

    def parse(self):
        self.position = self.peekTokenPosition()

        if(self.popToken().type != "FUNCTION_DEF"):
            raise SyntaxError(
                "FUNCTION_DEF seems not to have a FUNCTION_DEF. How?")

        if(self.peekTokenType() == "IDENTIFIER"):
            self.name = self.popToken().value

        if(self.popToken().type != "LEFT_ROUND"):
            raise SyntaxError("FUNCTION_DEF seems not to have a (")

        while(self.peekTokenType() != "RIGHT_ROUND"):
            self.children.append(self.popToken())
            if self.peekTokenType() == "COMMA":
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
        self.position = self.peekTokenPosition()

        if self.popToken().type != "FOR_EACH_PLAYER":
            raise_error(
                "FOREACHPLAYER seems not to have a FOREACHPLAYER. How?", self.position)
        if self.popToken().type != "LEFT_ROUND":
            raise_error("FOREACHPLAYER seems not to have a (.", self.position)

        self.children.append(Condition(self.tokens))

        if self.popToken().type != "RIGHT_ROUND":
            raise_error("FOREACHPLAYER seems not to have a ).", self.position)
        if self.popToken().type != "LEFT_CURLY":
            raise_error("FOREACHPLAYER seems not to have a {.", self.position)

        self.children.append(BlockOfCode(self.tokens))

        if self.popToken() == "RIGHT_CURLY":
            raise SyntaxError("FOREACHPLAYER seems not to have a }.")

    def execute(self):
        # not sure yet if breakStatus will collide with WhileNode if nested or not
        global breakStatus
        global analysedPlayer

        for player in players:
            analysedPlayer = player
            if self.children[0].execute():
                if breakStatus == 0 and analysedFunc.returnStatus == 0:
                    toReturn = self.children[1].execute()

        breakStatus = 0
        analysedPlayer = None
        return toReturn


class IfNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()

    def parse(self):
        self.position = self.peekTokenPosition()

        if self.popToken().type != "IF":
            raise_error("IF seems not to have an IF. How?", self.position)
        if self.popToken().type != "LEFT_ROUND":
            raise_error("IF seems not to have a (.", self.position)

        self.children.append(Condition(self.tokens))

        if self.popToken().type != "RIGHT_ROUND":
            raise_error("IF seems not to have a ).", self.position)
        if self.popToken().type != "LEFT_CURLY":
            raise_error("IF seems not to have a {.", self.position)

        self.children.append(BlockOfCode(self.tokens))

        if self.popToken() == "RIGHT_CURLY":
            raise_error("IF seems not to have a }.", self.position)

        if self.peekTokenType() == "ELSE":
            self.popToken()
            if self.popToken().type != "LEFT_CURLY":
                raise_error("ELSE seems not to have a {.", self.position)

            self.children.append(BlockOfCode(self.tokens))

            if self.popToken().type != "RIGHT_CURLY":
                raise_error("ELSE seems not to have a }.", self.position)

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
        self.position = self.peekTokenPosition()
        self.children.append(LogicalOrNode(self.tokens))

    def execute(self):
        if isinstance(self.children[0].execute(), str):
            raise_error(
                "Seems like you have put a string as a condition", self.position)
        return self.children[0].execute()


class ProgramNode(Node):
    # note for self: ignore "RUN:" tokens etc
    def __init__(self, tokens, fm):
        super().__init__(tokens)
        self.children = []
        self.varDict = {}
        global localVarDict
        localVarDict = self.varDict

        self.init_file_manager(fm)
        self.parse()

    def parse(self):
        while(self.peekTokenType() != "END_OF_FILE"):
            new_child = super().create_subtree(self.tokens)
            if new_child.__class__ is not doNothing:
                self.children.append(new_child)

    def execute(self):
        for child in self.children:
            child.execute()

    def init_file_manager(self, fm):
        global filemanager
        filemanager = fm


class ChoiceStatementNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()

    def parse(self):
        self.position = self.peekTokenPosition()

        self.popToken()  # CHOICE
        if self.popToken().type != "LEFT_ROUND":
            raise_error("Choice init seems not to have a (", self.position)

        self.children.append(LogicalOrNode(self.tokens))

        if self.popToken().type != "RIGHT_ROUND":
            raise_error("Choice init seems not to have a )", self.position)
        if self.popToken().type != "LEFT_CURLY":
            raise_error("Choice init seems not to have a {", self.position)

        while self.peekTokenType() != "RIGHT_CURLY":
            self.children.append(ChoiceNode(self.tokens))

        if self.popToken().type != "RIGHT_CURLY":
            raise_error("Choice init seems not to have a }", self.position)

    def execute(self):
        selectable = []
        localVarDict["rolled"] = randrange(self.children[0].execute())
        for child in self.children[1:]:
            # child's first child is condition:
            if child.children[0].execute():
                selectable.append(child)

        if len(selectable) == 0:
            return 0

        global chosenPlayer
        selected = ChoosePolicy(selectable)
        chosenPlayer = ChoosePlayer()
        selected.execute()
        chosenPlayer = None

        del localVarDict["rolled"]


class ChoiceNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []

        self.parse()

    def parse(self):
        self.position = self.peekTokenPosition()

        if self.popToken().type != "LEFT_SQUARE":
            raise_error("Choice init seems not to have a [", self.position)

        self.children.append(Condition(self.tokens))

        if self.popToken().type != "RIGHT_SQUARE":
            raise_error("Choice init seems not to have a ]", self.position)
        if self.popToken().type != "LEFT_CURLY":
            raise_error("Choice init seems not to have a {", self.position)

        self.children.append(BlockOfCode(self.tokens))

        if self.popToken().type != "RIGHT_CURLY":
            raise_error("Choice init seems not to have a }", self.position)

    def execute(self):
        self.children[1].execute()


class LogicalOrNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.value = None
        self.children = []

        self.children.append(LogicalAndNode(tokens))
        self.parse()

    def parse(self):
        self.position = self.peekTokenPosition()

        while(self.peekTokenType() == "LOGICAL_OR"):
            self.popToken()
            self.children.append(LogicalAndNode(self.tokens))

    def execute(self):
        if len(self.children) == 1:
            return self.children[0].execute()
        else:
            for element in self.children:
                if element.__class__ != Token:
                    if isinstance(element.execute(), str):
                        raise_error(
                            "Seems like you are doing a logical OR operation on a string?", self.position)
                    if element.execute() != 0:
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
        self.position = self.peekTokenPosition()

        while(self.peekTokenType() == "LOGICAL_AND"):
            self.popToken()
            self.children.append(LogicalCompareNode(self.tokens))

    def execute(self):
        if len(self.children) == 1:
            return self.children[0].execute()
        else:
            for element in self.children:
                if element.__class__ != Token:
                    if isinstance(element.execute(), str):
                        raise_error(
                            "Seems like you are doing a logical AND operation on a string?", self.position)
                    if element.execute() == 0:
                        return 0
            return 1


class LogicalNegationNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []

        self.parse()

    def parse(self):
        self.position = self.peekTokenPosition()

        if(self.peekTokenType() == "LOGICAL_NOT"):
            self.popToken()
            self.children.append(LogicalNot(self.tokens))
        self.children.append(FullMathExpressionNode(self.tokens))

    def execute(self):
        if self.children[0].__class__ == LogicalNot:
            if isinstance(self.children[1].execute(), str):
                raise_error(
                    "Seems like you are doing a logical NOT operation on a string?", self.position)
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
        self.position = self.peekTokenPosition()

        if(self.peekTokenType() in ["EQUAL_TO", "NOT_EQUAL_TO", "LOWER_OR_EQUAL", "GREATER_OR_EQUAL", "LOWER", "GREATER"]):
            self.children.append(self.popToken())
            self.children.append(LogicalNegationNode(self.tokens))

    def execute(self):
        if len(self.children) == 1:
            return self.children[0].execute()

        if isinstance(self.children[0].execute(), str):
            raise_error("Seems like you are comparing a string?",
                        self.position)

        else:
            lvalue = self.children[0].execute()
            rvalue = self.children[2].execute()
            return {
                "EQUAL_TO": lvalue == rvalue,
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
        self.children = []  # args
        self.parse()

    def parse(self):
        self.position = self.peekTokenPosition()

        if(self.peekTokenType() == "IDENTIFIER"):
            self.name = self.popToken().value

        if(self.popToken().type != "LEFT_ROUND"):
            raise_error("Function call seems not to have a (", self.position)

        while(self.peekTokenType() != "RIGHT_ROUND"):
            self.children.append(LogicalOrNode(self.tokens))
            if self.peekTokenType() == "COMMA":
                self.popToken()

        if(self.popToken().type != "RIGHT_ROUND"):
            raise_error("Function call seems not to have a )", self.position)

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
        self.position = self.peekTokenPosition()

        while(self.peekTokenType() in ["PLUS", "MINUS"]):
            self.children.append(self.popToken())
            self.children.append(MultiplicationNode(self.tokens))

    def execute(self):
        self.to_return = self.children[0].execute()

        if len(self.children) > 1:
            for child in self.children:
                if child.__class__ is not Token and isinstance(child.execute(), str):
                    raise_error(
                        "Seems like you are trying to do a math operation on a string", self.position)

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
        self.position = self.peekTokenPosition()

        while(self.peekTokenType() in ["MULTIPLICATION", "DIVISION"]):
            self.children.append(self.popToken())
            self.children.append(PartMathExpressionNode(self.tokens))

    def execute(self):
        self.to_return = self.children[0].execute()

        if len(self.children) > 1:
            for child in self.children:
                if child.__class__ is not Token and isinstance(child.execute(), str):
                    raise_error(
                        "Seems like you are trying to do a math operation on a string", self.position)

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
        self.position = self.peekTokenPosition()

        if(self.peekTokenType() == "MINUS"):
            self.popToken()
            self.children.append(NegativeNumber(self.tokens))
            self.is_negative = True

        if(self.peekTokenType() == "LEFT_ROUND"):
            self.children.append(BracketedExpression(self.tokens))
        elif(self.peekTokenType() in ["REAL_NUMBER", "NATURAL_NUMBER"]):
            self.children.append(ValueNode(self.tokens))
        elif(self.peekTokenType() == "ROLL"):
            self.children.append(RollNode(self.tokens))
        elif(self.peekTokenType() == "TEXT"):
            self.children.append(TextNode(self.tokens))
        elif(self.peekTokenType() == "IDENTIFIER"):
            if self.tokens[-2].type == "LEFT_ROUND":
                self.children.append(FunctionCallNode(self.tokens))
            else:
                self.children.append(ValueNode(self.tokens))

        if len(self.children) == 0:
            raise_error(
                "PartMathExpressionNode didn't find a proper value", self.position)

        if len(self.children) == 1 and self.children[0].__class__ is NegativeNumber:
            raise_error(
                "PartMathExpressionNode found a minus which wasn't followed by a proper value", self.position)

    def execute(self):
        if self.is_negative:
            if isinstance(self.children[1].execute(), str):
                raise_error(
                    "Seems like you are trying to get a negative of a string", self.position)
            else:
                return -1*self.children[1].execute()
        else:
            return self.children[0].execute()


class TextNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.type = self.peekTokenType()
        self.parse()

    def parse(self):
        self.value = self.popToken().value

    def get_value(self):
        return self.value

    def execute(self):
        return self.value


class ValueNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.type = self.peekTokenType()
        self.parse()

    def parse(self):
        self.position = self.peekTokenPosition()
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
            elif "chosen." in self.value:
                return chosenPlayer.getValue(self.value.replace("chosen.", "player."))
            elif "game." in self.value:
                try:
                    global gameVarDict
                    return gameVarDict[self.value]
                except:
                    raise_error("Variable not found in gamedict - " +
                                self.value, self.position)
            else:
                try:
                    global localVarDict
                    return localVarDict[self.value]
                except:
                    raise_error("Variable not found in vardict - " +
                                self.value, self.position)
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
        self.position = self.peekTokenPosition()

        if self.popToken().type != "LEFT_ROUND":
            raise_error(
                "Bracketed expression seems not to be open", self.position)

        self.children.append(LogicalOrNode(self.tokens))

        if self.popToken().type != "RIGHT_ROUND":
            raise_error(
                "Bracketed expression seems not to be closed", self.position)

    def execute(self):
        return self.children[0].execute()


class PlayersHeaderNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()

    def parse(self):
        self.position = self.peekTokenPosition()

        if self.popToken().type != "PLAYERS":
            raise_error("Missing PLAYERS in PLAYERS. How?", self.position)

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
        self.position = self.peekTokenPosition()

        if self.popToken().type != "GAME":
            raise_error("Missing GAME in GAME. How?", self.position)
        if self.popToken().type != "COLON":
            raise_error("Missing COLON after WIN. How?", self.position)

        while self.peekTokenType() not in header_names:
            self.children.append(VariableInitNode(self.tokens))
            if self.peekTokenType() == "SEMICOLON":
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
        self.position = self.peekTokenPosition()

        if self.popToken().type != "INDIVIDUAL":
            raise_error("Missing INDIVIDUAL in INDIVIDUAL. How?",
                        self.position)
        if self.popToken().type != "COLON":
            raise_error("Missing colon after WIN.", self.position)

        while self.peekTokenType() not in header_names:
            self.children.append(VariableInitNode(self.tokens))
            if self.peekTokenType() == "SEMICOLON":
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
        self.position = self.peekTokenPosition()

        if self.popToken().type != "FUNCTIONS":
            raise_error("Missing FUNCTIONS in FUNCTIONS. How?", self.position)
        if self.popToken().type != "COLON":
            raise_error("Missing colon after FUNCTIONS.", self.position)

        while self.peekTokenType() not in header_names:
            self.children.append(FunctionInitNode(self.tokens))
            if self.peekTokenType() == "SEMICOLON":
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
        self.position = self.peekTokenPosition()

        if self.popToken().type != "RUN":
            raise_error("Missing RUN in RUN. How?", self.position)
        if self.popToken().type != "COLON":
            raise_error("Missing colon after RUN.", self.position)

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
        self.position = self.peekTokenPosition()

        if self.popToken().type != "WIN":
            raise_error("Missing WIN in WIN. How?", self.position)
        if self.popToken().type != "COLON":
            raise_error("Missing colon after WIN.", self.position)
        if self.popToken().type != "LEFT_SQUARE":
            raise_error("Missing [ after WIN:.", self.position)

        self.children.append(Condition(self.tokens))

        if self.popToken().type != "RIGHT_SQUARE":
            raise_error("Missing ] after WIN.", self.position)

    def execute(self):
        global analysedPlayer
        for player in players:
            analysedPlayer = player
            if self.children[0].execute():
                player.printInfo(1)
            else:
                player.printInfo(0)
