# jesli nawias a poprzedni token to if: if 
import Lexer.token
from .node import *

class Parser():
    def __init__(self, tokens):
        self.tokens = tokens[::-1]
        self.create_subtree()

    def peekToken(self):
        return self.tokens[-1]

    def popToken(self):
        return self.tokens.pop()

    def create_subtree(self):
        if self.peekToken() == "IF":
            return IfNode(self.tokens)

