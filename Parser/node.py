from Lexer.token import Token, header_names

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

class WhileNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()

    def parse(self):
        if self.popToken().type != "WHILE":
            raise SyntaxError("WHILE seems not to have a WHILE. How?")
        if self.popToken().type != "LEFT_ROUND":
            raise SyntaxError("ROLL seems not to have a (")

        self.children.append(Condition(self.tokens))

        if self.popToken().type != "RIGHT_ROUND":
            raise SyntaxError("ROLL seems not to have a )")
        if self.popToken().type != "LEFT_CURLY":
            raise SyntaxError("ROLL seems not to have a {")

        self.children.append(BlockOfCode(self.tokens))

        if self.popToken() == "RIGHT_CURLY":
            raise SyntaxError("ROLL seems not to have a }")

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
        

class BreakNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)

        self.parse()

    def parse(self):
        self.popToken()

class ReturnNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()

    def parse(self):
        self.popToken() # RETURN
        self.children.append(super().create_subtree(self.tokens)) 

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

class Condition(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse(tokens)
    
    def parse(self, tokens):
        self.children.append(super().create_subtree(self.tokens))

class ProgramNode(Node):
    # note for self: ignore "RUN:" tokens etc
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []

        self.parse()

    def parse(self):
        while(self.peekToken() != "END_OF_FILE"):
            self.children.append(super().create_subtree(self.tokens))

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

        # if len(self.children) == 1:
        #     self.children = list(self.children[0].children)


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

        # if len(self.children) == 1:
        #     self.children = list(self.children[0].children)

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

        # if len(self.children) == 1:
        #     try:
        #         self.children = list(self.children[0].children)
        #     except:
        #         pass

    


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

        if(self.peekToken() == "LEFT_ROUND"):
            self.children.append(BracketedExpression(self.tokens))
        elif(self.peekToken() in ["REAL_NUMBER", "NATURAL_NUMBER"]):
            self.value = self.popToken().value
        elif(self.peekToken() == "ROLL"):
            self.children.append(RollNode(self.tokens))
        elif(self.peekToken() == "IDENTIFIER"):
            if self.tokens[-2].type == "LEFT_ROUND":
                self.children.append(FunctionCallNode(self.tokens))
            else:
                self.value = self.popToken().value

    def get_value(self):
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

class PlayersHeaderNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()

    def parse(self):
        if self.popToken().type != "PLAYERS":
            raise SyntaxError("Missing PLAYERS in PLAYERS. How?")
        
        self.children.append(super().create_subtree(self.tokens))

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
