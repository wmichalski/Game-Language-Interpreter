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
                parsed.execute()

                solution = """1
1
2
3
5
8
13
21
34
55
89"""

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
                parsed.execute()

                solution = """5"""

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
                parsed.execute()

                solution = """1
10
100
1
10
100
1
10
100"""

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
                parsed.execute()

                solution = """1.25
20.0"""

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
                parsed.execute()

                solution = """14
1
6
6
1000
1
1"""

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
                parsed.execute()

                solution = """8
9
365
64"""

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
                parsed.execute()

                solution = """6
6
8
8
-2
0
19397"""

                for line_sol, line_test in zip(solution.rstrip('\r'), buf.getvalue().rstrip('\r')):
                    self.compare_output(line_sol, line_test)