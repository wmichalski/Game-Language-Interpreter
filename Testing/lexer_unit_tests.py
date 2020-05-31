import unittest
import os
import io 

from unittest.mock import patch, mock_open

# https://stackoverflow.com/questions/18867747/how-to-use-mock-open-with-patch-object-in-test-annotation

from Lexer.file_manager import FileManager
from Lexer.tokeniser import Tokeniser
from Lexer import error_manager
from Lexer.token import Token

def loop_test(fm):
    tokeniser = Tokeniser(fm)
    analysed_tokens = []
    analysed_tokens.append(Token("START_OF_FILE", "", 0))
    while (analysed_tokens[-1].type is not "END_OF_FILE"):
        analysed_tokens.append(tokeniser.get_token())

    return analysed_tokens[1:]

class BaseTokeniserTester(unittest.TestCase):
    def assert_equal_tokens(self, expected):
        with FileManager("") as fm:
            for _type, _value in expected:
                token = Tokeniser(fm).get_token()
                self.assertEqual(_type, token.type)
                self.assertEqual(_value, token.value)

# noinspection PyUnusedLocal
class KeywordTokensTester(BaseTokeniserTester):
    @patch("builtins.open", return_value=io.StringIO("or"))
    def test_or_keyword(self, mock_open):
        self.assert_equal_tokens([("LOGICAL_OR", "or")])

    @patch("builtins.open", return_value=io.StringIO('and'))
    def test_and_keyword(self, mock_open):
        self.assert_equal_tokens([("LOGICAL_AND", 'and')])

    @patch("builtins.open", return_value=io.StringIO('return'))
    def test_return_keyword(self, mock_open):
        self.assert_equal_tokens([("RETURN", 'return')])

    @patch("builtins.open", return_value=io.StringIO('def'))
    def test_def_keyword(self, mock_open):
        self.assert_equal_tokens([("FUNCTION_DEF", 'def')])

    @patch("builtins.open", return_value=io.StringIO('var'))
    def test_var_keyword(self, mock_open):
        self.assert_equal_tokens([("VARIABLE_ASSIGN", 'var')])

    @patch("builtins.open", return_value=io.StringIO('while'))
    def test_while_keyword(self, mock_open):
        self.assert_equal_tokens([("WHILE", 'while')])

    @patch("builtins.open", return_value=io.StringIO('if'))
    def test_if_keyword(self, mock_open):
        self.assert_equal_tokens([("IF", 'if')])

    @patch("builtins.open", return_value=io.StringIO('choice'))
    def test_choice_keyword(self, mock_open):
        self.assert_equal_tokens([("CHOICE", 'choice')])

    @patch("builtins.open", return_value=io.StringIO('forEachPlayer'))
    def test_forEachPlayer_keyword(self, mock_open):
        self.assert_equal_tokens([("FOR_EACH_PLAYER", 'forEachPlayer')])

    @patch("builtins.open", return_value=io.StringIO('roll'))
    def test_roll_keyword(self, mock_open):
        self.assert_equal_tokens([("ROLL", 'roll')])

    @patch("builtins.open", return_value=io.StringIO('else'))
    def test_else_keyword(self, mock_open):
        self.assert_equal_tokens([("ELSE", 'else')])

    @patch("builtins.open", return_value=io.StringIO('PLAYERS'))
    def test_players_keyword(self, mock_open):
        self.assert_equal_tokens([("PLAYERS", 'PLAYERS')])

    @patch("builtins.open", return_value=io.StringIO('GAME'))
    def test_game_keyword(self, mock_open):
        self.assert_equal_tokens([("GAME", 'GAME')])

    @patch("builtins.open", return_value=io.StringIO('INDIVIDUAL'))
    def test_individual_keyword(self, mock_open):
        self.assert_equal_tokens([("INDIVIDUAL", 'INDIVIDUAL')])

    @patch("builtins.open", return_value=io.StringIO('FUNCTIONS'))
    def test_functions_keyword(self, mock_open):
        self.assert_equal_tokens([("FUNCTIONS", 'FUNCTIONS')])

    @patch("builtins.open", return_value=io.StringIO('RUN'))
    def test_run_keyword(self, mock_open):
        self.assert_equal_tokens([("RUN", 'RUN')])

    @patch("builtins.open", return_value=io.StringIO('WIN'))
    def test_win_keyword(self, mock_open):
        self.assert_equal_tokens([("WIN", 'WIN')])

