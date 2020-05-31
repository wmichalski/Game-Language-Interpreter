import unittest
import os
import io

from unittest.mock import patch, mock_open

from Lexer.file_manager import FileManager
from Lexer.tokeniser import Tokeniser
from Lexer import error_manager
from Lexer.token import Token
from Parser.parser import ProgramNode
import Parser


def run_program(fm):
    tokeniser = Tokeniser(fm)
    analysed_tokens = []
    analysed_tokens.append(Token("START_OF_FILE", "", 0))
    while (analysed_tokens[-1].type is not "END_OF_FILE"):
        analysed_tokens.append(tokeniser.get_token())

    analysed_tokens = analysed_tokens[1:]
    parsed = ProgramNode(analysed_tokens[::-1], fm)

    parsed.execute()

class ErrorCasesTester(unittest.TestCase):
    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("PLAYERS 2 PLAYERS 3"))
    def test_too_many_playerheaders(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("var a = \"text\"+3"))
    def test_math_with_string(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("var a = 3*\"text\""))
    def test_math_with_string2(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("var a = 4; print)a);"))
    def test_print_wrong_char(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("var rolled = 5;"))
    def test_rolled_inited(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("PLAYERS 2 var player.a; forEachPlayer(1){player.a=4;}"))
    def test_assign_player_variable_not_defined(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("game.a=5;"))
    def test_assign_game_var_not_defined(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("a=5;"))
    def test_assign_variable_not_defined(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("chosen.a=5;"))
    def test_assign_chosen_variable_not_defined(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("def 111(){a}"))
    def test_functionname_not_identifier(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("def if(){a}"))
    def test_functionname_keyword(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("def func() var a = 5;"))
    def test_function_no_body(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("forEachPlayer{};"))
    def test_foreach_only_body(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("else{};"))
    def test_else_without_if(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("if(1)else{}"))
    def test_if_without_body(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("if(\"aaa\")"))
    def test_cond_string(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("var a = \"aaa\"; if(a)"))
    def test_cond_string2(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("choice()"))
    def test_choice_no_roll(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("choice(1){[1]{var rolled = 5;}}"))
    def test_choice_overwritten_rolled(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("if(\"aaa\" or 1)"))
    def test_cond_string_or(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("if(\"aaa\" and 1)"))
    def test_cond_string_and(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("if(!\"aaa\")"))
    def test_cond_string_not(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("if(\"aaa\" > \"aa\")"))
    def test_cond_string_compare(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("print(\"aaa\" * 1)"))
    def test_string_multi_1(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("print(-)"))
    def test_minus_without_number(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("print(-\"aaa\")"))
    def test_minus_string(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("print(a);"))
    def test_access_nonexisting_var(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("var a;print(a);"))
    def test_access_existing_without_value(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("var a = 2+(2*2;"))
    def test_nonclosed_bracketed(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("WIN; []"))
    def test_wrong_win_syntax(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))

    @patch("Parser.error_manager.manage_error")
    @patch("builtins.open", return_value=io.StringIO("var a=\"a\";roll(a);"))
    def test_roll_string(self, mock_error, mock_open):
        with FileManager("") as fm:
            self.assertRaises(Parser.error_manager.ErrorManager, lambda: run_program(fm))
