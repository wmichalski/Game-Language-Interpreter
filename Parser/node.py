from Lexer.token import Token

class Node():
    def __init__(self, tokens):
        self.tokens = tokens
        self.value = None
        pass

    def peekToken(self):
        return self.tokens[-1].type

    def popToken(self):
        return self.tokens.pop()

    def create_subtree(self, tokens):
        self.tokens = tokens
        if self.peekToken() == "IF":
            return IfNode(self.tokens)

        if self.peekToken() == "LEFT_ROUND":
            return BracketedExpression(self.tokens)

        if self.peekToken() in ["REAL_NUMBER", "NATURAL_NUMBER", "IDENTIFIER", "MINUS", "LOGICAL_NOT"]:
            return LogicalOrNode(self.tokens)


class WhileNode(Node):
    def __init__(self, parent):
        super().__init__(self, parent)
        self.cond = None
        self.body = None

class ForEachPlayerNode(Node):
    def __init__(self, parent):
        super().__init__(self, parent)
        self.cond = None
        self.body = None

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
        if self.popToken() == "RIGHT_ROUND":
            pass
        if self.popToken() == "LEFT_CURLY":
            self.children.append(IfBody(self.tokens))
        if self.popToken() == "RIGHT_CURLY":
            pass
        if self.peekToken() == "ELSE":
            self.popToken() 
            if self.popToken() != "LEFT_CURLY":
                pass
            self.children.append(IfElseBody(self.tokens))
            if self.popToken() != "RIGHT_CURLY":
                pass

class Condition(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse(tokens)
    
    def parse(self, tokens):
        self.children.append(super().create_subtree(self.tokens))

class IfBody(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.children = []
        self.parse(tokens)
    
    def parse(self, tokens):
        self.children.append(super().create_subtree(self.tokens))

class IfElseBody(Node):
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
        # self.players_info = None
        # self.global_values = None
        # self.individual_values = None
        # self.function_declarations = None
        # self.run = None
        # self.win_condition = None
        self.children = []

        self.parse()

    def parse(self):
        self.children.append(super().create_subtree(self.tokens))
        pass

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
        self.roll = None
        self.choices = []

class ChoiceNode(Node):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.cond = None
        self.body = None

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