class SpecialSignsTokensTester(BaseTokeniserTester):
    @patch("builtins.open", return_value=io.StringIO('()'))
    def test_two_round_brackets(self, mock_open):
        self.assert_equal_tokens([("LEFT_ROUND", "("), ("RIGHT_ROUND", ")")])
    
    @patch("builtins.open", return_value=io.StringIO(r'{}'))
    def test_two_curly_brackets(self, mock_open):
        self.assert_equal_tokens([("LEFT_CURLY", "{"), ("RIGHT_CURLY", "}")])

    @patch("builtins.open", return_value=io.StringIO('+'))
    def test_plus(self, mock_open):
        self.assert_equal_tokens([("PLUS", "+")])

    @patch("builtins.open", return_value=io.StringIO('-'))
    def test_minus(self, mock_open):
        self.assert_equal_tokens([("MINUS", "-")])

    @patch("builtins.open", return_value=io.StringIO('*'))
    def test_multiplication(self, mock_open):
        self.assert_equal_tokens([("MULTIPLICATION", "*")])

    @patch("builtins.open", return_value=io.StringIO('/'))
    def test_division(self, mock_open):
        self.assert_equal_tokens([("DIVISION", "/")])

    @patch("builtins.open", return_value=io.StringIO('='))
    def test_assignment_operator(self, mock_open):
        self.assert_equal_tokens([("ASSIGNMENT", "=")])

    @patch("builtins.open", return_value=io.StringIO('<>'))
    def test_lower_greater(self, mock_open):
        self.assert_equal_tokens([("LOWER", "<"), ("GREATER", ">")])

    @patch("builtins.open", return_value=io.StringIO('[]'))
    def test_square_brackets(self, mock_open):
        self.assert_equal_tokens([("LEFT_SQUARE", "["), ("RIGHT_SQUARE", "]")])

    @patch("builtins.open", return_value=io.StringIO(':'))
    def test_colon(self, mock_open):
        self.assert_equal_tokens([("COLON", ":")])

    @patch("builtins.open", return_value=io.StringIO('!'))
    def test_exclamation(self, mock_open):
        self.assert_equal_tokens([("LOGICAL_NOT", "!")])

    @patch("builtins.open", return_value=io.StringIO(';'))
    def test_semicolon(self, mock_open):
        self.assert_equal_tokens([("SEMICOLON", ";")])

class ComparisonTokensTester(BaseTokeniserTester):
    @patch("builtins.open", return_value=io.StringIO('=='))
    def test_equal_to(self, mock_open):
        self.assert_equal_tokens([("EQUAL_TO", "==")])
    
    @patch("builtins.open", return_value=io.StringIO('!='))
    def test_not_equal_to(self, mock_open):
        self.assert_equal_tokens([("NOT_EQUAL_TO", "!=")])

    @patch("builtins.open", return_value=io.StringIO('<='))
    def test_lower_equal(self, mock_open):
        self.assert_equal_tokens([("LOWER_OR_EQUAL", '<=')])

    @patch("builtins.open", return_value=io.StringIO('>='))
    def test_greater_equal(self, mock_open):
        self.assert_equal_tokens([("GREATER_OR_EQUAL", '>=')])

class SimpleCodeTester(BaseTokeniserTester):
    @patch("builtins.open", return_value=io.StringIO('var a = 0.2;'))
    def test_equal_to(self, mock_open):
        self.assert_equal_tokens([
            ("VARIABLE_ASSIGN", "var"),
            ("IDENTIFIER", "a"),
            ("ASSIGNMENT", "="),
            ("REAL_NUMBER", "0.2"),
            ("SEMICOLON", ";"),
            ])

    @patch("builtins.open", return_value=io.StringIO('while(!cond)'))
    def test_while(self, mock_open):
        self.assert_equal_tokens([
            ("WHILE", "while"),
            ("LEFT_ROUND", "("),
            ("LOGICAL_NOT", "!"),
            ("IDENTIFIER", "cond"),
            ("RIGHT_ROUND", ")"),
            ])

    @patch("builtins.open", return_value=io.StringIO(r'ifif{                         }'))
    def test_two_keywords_typo(self, mock_open):
        self.assert_equal_tokens([
            ("IDENTIFIER", "ifif"),
            ("LEFT_CURLY", "{"),
            ("RIGHT_CURLY", "}"),
            ])

