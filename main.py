import argparse
from Lexer.file_manager import FileManager
from Lexer.tokeniser import Tokeniser
from Lexer.token import Token
from Parser.node import *


def run(path):
    file_manager = FileManager(path)
    with file_manager as fm:
        tokeniser = Tokeniser(fm)
        analysed_tokens = []
        analysed_tokens.append(Token("START_OF_FILE", "", 0))
        while (analysed_tokens[-1].type is not "END_OF_FILE"):
            analysed_tokens.append(tokeniser.get_token())

        analysed_tokens = analysed_tokens[1:]
        print_tokens(analysed_tokens)

        parsed = ProgramNode(analysed_tokens[::-1], file_manager)
        print_tree(parsed, 0)

        print("==========")
        parsed.execute()

def print_tokens(analysed_tokens):
    format_string = "({:<30} {:<20}),"
    for token in analysed_tokens:
        print(format_string.format("\"" + token.type +
              "\",", "\"" + token.value + "\""))


def print_tree(node, depth):
    if node.__class__ == Token:
        print("| " * (depth) + "└ " + node.__class__.__name__ + " [" + node.value + "]")
    else:
        print("| " * (depth) + "└ " + node.__class__.__name__, end="")
        print_node_name(node)
        print_node_value(node)
        print("")

    try:
        for child in node.children:
            print_tree(child, depth+1)
    except:
        pass

def print_node_name(node):
    try:
        name = node.get_name()
        print(" [" + name + "]", end="")
    except:
        pass

def print_node_value(node):
    try:
        value = node.get_value()
        print(" [" + str(value) + "]", end="")
    except:
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='game language interpreter')
    parser.add_argument('path', help='path to textfile')
    args = parser.parse_args()

    run(args.path)
