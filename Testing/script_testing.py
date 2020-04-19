import unittest
import os
import io 

from unittest.mock import patch, mock_open

from Lexer.file_manager import FileManager
from Lexer.tokeniser import Tokeniser
from Lexer import error_manager
from Lexer.token import Token

class AcceptanceScriptTester(unittest.TestCase):
    def loop_test(self, fm):
        tokeniser = Tokeniser(fm)
        analysed_tokens = []
        analysed_tokens.append(Token("START_OF_FILE", ""))
        while (analysed_tokens[-1].type is not "END_OF_FILE"):
            analysed_tokens.append(tokeniser.get_token())

        return analysed_tokens[1:]

    def compare_tokens(self, expected, result):
        for (ex_type, ex_value), result in zip(expected, result):
            self.assertEqual(ex_type, result.type)
            self.assertEqual(ex_value, result.value)

    def test1(self):
        with FileManager("Testing/test1.txt") as file_manager:
            tokens = self.loop_test(file_manager)

            expected = [
                ("FOR_EACH_PLAYER",             "forEachPlayer"     ),
                ("LEFT_ROUND",                  "("                 ),
                ("LOGICAL_NOT",                 "!"                 ),
                ("IDENTIFIER",                  "player.inPrison"   ),
                ("RIGHT_ROUND",                 ")"                 ),
                ("LEFT_CURLY",                  "{"                 ),
                ("IDENTIFIER",                  "player.score"      ),
                ("ASSIGNMENT",                  "="                 ),
                ("IDENTIFIER",                  "player.score"      ),
                ("PLUS",                        "+"                 ),
                ("ROLL",                        "roll"              ),
                ("LEFT_ROUND",                  "("                 ),
                ("NATURAL_NUMBER",              "6"                 ),
                ("RIGHT_ROUND",                 ")"                 ),
                ("RIGHT_CURLY",                 "}"                 ),
                ("FOR_EACH_PLAYER",             "forEachPlayer"     ),
                ("LEFT_ROUND",                  "("                 ),
                ("IDENTIFIER",                  "player.inPrison"   ),
                ("RIGHT_ROUND",                 ")"                 ),
                ("LEFT_CURLY",                  "{"                 ),
                ("IF",                          "if"                ),
                ("LEFT_ROUND",                  "("                 ),
                ("ROLL",                        "roll"              ),
                ("LEFT_ROUND",                  "("                 ),
                ("NATURAL_NUMBER",              "4"                 ),
                ("RIGHT_ROUND",                 ")"                 ),
                ("EQUAL_TO",                    "=="                ),
                ("NATURAL_NUMBER",              "4"                 ),
                ("RIGHT_ROUND",                 ")"                 ),
                ("LEFT_CURLY",                  "{"                 ),
                ("IDENTIFIER",                  "player.inPrison"   ),
                ("ASSIGNMENT",                  "="                 ),
                ("REAL_NUMBER",                 "0"                 ),
                ("SEMICOLON",                   ";"                 ),
                ("RIGHT_CURLY",                 "}"                 ),
                ("RIGHT_CURLY",                 "}"                 ),
                ("END_OF_FILE",                 ""                  )]

            self.compare_tokens(expected, tokens)

    def test2(self):
        with FileManager("Testing/test2.txt") as file_manager:
            tokens = self.loop_test(file_manager)

            expected = [
                ("PLAYERS",                     "PLAYERS"           ),
                ("NATURAL_NUMBER",              "2"                 ),
                ("GAME",                        "GAME"              ),
                ("COLON",                       ":"                 ),
                ("IDENTIFIER",                  "tokens"            ),
                ("ASSIGNMENT",                  "="                 ),
                ("NATURAL_NUMBER",              "10"                ),
                ("SEMICOLON",                   ";"                 ),
                ("IDENTIFIER",                  "finished"          ),
                ("ASSIGNMENT",                  "="                 ),
                ("REAL_NUMBER",                 "0"                 ),
                ("SEMICOLON",                   ";"                 ),
                ("INDIVIDUAL",                  "INDIVIDUAL"        ),
                ("COLON",                       ":"                 ),
                ("IDENTIFIER",                  "score"             ),
                ("ASSIGNMENT",                  "="                 ),
                ("REAL_NUMBER",                 "0"                 ),
                ("SEMICOLON",                   ";"                 ),
                ("FUNCTIONS",                   "FUNCTIONS"         ),
                ("COLON",                       ":"                 ),
                ("FUNCTION_DEF",                "def"               ),
                ("IDENTIFIER",                  "getScore"          ),
                ("LEFT_ROUND",                  "("                 ),
                ("IDENTIFIER",                  "playerscore"       ),
                ("COMMA",                       ","                 ),
                ("IDENTIFIER",                  "gametokens"        ),
                ("RIGHT_ROUND",                 ")"                 ),
                ("LEFT_CURLY",                  "{"                 ),
                ("VARIABLE_ASSIGN",             "var"               ),
                ("IDENTIFIER",                  "retScore"          ),
                ("SEMICOLON",                   ";"                 ),
                ("IDENTIFIER",                  "retScore"          ),
                ("ASSIGNMENT",                  "="                 ),
                ("NATURAL_NUMBER",              "2"                 ),
                ("MULTIPLICATION",              "*"                 ),
                ("IDENTIFIER",                  "playerscore"       ),
                ("MINUS",                       "-"                 ),
                ("IDENTIFIER",                  "gametokens"        ),
                ("SEMICOLON",                   ";"                 ),
                ("RETURN",                      "return"            ),
                ("IDENTIFIER",                  "retScore"          ),
                ("SEMICOLON",                   ";"                 ),
                ("RIGHT_CURLY",                 "}"                 ),
                ("RUN",                         "RUN"               ),
                ("COLON",                       ":"                 ),
                ("FOR_EACH_PLAYER",             "forEachPlayer"     ),
                ("LEFT_ROUND",                  "("                 ),
                ("NATURAL_NUMBER",              "1"                 ),
                ("RIGHT_ROUND",                 ")"                 ),
                ("LEFT_CURLY",                  "{"                 ),
                ("IDENTIFIER",                  "player.won"        ),
                ("ASSIGNMENT",                  "="                 ),
                ("NATURAL_NUMBER",              "1"                 ),
                ("SEMICOLON",                   ";"                 ),
                ("BREAK",                       "break"             ),
                ("SEMICOLON",                   ";"                 ),
                ("RIGHT_CURLY",                 "}"                 ),
                ("WIN",                         "WIN"               ),
                ("COLON",                       ":"                 ),
                ("LEFT_SQUARE",                 "["                 ),
                ("IDENTIFIER",                  "won"               ),
                ("EQUAL_TO",                    "=="                ),
                ("NATURAL_NUMBER",              "1"                 ),
                ("RIGHT_SQUARE",                "]"                 ),
                ("END_OF_FILE",                 ""                  )]
            
            self.compare_tokens(expected, tokens)

    def test3(self):
        with FileManager("Testing/test3.txt") as file_manager:
            tokens = self.loop_test(file_manager)

            expected = [
                ("WHILE",                       "while"             ),
                ("LEFT_ROUND",                  "("                 ),
                ("LOGICAL_NOT",                 "!"                 ),
                ("IDENTIFIER",                  "finished"          ),
                ("RIGHT_ROUND",                 ")"                 ),
                ("LEFT_CURLY",                  "{"                 ),
                ("FOR_EACH_PLAYER",             "forEachPlayer"     ),
                ("LEFT_ROUND",                  "("                 ),
                ("NATURAL_NUMBER",              "1"                 ),
                ("RIGHT_ROUND",                 ")"                 ),
                ("LEFT_CURLY",                  "{"                 ),
                ("CHOICE",                      "choice"            ),
                ("LEFT_ROUND",                  "("                 ),
                ("NATURAL_NUMBER",              "20"                ),
                ("RIGHT_ROUND",                 ")"                 ),
                ("LEFT_CURLY",                  "{"                 ),
                ("LEFT_SQUARE",                 "["                 ),
                ("ROLL",                        "roll"              ),
                ("GREATER_OR_EQUAL",            ">="                ),
                ("NATURAL_NUMBER",              "20"                ),
                ("LOGICAL_AND",                 "and"               ),
                ("LEFT_ROUND",                  "("                 ),
                ("IDENTIFIER",                  "chosen.score"      ),
                ("GREATER_OR_EQUAL",            ">="                ),
                ("NATURAL_NUMBER",              "3"                 ),
                ("RIGHT_ROUND",                 ")"                 ),
                ("RIGHT_SQUARE",                "]"                 ),
                ("LEFT_CURLY",                  "{"                 ),
                ("IDENTIFIER",                  "player.score"      ),
                ("ASSIGNMENT",                  "="                 ),
                ("IDENTIFIER",                  "player.score"      ),
                ("PLUS",                        "+"                 ),
                ("ROLL",                        "roll"              ),
                ("LEFT_ROUND",                  "("                 ),
                ("NATURAL_NUMBER",              "5"                 ),
                ("RIGHT_ROUND",                 ")"                 ),
                ("SEMICOLON",                   ";"                 ),
                ("IDENTIFIER",                  "chosen.score"      ),
                ("ASSIGNMENT",                  "="                 ),
                ("IDENTIFIER",                  "chosen.score"      ),
                ("MINUS",                       "-"                 ),
                ("NATURAL_NUMBER",              "3"                 ),
                ("SEMICOLON",                   ";"                 ),
                ("RIGHT_CURLY",                 "}"                 ),
                ("LEFT_SQUARE",                 "["                 ),
                ("ROLL",                        "roll"              ),
                ("GREATER_OR_EQUAL",            ">="                ),
                ("NATURAL_NUMBER",              "18"                ),
                ("LOGICAL_AND",                 "and"               ),
                ("LEFT_ROUND",                  "("                 ),
                ("IDENTIFIER",                  "tokens"            ),
                ("GREATER_OR_EQUAL",            ">="                ),
                ("NATURAL_NUMBER",              "1"                 ),
                ("RIGHT_ROUND",                 ")"                 ),
                ("RIGHT_SQUARE",                "]"                 ),
                ("LEFT_CURLY",                  "{"                 ),
                ("IDENTIFIER",                  "player.score"      ),
                ("ASSIGNMENT",                  "="                 ),
                ("IDENTIFIER",                  "player.score"      ),
                ("PLUS",                        "+"                 ),
                ("NATURAL_NUMBER",              "2"                 ),
                ("SEMICOLON",                   ";"                 ),
                ("IDENTIFIER",                  "tokens"            ),
                ("ASSIGNMENT",                  "="                 ),
                ("IDENTIFIER",                  "tokens"            ),
                ("MINUS",                       "-"                 ),
                ("NATURAL_NUMBER",              "1"                 ),
                ("SEMICOLON",                   ";"                 ),
                ("RIGHT_CURLY",                 "}"                 ),
                ("LEFT_SQUARE",                 "["                 ),
                ("ROLL",                        "roll"              ),
                ("GREATER_OR_EQUAL",            ">="                ),
                ("NATURAL_NUMBER",              "15"                ),
                ("RIGHT_SQUARE",                "]"                 ),
                ("LEFT_CURLY",                  "{"                 ),
                ("IDENTIFIER",                  "player.score"      ),
                ("PLUS",                        "+"                 ),
                ("ASSIGNMENT",                  "="                 ),
                ("NATURAL_NUMBER",              "1"                 ),
                ("SEMICOLON",                   ";"                 ),
                ("RIGHT_CURLY",                 "}"                 ),
                ("RIGHT_CURLY",                 "}"                 ),
                ("IF",                          "if"                ),
                ("LEFT_ROUND",                  "("                 ),
                ("IDENTIFIER",                  "player.score"      ),
                ("GREATER",                     ">"                 ),
                ("NATURAL_NUMBER",              "20"                ),
                ("RIGHT_ROUND",                 ")"                 ),
                ("LEFT_CURLY",                  "{"                 ),
                ("IDENTIFIER",                  "finished"          ),
                ("ASSIGNMENT",                  "="                 ),
                ("NATURAL_NUMBER",              "1"                 ),
                ("SEMICOLON",                   ";"                 ),
                ("IDENTIFIER",                  "player.won"        ),
                ("ASSIGNMENT",                  "="                 ),
                ("NATURAL_NUMBER",              "1"                 ),
                ("SEMICOLON",                   ";"                 ),
                ("BREAK",                       "break"             ),
                ("SEMICOLON",                   ";"                 ),
                ("RIGHT_CURLY",                 "}"                 ),
                ("RIGHT_CURLY",                 "}"                 ),
                ("RIGHT_CURLY",                 "}"                 ),
                ("END_OF_FILE",                 ""                  )]
            
            self.compare_tokens(expected, tokens)