class ErrorCasesTester(BaseTokeniserTester):
    @patch("Lexer.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO('050'))
    def test_number_starting_with_0(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(error_manager.ErrorManager, Tokeniser(fm).get_token)
            self.assertTrue(mock_error.called)

    @patch("builtins.open", return_value=io.StringIO('50'))
    def test_legit_natnumber(self, mock_open):
        self.assert_equal_tokens([("NATURAL_NUMBER", "50")])

    @patch("builtins.open", return_value=io.StringIO('210.037'))
    def test_legit_realnumber(self, mock_open):
        self.assert_equal_tokens([("REAL_NUMBER", "210.037")])

    @patch("builtins.open", return_value=io.StringIO('0'))
    def test_zero(self, mock_open):
        self.assert_equal_tokens([("REAL_NUMBER", "0")])

    # lambda: https://stackoverflow.com/questions/16045249/python-assertraises-error-in-unit-test-exception-not-being-caught
    @patch("Lexer.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO('0.5.0'))
    def test_number_with_2_separators(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(error_manager.ErrorManager, lambda: loop_test(fm)) 
            self.assertTrue(mock_error.called)

    @patch("Lexer.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO('123.'))
    def test_number_with_comma_but_no_decimal(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(error_manager.ErrorManager, lambda: loop_test(fm)) 
            self.assertTrue(mock_error.called)

    @patch("Lexer.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO('&'))
    def test_unknown_char(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(error_manager.ErrorManager, Tokeniser(fm).get_token)   
            self.assertTrue(mock_error.called)


    @patch("Lexer.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO('o'*(Tokeniser.MAX_TOKEN_LENGTH+1)))
    def test_string_too_long(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(error_manager.ErrorManager, Tokeniser(fm).get_token)  
            self.assertTrue(mock_error.called)

    @patch("builtins.open", return_value=io.StringIO('o'*(Tokeniser.MAX_TOKEN_LENGTH)))
    def test_string_max_length(self, mock_open):
        self.assert_equal_tokens([("IDENTIFIER", 'o'*(Tokeniser.MAX_TOKEN_LENGTH))])

    @patch("Lexer.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO('1'*(Tokeniser.MAX_TOKEN_LENGTH+1)))
    def test_natnumber_too_long(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(error_manager.ErrorManager, Tokeniser(fm).get_token)  
            self.assertTrue(mock_error.called)

    @patch("builtins.open", return_value=io.StringIO('1'*(Tokeniser.MAX_TOKEN_LENGTH)))
    def test_natnumber_max_length(self, mock_open):
        self.assert_equal_tokens([("NATURAL_NUMBER", '1'*(Tokeniser.MAX_TOKEN_LENGTH))])

    @patch("Lexer.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO('1.'+'1'*(Tokeniser.MAX_TOKEN_LENGTH-1)))
    def test_realnumber_too_long(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(error_manager.ErrorManager, Tokeniser(fm).get_token)  
            self.assertTrue(mock_error.called)

    @patch("builtins.open", return_value=io.StringIO('1.'+'1'*(Tokeniser.MAX_TOKEN_LENGTH-2)))
    def test_realnumber_max_length(self, mock_open):
        self.assert_equal_tokens([("REAL_NUMBER", '1.'+'1'*(Tokeniser.MAX_TOKEN_LENGTH-2))])

    @patch("builtins.open", return_value=io.StringIO(""))
    def test_if_only_eof_in_empty_input(self, mock_open):
        self.assert_equal_tokens([("END_OF_FILE", "")])

    @patch("builtins.open", return_value=io.StringIO("                  "))
    def test_if_only_eof_in_spaced_input(self, mock_open):
        self.assert_equal_tokens([("END_OF_FILE", "")])
