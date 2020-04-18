import argparse
from Lekser.file_manager import FileManager
from Lekser.tokeniser import Tokeniser
from Lekser.token import Token

def run(path):
    file_manager = FileManager(path)
    with file_manager as fm:
        tokeniser = Tokeniser(fm)
        analysed_tokens = []
        analysed_tokens.append(Token("START_OF_FILE", ""))
        while (analysed_tokens[-1].type is not "END_OF_FILE"):
            analysed_tokens.append(tokeniser.get_token())

    print_tokens(analysed_tokens)

def print_tokens(analysed_tokens):
    format_string = "{:<30} | {:<20}"
    for token in analysed_tokens:
        print(format_string.format(token.value, token.type))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='game language interpreter')
    parser.add_argument('path', help='path to textfile')
    args = parser.parse_args()

    run(args.path)