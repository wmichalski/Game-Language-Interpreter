import unittest
import os
import io
from contextlib import redirect_stdout

from unittest.mock import patch, mock_open

from Lexer.file_manager import FileManager
from Lexer.tokeniser import Tokeniser
from Lexer.token import Token
from Parser.node import *

class AcceptanceScriptTester(unittest.TestCase):
    def compare_output(self, expected, result):
        self.assertEqual(expected, result)


    def print_tree(self, node, depth):
        if node.__class__ == Token:
            print("| " * (depth) + "└ " + node.__class__.__name__ + " [" + node.value + "]")
        else:
            print("| " * (depth) + "└ " + node.__class__.__name__, end="")
            self.print_node_name(node)
            self.print_node_value(node)
            print("")

        try:
            for child in node.children:
                print_tree(child, depth+1)
        except:
            pass

    def print_node_name(self, node):
        try:
            name = node.get_name()
            print(" [" + name + "]", end="")
        except:
            pass

    def print_node_value(self, node):
        try:
            value = node.get_value()
            print(" [" + str(value) + "]", end="")
        except:
            pass

    def test_fibonacci(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            with FileManager("Testing/Final_Test_Cases/fibonacci.txt") as file_manager:
                tokeniser = Tokeniser(file_manager)
                analysed_tokens = []
                analysed_tokens.append(Token("START_OF_FILE", "", 0))
                while (analysed_tokens[-1].type is not "END_OF_FILE"):
                    analysed_tokens.append(tokeniser.get_token())

                analysed_tokens = analysed_tokens[1:]

                parsed = ProgramNode(analysed_tokens[::-1], file_manager)
                self.print_tree(parsed, 0)

                solution = """└ ProgramNode
| └ FunctionInitNode [fib]
| | └ Token [n]
| | └ BlockOfCode
| | | └ IfNode
| | | | └ Condition
| | | | | └ LogicalOrNode
| | | | | | └ LogicalAndNode
| | | | | | | └ LogicalCompareNode
| | | | | | | | └ LogicalNegationNode
| | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | └ ValueNode [n]
| | | | | | | | └ Token [<]
| | | | | | | | └ LogicalNegationNode
| | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | └ ValueNode [3]
| | | | └ BlockOfCode
| | | | | └ ReturnNode
| | | | | | └ LogicalOrNode
| | | | | | | └ LogicalAndNode
| | | | | | | | └ LogicalCompareNode
| | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | └ ValueNode [1]
| | | └ ReturnNode
| | | | └ LogicalOrNode
| | | | | └ LogicalAndNode
| | | | | | └ LogicalCompareNode
| | | | | | | └ LogicalNegationNode
| | | | | | | | └ FullMathExpressionNode
| | | | | | | | | └ MultiplicationNode
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ FunctionCallNode [fib]
| | | | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | └ ValueNode [n]
| | | | | | | | | | | | | | | | | └ Token [-]
| | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | └ ValueNode [2]
| | | | | | | | | └ Token [+]
| | | | | | | | | └ MultiplicationNode
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ FunctionCallNode [fib]
| | | | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | └ ValueNode [n]
| | | | | | | | | | | | | | | | | └ Token [-]
| | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | └ ValueNode [1]
| └ VariableInitNode [i]
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [1]
| └ WhileNode
| | └ Condition
| | | └ LogicalOrNode
| | | | └ LogicalAndNode
| | | | | └ LogicalCompareNode
| | | | | | └ LogicalNegationNode
| | | | | | | └ FullMathExpressionNode
| | | | | | | | └ MultiplicationNode
| | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | └ ValueNode [i]
| | | | | | └ Token [<]
| | | | | | └ LogicalNegationNode
| | | | | | | └ FullMathExpressionNode
| | | | | | | | └ MultiplicationNode
| | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | └ ValueNode [12]
| | └ BlockOfCode
| | | └ PrintNode
| | | | └ LogicalOrNode
| | | | | └ LogicalAndNode
| | | | | | └ LogicalCompareNode
| | | | | | | └ LogicalNegationNode
| | | | | | | | └ FullMathExpressionNode
| | | | | | | | | └ MultiplicationNode
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ FunctionCallNode [fib]
| | | | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | └ ValueNode [i]
| | | └ VariableAssignmentNode [i]
| | | | └ LogicalOrNode
| | | | | └ LogicalAndNode
| | | | | | └ LogicalCompareNode
| | | | | | | └ LogicalNegationNode
| | | | | | | | └ FullMathExpressionNode
| | | | | | | | | └ MultiplicationNode
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ ValueNode [i]
| | | | | | | | | └ Token [+]
| | | | | | | | | └ MultiplicationNode
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ ValueNode [1]"""

                for line_sol, line_test in zip(solution.rstrip('\r'), buf.getvalue().rstrip('\r')):
                    self.compare_output(line_sol, line_test)


    def test_add_function(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            with FileManager("Testing/Final_Test_Cases/add_function.txt") as file_manager:
                tokeniser = Tokeniser(file_manager)
                analysed_tokens = []
                analysed_tokens.append(Token("START_OF_FILE", "", 0))
                while (analysed_tokens[-1].type is not "END_OF_FILE"):
                    analysed_tokens.append(tokeniser.get_token())

                analysed_tokens = analysed_tokens[1:]

                parsed = ProgramNode(analysed_tokens[::-1], file_manager)
                self.print_tree(parsed, 0)

                solution = """└ ProgramNode
| └ FunctionInitNode [add]
| | └ Token [c]
| | └ Token [d]
| | └ BlockOfCode
| | | └ ReturnNode
| | | | └ LogicalOrNode
| | | | | └ LogicalAndNode
| | | | | | └ LogicalCompareNode
| | | | | | | └ LogicalNegationNode
| | | | | | | | └ FullMathExpressionNode
| | | | | | | | | └ MultiplicationNode
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ BracketedExpression
| | | | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | └ ValueNode [c]
| | | | | | | | | | | | | | | | | └ Token [+]
| | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | └ ValueNode [d]
| └ VariableInitNode [a]
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [2]
| └ VariableInitNode [b]
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [3]
| └ PrintNode
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ FunctionCallNode [add]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [a]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [b]"""

                for line_sol, line_test in zip(solution.rstrip('\r'), buf.getvalue().rstrip('\r')):
                    self.compare_output(line_sol, line_test)


    def test_break(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            with FileManager("Testing/Final_Test_Cases/break_in_nested_while.txt") as file_manager:
                tokeniser = Tokeniser(file_manager)
                analysed_tokens = []
                analysed_tokens.append(Token("START_OF_FILE", "", 0))
                while (analysed_tokens[-1].type is not "END_OF_FILE"):
                    analysed_tokens.append(tokeniser.get_token())

                analysed_tokens = analysed_tokens[1:]

                parsed = ProgramNode(analysed_tokens[::-1], file_manager)
                self.print_tree(parsed, 0)

                solution = """└ ProgramNode
| └ RunHeaderNode
| | └ BlockOfCode
| | | └ VariableInitNode [a]
| | | | └ LogicalOrNode
| | | | | └ LogicalAndNode
| | | | | | └ LogicalCompareNode
| | | | | | | └ LogicalNegationNode
| | | | | | | | └ FullMathExpressionNode
| | | | | | | | | └ MultiplicationNode
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ ValueNode [1]
| | | └ VariableInitNode [b]
| | | | └ LogicalOrNode
| | | | | └ LogicalAndNode
| | | | | | └ LogicalCompareNode
| | | | | | | └ LogicalNegationNode
| | | | | | | | └ FullMathExpressionNode
| | | | | | | | | └ MultiplicationNode
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ ValueNode [1]
| | | └ WhileNode
| | | | └ Condition
| | | | | └ LogicalOrNode
| | | | | | └ LogicalAndNode
| | | | | | | └ LogicalCompareNode
| | | | | | | | └ LogicalNegationNode
| | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | └ ValueNode [a]
| | | | | | | | └ Token [<]
| | | | | | | | └ LogicalNegationNode
| | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | └ ValueNode [4]
| | | | └ BlockOfCode
| | | | | └ VariableAssignmentNode [a]
| | | | | | └ LogicalOrNode
| | | | | | | └ LogicalAndNode
| | | | | | | | └ LogicalCompareNode
| | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | └ ValueNode [a]
| | | | | | | | | | | └ Token [+]
| | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | └ ValueNode [1]
| | | | | └ VariableAssignmentNode [b]
| | | | | | └ LogicalOrNode
| | | | | | | └ LogicalAndNode
| | | | | | | | └ LogicalCompareNode
| | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | └ ValueNode [1]
| | | | | └ WhileNode
| | | | | | └ Condition
| | | | | | | └ LogicalOrNode
| | | | | | | | └ LogicalAndNode
| | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | └ ValueNode [b]
| | | | | | | | | | └ Token [<]
| | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | └ ValueNode [100000]
| | | | | | └ BlockOfCode
| | | | | | | └ PrintNode
| | | | | | | | └ LogicalOrNode
| | | | | | | | | └ LogicalAndNode
| | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | └ ValueNode [b]
| | | | | | | └ VariableAssignmentNode [b]
| | | | | | | | └ LogicalOrNode
| | | | | | | | | └ LogicalAndNode
| | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | └ ValueNode [b]
| | | | | | | | | | | | | | └ Token [*]
| | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | └ ValueNode [10]
| | | | | | | └ IfNode
| | | | | | | | └ Condition
| | | | | | | | | └ LogicalOrNode
| | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | └ ValueNode [b]
| | | | | | | | | | | | └ Token [==]
| | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | └ ValueNode [1000]
| | | | | | | | └ BlockOfCode
| | | | | | | | | └ BreakNode"""

                for line_sol, line_test in zip(solution.rstrip('\r'), buf.getvalue().rstrip('\r')):
                    self.compare_output(line_sol, line_test)


    def test_dividemultiply(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            with FileManager("Testing/Final_Test_Cases/dividemultiply.txt") as file_manager:
                tokeniser = Tokeniser(file_manager)
                analysed_tokens = []
                analysed_tokens.append(Token("START_OF_FILE", "", 0))
                while (analysed_tokens[-1].type is not "END_OF_FILE"):
                    analysed_tokens.append(tokeniser.get_token())

                analysed_tokens = analysed_tokens[1:]

                parsed = ProgramNode(analysed_tokens[::-1], file_manager)
                self.print_tree(parsed, 0)

                solution = """└ ProgramNode
| └ FunctionInitNode [divideBy]
| | └ Token [x]
| | └ Token [y]
| | └ BlockOfCode
| | | └ VariableInitNode [z]
| | | | └ LogicalOrNode
| | | | | └ LogicalAndNode
| | | | | | └ LogicalCompareNode
| | | | | | | └ LogicalNegationNode
| | | | | | | | └ FullMathExpressionNode
| | | | | | | | | └ MultiplicationNode
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ ValueNode [x]
| | | | | | | | | | └ Token [/]
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ ValueNode [y]
| | | └ ReturnNode
| | | | └ LogicalOrNode
| | | | | └ LogicalAndNode
| | | | | | └ LogicalCompareNode
| | | | | | | └ LogicalNegationNode
| | | | | | | | └ FullMathExpressionNode
| | | | | | | | | └ MultiplicationNode
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ ValueNode [z]
| └ FunctionInitNode [multiplyBy]
| | └ Token [x]
| | └ Token [y]
| | └ BlockOfCode
| | | └ VariableInitNode [z]
| | | | └ LogicalOrNode
| | | | | └ LogicalAndNode
| | | | | | └ LogicalCompareNode
| | | | | | | └ LogicalNegationNode
| | | | | | | | └ FullMathExpressionNode
| | | | | | | | | └ MultiplicationNode
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ FunctionCallNode [divideBy]
| | | | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | └ ValueNode [1]
| | | | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | └ ValueNode [y]
| | | └ ReturnNode
| | | | └ LogicalOrNode
| | | | | └ LogicalAndNode
| | | | | | └ LogicalCompareNode
| | | | | | | └ LogicalNegationNode
| | | | | | | | └ FullMathExpressionNode
| | | | | | | | | └ MultiplicationNode
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ ValueNode [x]
| | | | | | | | | | └ Token [/]
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ ValueNode [z]
| └ VariableInitNode [a]
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [5]
| └ VariableInitNode [b]
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [4]
| └ PrintNode
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ FunctionCallNode [divideBy]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [a]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [b]
| └ PrintNode
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ FunctionCallNode [multiplyBy]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [a]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [b]"""

                for line_sol, line_test in zip(solution.rstrip('\r'), buf.getvalue().rstrip('\r')):
                    self.compare_output(line_sol, line_test)


    def test_nwd(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            with FileManager("Testing/Final_Test_Cases/recursive_nwd.txt") as file_manager:
                tokeniser = Tokeniser(file_manager)
                analysed_tokens = []
                analysed_tokens.append(Token("START_OF_FILE", "", 0))
                while (analysed_tokens[-1].type is not "END_OF_FILE"):
                    analysed_tokens.append(tokeniser.get_token())

                analysed_tokens = analysed_tokens[1:]

                parsed = ProgramNode(analysed_tokens[::-1], file_manager)
                self.print_tree(parsed, 0)

                solution = """└ ProgramNode
| └ FunctionInitNode [nwd]
| | └ Token [c]
| | └ Token [d]
| | └ BlockOfCode
| | | └ IfNode
| | | | └ Condition
| | | | | └ LogicalOrNode
| | | | | | └ LogicalAndNode
| | | | | | | └ LogicalCompareNode
| | | | | | | | └ LogicalNegationNode
| | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | └ ValueNode [c]
| | | | | | | | └ Token [!=]
| | | | | | | | └ LogicalNegationNode
| | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | └ ValueNode [d]
| | | | └ BlockOfCode
| | | | | └ IfNode
| | | | | | └ Condition
| | | | | | | └ LogicalOrNode
| | | | | | | | └ LogicalAndNode
| | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | └ ValueNode [c]
| | | | | | | | | | └ Token [>]
| | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | └ ValueNode [d]
| | | | | | └ BlockOfCode
| | | | | | | └ ReturnNode
| | | | | | | | └ LogicalOrNode
| | | | | | | | | └ LogicalAndNode
| | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | └ FunctionCallNode [nwd]
| | | | | | | | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | | | | | └ ValueNode [c]
| | | | | | | | | | | | | | | | | | | | | └ Token [-]
| | | | | | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | | | | | └ ValueNode [d]
| | | | | | | | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | | | | | └ ValueNode [d]
| | | | | | └ BlockOfCode
| | | | | | | └ ReturnNode
| | | | | | | | └ LogicalOrNode
| | | | | | | | | └ LogicalAndNode
| | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | └ FunctionCallNode [nwd]
| | | | | | | | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | | | | | └ ValueNode [c]
| | | | | | | | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | | | | | └ ValueNode [d]
| | | | | | | | | | | | | | | | | | | | | └ Token [-]
| | | | | | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | | | | | └ ValueNode [c]
| | | | └ BlockOfCode
| | | | | └ ReturnNode
| | | | | | └ LogicalOrNode
| | | | | | | └ LogicalAndNode
| | | | | | | | └ LogicalCompareNode
| | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | └ ValueNode [c]
| └ PrintNode
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ FunctionCallNode [nwd]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [28]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [70]
| └ PrintNode
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ FunctionCallNode [nwd]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [1]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [12]
| └ PrintNode
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ FunctionCallNode [nwd]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [66]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [102]
| └ PrintNode
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ FunctionCallNode [nwd]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [12]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [18]
| └ PrintNode
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ FunctionCallNode [nwd]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [10000]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [1000]
| └ PrintNode
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ FunctionCallNode [nwd]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [8941]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [785]
| └ PrintNode
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ FunctionCallNode [nwd]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [785]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [8941]"""

                for line_sol, line_test in zip(solution.rstrip('\r'), buf.getvalue().rstrip('\r')):
                    self.compare_output(line_sol, line_test)

    def test_power(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            with FileManager("Testing/Final_Test_Cases/recursive_power.txt") as file_manager:
                tokeniser = Tokeniser(file_manager)
                analysed_tokens = []
                analysed_tokens.append(Token("START_OF_FILE", "", 0))
                while (analysed_tokens[-1].type is not "END_OF_FILE"):
                    analysed_tokens.append(tokeniser.get_token())

                analysed_tokens = analysed_tokens[1:]

                parsed = ProgramNode(analysed_tokens[::-1], file_manager)
                self.print_tree(parsed, 0)

                solution = """└ ProgramNode
| └ FunctionInitNode [power]
| | └ Token [base]
| | └ Token [exp]
| | └ BlockOfCode
| | | └ IfNode
| | | | └ Condition
| | | | | └ LogicalOrNode
| | | | | | └ LogicalAndNode
| | | | | | | └ LogicalCompareNode
| | | | | | | | └ LogicalNegationNode
| | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | └ ValueNode [exp]
| | | | | | | | └ Token [>]
| | | | | | | | └ LogicalNegationNode
| | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | └ ValueNode [0]
| | | | └ BlockOfCode
| | | | | └ ReturnNode
| | | | | | └ LogicalOrNode
| | | | | | | └ LogicalAndNode
| | | | | | | | └ LogicalCompareNode
| | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | └ ValueNode [base]
| | | | | | | | | | | | └ Token [*]
| | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | └ FunctionCallNode [power]
| | | | | | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | | | └ ValueNode [base]
| | | | | | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | | | └ ValueNode [exp]
| | | | | | | | | | | | | | | | | | | └ Token [-]
| | | | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | | | └ ValueNode [1]
| | | | └ BlockOfCode
| | | | | └ ReturnNode
| | | | | | └ LogicalOrNode
| | | | | | | └ LogicalAndNode
| | | | | | | | └ LogicalCompareNode
| | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | └ ValueNode [1]
| └ VariableInitNode [a]
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ FunctionCallNode [power]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [2]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [3]
| └ PrintNode
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [a]
| └ VariableInitNode [b]
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ FunctionCallNode [power]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [3]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [2]
| └ PrintNode
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [b]
| └ VariableInitNode [c]
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [3]
| | | | | | | | └ Token [*]
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ FunctionCallNode [power]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [10]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [2]
| | | | | | | └ Token [+]
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [1]
| | | | | | | | └ Token [*]
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ FunctionCallNode [power]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [16]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [0]
| | | | | | | └ Token [+]
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ FunctionCallNode [power]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [2]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [6]
| └ PrintNode
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [c]
| └ PrintNode
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ FunctionCallNode [power]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ FunctionCallNode [power]
| | | | | | | | | | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | | | | | | | └ ValueNode [2]
| | | | | | | | | | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | | | | | | | └ ValueNode [3]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [2]"""

                for line_sol, line_test in zip(solution.rstrip('\r'), buf.getvalue().rstrip('\r')):
                    self.compare_output(line_sol, line_test)

    def test_math(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            with FileManager("Testing/Final_Test_Cases/complex_math.txt") as file_manager:
                tokeniser = Tokeniser(file_manager)
                analysed_tokens = []
                analysed_tokens.append(Token("START_OF_FILE", "", 0))
                while (analysed_tokens[-1].type is not "END_OF_FILE"):
                    analysed_tokens.append(tokeniser.get_token())

                analysed_tokens = analysed_tokens[1:]

                parsed = ProgramNode(analysed_tokens[::-1], file_manager)
                self.print_tree(parsed, 0)

                solution = """└ ProgramNode
| └ PrintNode
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [2]
| | | | | | | └ Token [+]
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [2]
| | | | | | | | └ Token [*]
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [2]
| └ PrintNode
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [2]
| | | | | | | | └ Token [*]
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [2]
| | | | | | | └ Token [+]
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [2]
| └ PrintNode
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [2]
| | | | | | | | └ Token [*]
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ BracketedExpression
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [2]
| | | | | | | | | | | | | | | └ Token [+]
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [2]
| └ PrintNode
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ BracketedExpression
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ BracketedExpression
| | | | | | | | | | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | | | | | | | └ ValueNode [2]
| | | | | | | | └ Token [*]
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ BracketedExpression
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ BracketedExpression
| | | | | | | | | | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | | | | | | | └ ValueNode [2]
| | | | | | | | | | | | | | | | | | | | | | | └ Token [+]
| | | | | | | | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | | | | | | | └ ValueNode [2]
| └ PrintNode
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [2]
| | | | | | | └ Token [-]
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [2]
| | | | | | | └ Token [-]
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [2]
| └ PrintNode
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [2]
| | | | | | | └ Token [-]
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ BracketedExpression
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ NegativeNumber
| | | | | | | | | | | | | | | | | └ BracketedExpression
| | | | | | | | | | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | | | | | | | └ NegativeNumber
| | | | | | | | | | | | | | | | | | | | | | | | | └ ValueNode [2]
| └ PrintNode
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [2]
| | | | | | | | └ Token [*]
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ BracketedExpression
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [100]
| | | | | | | | | | | | | | | └ Token [-]
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [3]
| | | | | | | | └ Token [*]
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [100]
| | | | | | | └ Token [-]
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [3]"""

                for line_sol, line_test in zip(solution.rstrip('\r'), buf.getvalue().rstrip('\r')):
                    self.compare_output(line_sol, line_test)

    def test_10_players(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            with FileManager("Testing/Final_Test_Cases/10_players.txt") as file_manager:
                tokeniser = Tokeniser(file_manager)
                analysed_tokens = []
                analysed_tokens.append(Token("START_OF_FILE", "", 0))
                while (analysed_tokens[-1].type is not "END_OF_FILE"):
                    analysed_tokens.append(tokeniser.get_token())

                analysed_tokens = analysed_tokens[1:]

                parsed = ProgramNode(analysed_tokens[::-1], file_manager)
                self.print_tree(parsed, 0)

                solution = """└ ProgramNode
| └ PlayersHeaderNode
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [10]
| └ GameHeaderNode
| | └ VariableInitNode [game.tokens]
| | | └ LogicalOrNode
| | | | └ LogicalAndNode
| | | | | └ LogicalCompareNode
| | | | | | └ LogicalNegationNode
| | | | | | | └ FullMathExpressionNode
| | | | | | | | └ MultiplicationNode
| | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | └ ValueNode [10]
| | └ VariableInitNode [game.finished]
| | | └ LogicalOrNode
| | | | └ LogicalAndNode
| | | | | └ LogicalCompareNode
| | | | | | └ LogicalNegationNode
| | | | | | | └ FullMathExpressionNode
| | | | | | | | └ MultiplicationNode
| | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | └ ValueNode [0]
| └ IndividualHeaderNode
| | └ VariableInitNode [player.xD]
| | | └ LogicalOrNode
| | | | └ LogicalAndNode
| | | | | └ LogicalCompareNode
| | | | | | └ LogicalNegationNode
| | | | | | | └ FullMathExpressionNode
| | | | | | | | └ MultiplicationNode
| | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | └ ValueNode [1]
| └ RunHeaderNode
| | └ BlockOfCode
| | | └ VariableInitNode [finished]
| | | | └ LogicalOrNode
| | | | | └ LogicalAndNode
| | | | | | └ LogicalCompareNode
| | | | | | | └ LogicalNegationNode
| | | | | | | | └ FullMathExpressionNode
| | | | | | | | | └ MultiplicationNode
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ ValueNode [0]
| | | └ WhileNode
| | | | └ Condition
| | | | | └ LogicalOrNode
| | | | | | └ LogicalAndNode
| | | | | | | └ LogicalCompareNode
| | | | | | | | └ LogicalNegationNode
| | | | | | | | | └ LogicalNot
| | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | └ ValueNode [finished]
| | | | └ BlockOfCode
| | | | | └ ForEachPlayerNode
| | | | | | └ Condition
| | | | | | | └ LogicalOrNode
| | | | | | | | └ LogicalAndNode
| | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | └ ValueNode [1]
| | | | | | └ BlockOfCode
| | | | | | | └ VariableInitNode [rolledx]
| | | | | | | | └ LogicalOrNode
| | | | | | | | | └ LogicalAndNode
| | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | └ ValueNode [0]
| | | | | | | └ WhileNode
| | | | | | | | └ Condition
| | | | | | | | | └ LogicalOrNode
| | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | └ ValueNode [rolledx]
| | | | | | | | | | | | └ Token [<]
| | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | └ ValueNode [5]
| | | | | | | | └ BlockOfCode
| | | | | | | | | └ VariableAssignmentNode [rolledx]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ RollNode
| | | | | | | | | | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | | | | | | | └ ValueNode [10]
| | | | | | | └ VariableAssignmentNode [player.xD]
| | | | | | | | └ LogicalOrNode
| | | | | | | | | └ LogicalAndNode
| | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | └ ValueNode [player.xD]
| | | | | | | | | | | | | └ Token [+]
| | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | └ ValueNode [rolledx]
| | | | | | | └ PrintNode
| | | | | | | | └ LogicalOrNode
| | | | | | | | | └ LogicalAndNode
| | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | └ ValueNode [player.name]
| | | | | | | └ PrintNode
| | | | | | | | └ LogicalOrNode
| | | | | | | | | └ LogicalAndNode
| | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | └ ValueNode [player.xD]
| | | | | | | └ IfNode
| | | | | | | | └ Condition
| | | | | | | | | └ LogicalOrNode
| | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | └ ValueNode [player.xD]
| | | | | | | | | | | | └ Token [>]
| | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | └ ValueNode [20]
| | | | | | | | └ BlockOfCode
| | | | | | | | | └ VariableAssignmentNode [finished]
| | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | └ ValueNode [1]
| | | | | | | | | └ BreakNode
| | | | | └ PrintNode
| | | | | | └ LogicalOrNode
| | | | | | | └ LogicalAndNode
| | | | | | | | └ LogicalCompareNode
| | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | └ TextNode [--]
| └ WinHeaderNode
| | └ Condition
| | | └ LogicalOrNode
| | | | └ LogicalAndNode
| | | | | └ LogicalCompareNode
| | | | | | └ LogicalNegationNode
| | | | | | | └ FullMathExpressionNode
| | | | | | | | └ MultiplicationNode
| | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | └ ValueNode [player.xD]
| | | | | | └ Token [>]
| | | | | | └ LogicalNegationNode
| | | | | | | └ FullMathExpressionNode
| | | | | | | | └ MultiplicationNode
| | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | └ ValueNode [20]"""

                for line_sol, line_test in zip(solution.rstrip('\r'), buf.getvalue().rstrip('\r')):
                    self.compare_output(line_sol, line_test)

    def test_choice(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            with FileManager("Testing/Final_Test_Cases/choice.txt") as file_manager:
                tokeniser = Tokeniser(file_manager)
                analysed_tokens = []
                analysed_tokens.append(Token("START_OF_FILE", "", 0))
                while (analysed_tokens[-1].type is not "END_OF_FILE"):
                    analysed_tokens.append(tokeniser.get_token())

                analysed_tokens = analysed_tokens[1:]

                parsed = ProgramNode(analysed_tokens[::-1], file_manager)
                self.print_tree(parsed, 0)

                solution = """└ ProgramNode
| └ PlayersHeaderNode
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [3]
| └ VariableInitNode [player.tokens]
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [15]
| └ VariableInitNode [player.won]
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [0]
| └ VariableInitNode [game.over]
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [0]
| └ FunctionInitNode [isGameOver]
| | └ BlockOfCode
| | | └ ForEachPlayerNode
| | | | └ Condition
| | | | | └ LogicalOrNode
| | | | | | └ LogicalAndNode
| | | | | | | └ LogicalCompareNode
| | | | | | | | └ LogicalNegationNode
| | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | └ ValueNode [1]
| | | | └ BlockOfCode
| | | | | └ IfNode
| | | | | | └ Condition
| | | | | | | └ LogicalOrNode
| | | | | | | | └ LogicalAndNode
| | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | └ ValueNode [player.tokens]
| | | | | | | | | | └ Token [<]
| | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | └ ValueNode [0]
| | | | | | └ BlockOfCode
| | | | | | | └ ReturnNode
| | | | | | | | └ LogicalOrNode
| | | | | | | | | └ LogicalAndNode
| | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | └ ValueNode [1]
| | | └ ReturnNode
| | | | └ LogicalOrNode
| | | | | └ LogicalAndNode
| | | | | | └ LogicalCompareNode
| | | | | | | └ LogicalNegationNode
| | | | | | | | └ FullMathExpressionNode
| | | | | | | | | └ MultiplicationNode
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ ValueNode [0]
| └ WhileNode
| | └ Condition
| | | └ LogicalOrNode
| | | | └ LogicalAndNode
| | | | | └ LogicalCompareNode
| | | | | | └ LogicalNegationNode
| | | | | | | └ LogicalNot
| | | | | | | └ FullMathExpressionNode
| | | | | | | | └ MultiplicationNode
| | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | └ ValueNode [game.over]
| | └ BlockOfCode
| | | └ VariableAssignmentNode [game.over]
| | | | └ LogicalOrNode
| | | | | └ LogicalAndNode
| | | | | | └ LogicalCompareNode
| | | | | | | └ LogicalNegationNode
| | | | | | | | └ FullMathExpressionNode
| | | | | | | | | └ MultiplicationNode
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ FunctionCallNode [isGameOver]
| | | └ IfNode
| | | | └ Condition
| | | | | └ LogicalOrNode
| | | | | | └ LogicalAndNode
| | | | | | | └ LogicalCompareNode
| | | | | | | | └ LogicalNegationNode
| | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | └ ValueNode [game.over]
| | | | └ BlockOfCode
| | | | | └ BreakNode
| | | └ ForEachPlayerNode
| | | | └ Condition
| | | | | └ LogicalOrNode
| | | | | | └ LogicalAndNode
| | | | | | | └ LogicalCompareNode
| | | | | | | | └ LogicalNegationNode
| | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | └ ValueNode [1]
| | | | └ BlockOfCode
| | | | | └ PrintNode
| | | | | | └ LogicalOrNode
| | | | | | | └ LogicalAndNode
| | | | | | | | └ LogicalCompareNode
| | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | └ ValueNode [player.name]
| | | | | └ PrintNode
| | | | | | └ LogicalOrNode
| | | | | | | └ LogicalAndNode
| | | | | | | | └ LogicalCompareNode
| | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | └ ValueNode [player.tokens]
| | | | | └ ChoiceStatementNode
| | | | | | └ LogicalOrNode
| | | | | | | └ LogicalAndNode
| | | | | | | | └ LogicalCompareNode
| | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | └ ValueNode [1]
| | | | | | └ ChoiceNode
| | | | | | | └ Condition
| | | | | | | | └ LogicalOrNode
| | | | | | | | | └ LogicalAndNode
| | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | └ ValueNode [player.tokens]
| | | | | | | | | | | └ Token [>]
| | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | └ ValueNode [10]
| | | | | | | └ BlockOfCode
| | | | | | | | └ VariableAssignmentNode [chosen.tokens]
| | | | | | | | | └ LogicalOrNode
| | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | └ ValueNode [chosen.tokens]
| | | | | | | | | | | | | | └ Token [-]
| | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | └ ValueNode [3]
| | | | | | └ ChoiceNode
| | | | | | | └ Condition
| | | | | | | | └ LogicalOrNode
| | | | | | | | | └ LogicalAndNode
| | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | └ ValueNode [player.tokens]
| | | | | | | | | | | └ Token [>=]
| | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | └ ValueNode [5]
| | | | | | | └ BlockOfCode
| | | | | | | | └ VariableAssignmentNode [chosen.tokens]
| | | | | | | | | └ LogicalOrNode
| | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | └ ValueNode [chosen.tokens]
| | | | | | | | | | | | | | └ Token [-]
| | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | └ ValueNode [2]
| | | | | | | | └ VariableAssignmentNode [player.tokens]
| | | | | | | | | └ LogicalOrNode
| | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | └ ValueNode [player.tokens]
| | | | | | | | | | | | | | └ Token [+]
| | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | └ ValueNode [1]
| | | | | | └ ChoiceNode
| | | | | | | └ Condition
| | | | | | | | └ LogicalOrNode
| | | | | | | | | └ LogicalAndNode
| | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | └ ValueNode [player.tokens]
| | | | | | | | | | | └ Token [<]
| | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | └ ValueNode [5]
| | | | | | | └ BlockOfCode
| | | | | | | | └ VariableAssignmentNode [player.tokens]
| | | | | | | | | └ LogicalOrNode
| | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | └ ValueNode [player.tokens]
| | | | | | | | | | | | | | └ Token [+]
| | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | └ ValueNode [1]
| | | | | └ PrintNode
| | | | | | └ LogicalOrNode
| | | | | | | └ LogicalAndNode
| | | | | | | | └ LogicalCompareNode
| | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | └ TextNode [===]
| | | | | └ ForEachPlayerNode
| | | | | | └ Condition
| | | | | | | └ LogicalOrNode
| | | | | | | | └ LogicalAndNode
| | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | └ ValueNode [1]
| | | | | | └ BlockOfCode
| | | | | | | └ PrintNode
| | | | | | | | └ LogicalOrNode
| | | | | | | | | └ LogicalAndNode
| | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | └ ValueNode [player.name]
| | | | | | | └ PrintNode
| | | | | | | | └ LogicalOrNode
| | | | | | | | | └ LogicalAndNode
| | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | └ ValueNode [player.tokens]
| | | | | └ PrintNode
| | | | | | └ LogicalOrNode
| | | | | | | └ LogicalAndNode
| | | | | | | | └ LogicalCompareNode
| | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | └ TextNode [===================]
| └ WinHeaderNode
| | └ Condition
| | | └ LogicalOrNode
| | | | └ LogicalAndNode
| | | | | └ LogicalCompareNode
| | | | | | └ LogicalNegationNode
| | | | | | | └ FullMathExpressionNode
| | | | | | | | └ MultiplicationNode
| | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | └ ValueNode [player.tokens]
| | | | | | └ Token [>]
| | | | | | └ LogicalNegationNode
| | | | | | | └ FullMathExpressionNode
| | | | | | | | └ MultiplicationNode
| | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | └ ValueNode [10]"""

                for line_sol, line_test in zip(solution.rstrip('\r'), buf.getvalue().rstrip('\r')):
                    self.compare_output(line_sol, line_test)

    def test_prison(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            with FileManager("Testing/Final_Test_Cases/prison.txt") as file_manager:
                tokeniser = Tokeniser(file_manager)
                analysed_tokens = []
                analysed_tokens.append(Token("START_OF_FILE", "", 0))
                while (analysed_tokens[-1].type is not "END_OF_FILE"):
                    analysed_tokens.append(tokeniser.get_token())

                analysed_tokens = analysed_tokens[1:]

                parsed = ProgramNode(analysed_tokens[::-1], file_manager)
                self.print_tree(parsed, 0)

                solution = """└ ProgramNode
| └ PlayersHeaderNode
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [10]
| └ VariableInitNode [player.inPrison]
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [1]
| └ VariableInitNode [player.tries]
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [0]
| └ VariableInitNode [game.rollChance]
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [4]
| └ FunctionInitNode [prisonRoll]
| | └ BlockOfCode
| | | └ IfNode
| | | | └ Condition
| | | | | └ LogicalOrNode
| | | | | | └ LogicalAndNode
| | | | | | | └ LogicalCompareNode
| | | | | | | | └ LogicalNegationNode
| | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | └ RollNode
| | | | | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | | └ ValueNode [game.rollChance]
| | | | | | | | └ Token [==]
| | | | | | | | └ LogicalNegationNode
| | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | └ ValueNode [game.rollChance]
| | | | | | | | | | └ Token [-]
| | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | └ ValueNode [1]
| | | | └ BlockOfCode
| | | | | └ ReturnNode
| | | | | | └ LogicalOrNode
| | | | | | | └ LogicalAndNode
| | | | | | | | └ LogicalCompareNode
| | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | └ ValueNode [1]
| | | └ ReturnNode
| | | | └ LogicalOrNode
| | | | | └ LogicalAndNode
| | | | | | └ LogicalCompareNode
| | | | | | | └ LogicalNegationNode
| | | | | | | | └ FullMathExpressionNode
| | | | | | | | | └ MultiplicationNode
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ ValueNode [0]
| └ FunctionInitNode [someoneStillInPrison]
| | └ BlockOfCode
| | | └ ForEachPlayerNode
| | | | └ Condition
| | | | | └ LogicalOrNode
| | | | | | └ LogicalAndNode
| | | | | | | └ LogicalCompareNode
| | | | | | | | └ LogicalNegationNode
| | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | └ ValueNode [1]
| | | | └ BlockOfCode
| | | | | └ IfNode
| | | | | | └ Condition
| | | | | | | └ LogicalOrNode
| | | | | | | | └ LogicalAndNode
| | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | └ ValueNode [player.inPrison]
| | | | | | | | | | └ Token [==]
| | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | └ ValueNode [1]
| | | | | | └ BlockOfCode
| | | | | | | └ ReturnNode
| | | | | | | | └ LogicalOrNode
| | | | | | | | | └ LogicalAndNode
| | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | └ ValueNode [1]
| | | └ ReturnNode
| | | | └ LogicalOrNode
| | | | | └ LogicalAndNode
| | | | | | └ LogicalCompareNode
| | | | | | | └ LogicalNegationNode
| | | | | | | | └ FullMathExpressionNode
| | | | | | | | | └ MultiplicationNode
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ ValueNode [0]
| └ FunctionInitNode [getMinTries]
| | └ BlockOfCode
| | | └ VariableInitNode [min]
| | | | └ LogicalOrNode
| | | | | └ LogicalAndNode
| | | | | | └ LogicalCompareNode
| | | | | | | └ LogicalNegationNode
| | | | | | | | └ FullMathExpressionNode
| | | | | | | | | └ MultiplicationNode
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ ValueNode [99999]
| | | └ ForEachPlayerNode
| | | | └ Condition
| | | | | └ LogicalOrNode
| | | | | | └ LogicalAndNode
| | | | | | | └ LogicalCompareNode
| | | | | | | | └ LogicalNegationNode
| | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | └ ValueNode [1]
| | | | └ BlockOfCode
| | | | | └ IfNode
| | | | | | └ Condition
| | | | | | | └ LogicalOrNode
| | | | | | | | └ LogicalAndNode
| | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | └ ValueNode [player.tries]
| | | | | | | | | | └ Token [<]
| | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | └ ValueNode [min]
| | | | | | └ BlockOfCode
| | | | | | | └ VariableAssignmentNode [min]
| | | | | | | | └ LogicalOrNode
| | | | | | | | | └ LogicalAndNode
| | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | └ ValueNode [player.tries]
| | | └ ReturnNode
| | | | └ LogicalOrNode
| | | | | └ LogicalAndNode
| | | | | | └ LogicalCompareNode
| | | | | | | └ LogicalNegationNode
| | | | | | | | └ FullMathExpressionNode
| | | | | | | | | └ MultiplicationNode
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ ValueNode [min]
| └ WhileNode
| | └ Condition
| | | └ LogicalOrNode
| | | | └ LogicalAndNode
| | | | | └ LogicalCompareNode
| | | | | | └ LogicalNegationNode
| | | | | | | └ FullMathExpressionNode
| | | | | | | | └ MultiplicationNode
| | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | └ FunctionCallNode [someoneStillInPrison]
| | └ BlockOfCode
| | | └ ForEachPlayerNode
| | | | └ Condition
| | | | | └ LogicalOrNode
| | | | | | └ LogicalAndNode
| | | | | | | └ LogicalCompareNode
| | | | | | | | └ LogicalNegationNode
| | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | └ ValueNode [player.inPrison]
| | | | └ BlockOfCode
| | | | | └ VariableAssignmentNode [player.tries]
| | | | | | └ LogicalOrNode
| | | | | | | └ LogicalAndNode
| | | | | | | | └ LogicalCompareNode
| | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | └ ValueNode [player.tries]
| | | | | | | | | | | └ Token [+]
| | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | └ ValueNode [1]
| | | | | └ IfNode
| | | | | | └ Condition
| | | | | | | └ LogicalOrNode
| | | | | | | | └ LogicalAndNode
| | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | └ FunctionCallNode [prisonRoll]
| | | | | | └ BlockOfCode
| | | | | | | └ VariableAssignmentNode [player.inPrison]
| | | | | | | | └ LogicalOrNode
| | | | | | | | | └ LogicalAndNode
| | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | └ ValueNode [0]
| └ VariableInitNode [minTries]
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ FunctionCallNode [getMinTries]
| └ WinHeaderNode
| | └ Condition
| | | └ LogicalOrNode
| | | | └ LogicalAndNode
| | | | | └ LogicalCompareNode
| | | | | | └ LogicalNegationNode
| | | | | | | └ FullMathExpressionNode
| | | | | | | | └ MultiplicationNode
| | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | └ ValueNode [player.tries]
| | | | | | └ Token [==]
| | | | | | └ LogicalNegationNode
| | | | | | | └ FullMathExpressionNode
| | | | | | | | └ MultiplicationNode
| | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | └ ValueNode [minTries]"""

                for line_sol, line_test in zip(solution.rstrip('\r'), buf.getvalue().rstrip('\r')):
                    self.compare_output(line_sol, line_test)

    def test_foreachplayer_win(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            with FileManager("Testing/Final_Test_Cases/foreachplayer_win.txt") as file_manager:
                tokeniser = Tokeniser(file_manager)
                analysed_tokens = []
                analysed_tokens.append(Token("START_OF_FILE", "", 0))
                while (analysed_tokens[-1].type is not "END_OF_FILE"):
                    analysed_tokens.append(tokeniser.get_token())

                analysed_tokens = analysed_tokens[1:]

                parsed = ProgramNode(analysed_tokens[::-1], file_manager)
                self.print_tree(parsed, 0)

                solution = """└ ProgramNode
| └ PlayersHeaderNode
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [4]
| └ VariableInitNode [player.token]
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [4]
| └ FunctionInitNode [getScore]
| | └ Token [playerScore]
| | └ BlockOfCode
| | | └ ReturnNode
| | | | └ LogicalOrNode
| | | | | └ LogicalAndNode
| | | | | | └ LogicalCompareNode
| | | | | | | └ LogicalNegationNode
| | | | | | | | └ FullMathExpressionNode
| | | | | | | | | └ MultiplicationNode
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ ValueNode [playerScore]
| | | | | | | | | | └ Token [*]
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ ValueNode [2]
| └ FunctionInitNode [analysePlayer]
| | └ Token [playerScore]
| | └ BlockOfCode
| | | └ ReturnNode
| | | | └ LogicalOrNode
| | | | | └ LogicalAndNode
| | | | | | └ LogicalCompareNode
| | | | | | | └ LogicalNegationNode
| | | | | | | | └ FullMathExpressionNode
| | | | | | | | | └ MultiplicationNode
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ FunctionCallNode [getScore]
| | | | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | └ ValueNode [playerScore]
| └ VariableInitNode [iter]
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ ValueNode [1]
| └ ForEachPlayerNode
| | └ Condition
| | | └ LogicalOrNode
| | | | └ LogicalAndNode
| | | | | └ LogicalCompareNode
| | | | | | └ LogicalNegationNode
| | | | | | | └ FullMathExpressionNode
| | | | | | | | └ MultiplicationNode
| | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | └ ValueNode [1]
| | └ BlockOfCode
| | | └ PrintNode
| | | | └ LogicalOrNode
| | | | | └ LogicalAndNode
| | | | | | └ LogicalCompareNode
| | | | | | | └ LogicalNegationNode
| | | | | | | | └ FullMathExpressionNode
| | | | | | | | | └ MultiplicationNode
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ FunctionCallNode [analysePlayer]
| | | | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | └ ValueNode [player.token]
| | | | | | | | | | | | | | | | | └ Token [+]
| | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | └ ValueNode [iter]
| | | └ VariableAssignmentNode [player.token]
| | | | └ LogicalOrNode
| | | | | └ LogicalAndNode
| | | | | | └ LogicalCompareNode
| | | | | | | └ LogicalNegationNode
| | | | | | | | └ FullMathExpressionNode
| | | | | | | | | └ MultiplicationNode
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ FunctionCallNode [analysePlayer]
| | | | | | | | | | | | └ LogicalOrNode
| | | | | | | | | | | | | └ LogicalAndNode
| | | | | | | | | | | | | | └ LogicalCompareNode
| | | | | | | | | | | | | | | └ LogicalNegationNode
| | | | | | | | | | | | | | | | └ FullMathExpressionNode
| | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | └ ValueNode [player.token]
| | | | | | | | | | | | | | | | | └ Token [+]
| | | | | | | | | | | | | | | | | └ MultiplicationNode
| | | | | | | | | | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | | | | | | | | | └ ValueNode [iter]
| | | └ VariableAssignmentNode [iter]
| | | | └ LogicalOrNode
| | | | | └ LogicalAndNode
| | | | | | └ LogicalCompareNode
| | | | | | | └ LogicalNegationNode
| | | | | | | | └ FullMathExpressionNode
| | | | | | | | | └ MultiplicationNode
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ ValueNode [iter]
| | | | | | | | | └ Token [+]
| | | | | | | | | └ MultiplicationNode
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ ValueNode [1]
| └ PrintNode
| | └ LogicalOrNode
| | | └ LogicalAndNode
| | | | └ LogicalCompareNode
| | | | | └ LogicalNegationNode
| | | | | | └ FullMathExpressionNode
| | | | | | | └ MultiplicationNode
| | | | | | | | └ PartMathExpressionNode
| | | | | | | | | └ TextNode []
| └ ForEachPlayerNode
| | └ Condition
| | | └ LogicalOrNode
| | | | └ LogicalAndNode
| | | | | └ LogicalCompareNode
| | | | | | └ LogicalNegationNode
| | | | | | | └ FullMathExpressionNode
| | | | | | | | └ MultiplicationNode
| | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | └ ValueNode [player.token]
| | | | | | └ Token [<]
| | | | | | └ LogicalNegationNode
| | | | | | | └ FullMathExpressionNode
| | | | | | | | └ MultiplicationNode
| | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | └ ValueNode [13]
| | └ BlockOfCode
| | | └ VariableAssignmentNode [player.token]
| | | | └ LogicalOrNode
| | | | | └ LogicalAndNode
| | | | | | └ LogicalCompareNode
| | | | | | | └ LogicalNegationNode
| | | | | | | | └ FullMathExpressionNode
| | | | | | | | | └ MultiplicationNode
| | | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | | └ ValueNode [5]
| └ WinHeaderNode
| | └ Condition
| | | └ LogicalOrNode
| | | | └ LogicalAndNode
| | | | | └ LogicalCompareNode
| | | | | | └ LogicalNegationNode
| | | | | | | └ FullMathExpressionNode
| | | | | | | | └ MultiplicationNode
| | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | └ ValueNode [player.token]
| | | | | | └ Token [>]
| | | | | | └ LogicalNegationNode
| | | | | | | └ FullMathExpressionNode
| | | | | | | | └ MultiplicationNode
| | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | └ ValueNode [11]
| | | | | └ LogicalCompareNode
| | | | | | └ LogicalNegationNode
| | | | | | | └ FullMathExpressionNode
| | | | | | | | └ MultiplicationNode
| | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | └ ValueNode [player.token]
| | | | | | └ Token [<]
| | | | | | └ LogicalNegationNode
| | | | | | | └ FullMathExpressionNode
| | | | | | | | └ MultiplicationNode
| | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | └ ValueNode [13]
| | | | └ LogicalAndNode
| | | | | └ LogicalCompareNode
| | | | | | └ LogicalNegationNode
| | | | | | | └ FullMathExpressionNode
| | | | | | | | └ MultiplicationNode
| | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | └ ValueNode [player.token]
| | | | | | └ Token [==]
| | | | | | └ LogicalNegationNode
| | | | | | | └ FullMathExpressionNode
| | | | | | | | └ MultiplicationNode
| | | | | | | | | └ PartMathExpressionNode
| | | | | | | | | | └ ValueNode [16]"""

                for line_sol, line_test in zip(solution.rstrip('\r'), buf.getvalue().rstrip('\r')):
                    self.compare_output(line_sol, line_test)