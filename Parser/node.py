from Lexer.token import Token, header_names

class Node():
    def __init__(self, tokens):
        self.tokens = tokens
        self.value = None
        pass

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

        return doNothing(self.tokens)
        
class doNothing(Node):
    def __init__(self, tokens):
        super().__init__(tokens)

class WhileNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()

    def parse(self):
        if self.popToken() != "WHILE":
            pass
        if self.popToken() != "LEFT_ROUND":
            pass
        self.children.append(Condition(self.tokens))
        if self.popToken() != "RIGHT_ROUND":
            pass
        if self.popToken() != "LEFT_CURLY":
            pass
        self.children.append(BlockOfCode(self.tokens))
        if self.popToken() == "RIGHT_CURLY":
            pass

# class WhileBody(Node):
#     def __init__(self, tokens):
#         super().__init__(tokens)
#         self.children = []
#         self.parse()
    
#     def parse(self):
#         self.children.append(super().create_subtree(self.tokens)) 

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

class RollNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()
    
    def parse(self):
        self.popToken() # ROLL
        if self.popToken() != "LEFT_ROUND":
            pass
        self.children.append(super().create_subtree(self.tokens)) 
        if self.popToken() == "RIGHT_ROUND":
            pass
        

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
        if self.popToken() != "VAR":
            pass
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
            pass
        if(self.peekToken() == "IDENTIFIER"):
            self.name = self.popToken().value
        if(self.popToken().type != "LEFT_ROUND"):
            pass
        while(self.peekToken() != "RIGHT_ROUND"):
            self.children.append(self.popToken())
            if self.peekToken() == "COMMA":
                self.popToken()
        if(self.popToken().type != "RIGHT_ROUND"):
            pass

        if(self.popToken().type != "LEFT_CURLY"):
            pass
        self.children.append(BlockOfCode(self.tokens))
        if(self.popToken().type != "RIGHT_CURLY"):
            pass

    def get_name(self):
        return self.name


class ForEachPlayerNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()

    def parse(self):
        if self.popToken() != "FOR_EACH_PLAYER":
            pass
        if self.popToken() != "LEFT_ROUND":
            pass
        self.children.append(Condition(self.tokens))
        if self.popToken() == "RIGHT_ROUND":
            pass
        if self.popToken() == "LEFT_CURLY":
            pass
        self.children.append(BlockOfCode(self.tokens))
        if self.popToken() == "RIGHT_CURLY":
            pass

class IfNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()

    def parse(self):
        if self.popToken() != "IF":
            pass
        if self.popToken() != "LEFT_ROUND":
            pass
        self.children.append(Condition(self.tokens))
        if self.popToken() != "RIGHT_ROUND":
            pass
        if self.popToken() != "LEFT_CURLY":
            pass
        self.children.append(BlockOfCode(self.tokens))
        if self.popToken() == "RIGHT_CURLY":
            pass
        if self.peekToken() == "ELSE":
            self.popToken() 
            if self.popToken() != "LEFT_CURLY":
                pass
            self.children.append(BlockOfCode(self.tokens))
            if self.popToken() != "RIGHT_CURLY":
                pass

class Condition(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse(tokens)
    
    def parse(self, tokens):
        self.children.append(super().create_subtree(self.tokens))

# class IfBody(Node):
#     def __init__(self, tokens):
#         super().__init__(tokens)
#         self.children = []
#         self.parse(tokens)
    
#     def parse(self, tokens):
#         self.children.append(super().create_subtree(self.tokens))

# class IfElseBody(Node):
#     def __init__(self, tokens):
#         super().__init__(tokens)
#         self.children = []
#         self.parse(tokens)
    
#     def parse(self, tokens):
#         self.children.append(super().create_subtree(self.tokens))

class ProgramNode(Node):
    # note for self: ignore "RUN:" tokens etc
    def __init__(self, tokens):
        super().__init__(tokens)
        # self.players_info = None
        # self.global_values = None
        # self.individual_values = None
        # self.function_declarations = None
        # self.run = None
        # self.win_condition = None
        self.children = []

        self.parse()

    def parse(self):
        while(self.peekToken() != "END_OF_FILE"):
            self.children.append(super().create_subtree(self.tokens))

# class AssignmentNode(Node):
#     def __init__(self, left):
#         super().__init__(tokens)
#         self.left = left
#         self.right = None
#         self.parse()

#     def parse(self):
#         if self.popToken() != "ASSIGNMENT":
#             pass
#         self.right = super().create_subtree(self.tokens)

class ChoiceStatementNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()
    
    def parse(self):
        self.popToken() # CHOICE
        if self.popToken() != "LEFT_ROUND":
            pass
        self.children.append(super().create_subtree(self.tokens))
        if self.popToken() != "RIGHT_ROUND":
            pass
        if self.popToken() != "LEFT_CURLY":
            pass
        while self.peekToken() != "RIGHT_CURLY":
            self.children.append(ChoiceNode(self.tokens))
        if self.popToken() != "RIGHT_CURLY":
            pass

class ChoiceNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []

        self.parse()

    def parse(self):
        if self.popToken() != "LEFT_SQUARE":
            pass
        self.children.append(Condition(self.tokens))
        if self.popToken() != "RIGHT_SQUARE":
            pass
        if self.popToken() != "LEFT_CURLY":
            pass
        self.children.append(BlockOfCode(self.tokens))
        if self.popToken() != "RIGHT_CURLY":
            pass



class FunctionNode(Node):
    def __init__(self, parent):
        super().__init__(self)
        self.name = None
        self.args = None
        self.body = None

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
            pass
        while(self.peekToken() != "RIGHT_ROUND"):
            self.children.append(super().create_subtree(self.tokens))
            if self.peekToken() == "COMMA":
                self.popToken()
        if(self.popToken().type != "RIGHT_ROUND"):
            pass

    def get_name(self):
        return self.name

# class ReturnNode(Node):
#     def __init__(self, parent):
#         super().__init__(self)
#         self.expression = None

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
        if self.popToken() == "LEFT_ROUND":
            pass
        self.children.append(super().create_subtree(self.tokens))
        if self.popToken() == "RIGHT_ROUND":
            pass

class PlayersHeaderNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()

    def parse(self):
        if self.popToken() != "PLAYERS":
            pass
        
        self.children.append(super().create_subtree(self.tokens))

class GameHeaderNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()

    def parse(self):
        if self.popToken() != "GAME":
            pass
        if self.popToken() != "COLON":
            pass
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
        if self.popToken() != "INDIVIDUAL":
            pass
        if self.popToken() != "COLON":
            pass
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
        if self.popToken() != "FUNCTIONS":
            pass
        if self.popToken() != "COLON":
            pass
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
        if self.popToken() != "RUN":
            pass
        if self.popToken() != "COLON":
            pass
        self.children.append(BlockOfCode(self.tokens))

class WinHeaderNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse()

    def parse(self):
        if self.popToken() != "WIN":
            pass
        if self.popToken() != "COLON":
            pass
        if self.popToken() != "[":
            pass
        self.children.append(Condition(self.tokens))
        if self.popToken() != "]":
            pass
