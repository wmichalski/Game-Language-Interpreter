from Lexer.file_manager import FileManager
from Lexer.token import Token, keyword_types, accepted_special_signs, comparison_operators
from Lexer import error_manager

class Tokeniser:
    MAX_TOKEN_LENGTH = 100

    def __init__(self, file_manager):
        self.fm = file_manager

    def get_token(self):
        first_char = self.fm.peek_chars(1)

        if first_char.isspace():
            self.ignore_spaces()
            first_char = self.fm.peek_chars(1)

        if first_char == "":
            return self.end_of_file()

        if first_char.isalpha():
            return self.get_string_token()

        if first_char.isdigit():
            return self.get_number_token()

        if first_char in accepted_special_signs.keys():
            return self.get_special_sign()

        return self.unexpected_sign()


    def get_string_token(self):
        chars = ""
        counter = 0
        while (self.fm.peek_chars(1).isalpha() or self.fm.peek_chars(1).isdigit()):
            counter += 1
            if counter > self.MAX_TOKEN_LENGTH:
                self.raise_error("The token is too long", chars)
            chars += self.fm.get_chars(1)

        if (self.fm.peek_chars(1) == "."):
            if ((chars != "player") and (chars != "chosen")and (chars != "game")):
                self.raise_error("Found dot, but the keyword before it doesnt match neither 'player' nor 'chosen' nor 'game'", chars)

            counter += 1
            if counter > self.MAX_TOKEN_LENGTH:
                self.raise_error("The token is too long", chars)
            chars += self.fm.get_chars(1)
            
            if not (self.fm.peek_chars(1).isalpha()):
                self.raise_error("Found dot, but no variable name afterwards", chars)

            while (self.fm.peek_chars(1).isalpha() or self.fm.peek_chars(1).isdigit()):
                counter += 1
                if counter > self.MAX_TOKEN_LENGTH:
                    self.raise_error("The token is too long", chars)
                chars += self.fm.get_chars(1)

        if chars in keyword_types.keys():
            return Token(keyword_types[chars], chars)
        else:
            return Token("IDENTIFIER", chars)

    def get_number_token(self):
        chars = ""
        counter = 0

        if self.fm.peek_chars(1) == "0":
            counter += 1
            chars += self.fm.get_chars(1)

            if self.fm.peek_chars(1) == ".":
                counter += 1
                chars += self.fm.get_chars(1)
                while (self.fm.peek_chars(1).isdigit()):
                    counter += 1
                    if counter > self.MAX_TOKEN_LENGTH:
                        self.raise_error("The token is too long", chars)
                    chars += self.fm.get_chars(1)

                return Token("REAL_NUMBER", chars)
            
            if self.fm.peek_chars(1).isdigit():
                self.raise_error("ERROR - NONZERO NUMBER STARTS WITH A 0", chars)

            return Token("REAL_NUMBER", chars) # not sure how to treat a zero

        while (self.fm.peek_chars(1).isdigit()):
            counter += 1
            if counter > self.MAX_TOKEN_LENGTH:
                self.raise_error("The token is too long", chars)
            chars += self.fm.get_chars(1)

        if self.fm.peek_chars(1) == "." and self.fm.peek_chars(2)[-1].isdigit():
            counter += 1
            chars += self.fm.get_chars(1)
            while (self.fm.peek_chars(1).isdigit()):
                counter += 1
                if counter > self.MAX_TOKEN_LENGTH:
                    self.raise_error("The token is too long", chars)
                chars += self.fm.get_chars(1)
            return Token("REAL_NUMBER", chars)

        return Token("NATURAL_NUMBER", chars)

    def get_special_sign(self):
        chars = ""
        if self.fm.peek_chars(2) in comparison_operators:
            chars += self.fm.get_chars(2)
            return Token(comparison_operators[chars], chars)

        if self.fm.peek_chars(1) == "\"":
            self.fm.get_chars(1)
            while self.fm.peek_chars(1) != "\"":
                chars += self.fm.get_chars(1)
            self.fm.get_chars(1)
            return Token("TEXT", chars)

        chars += self.fm.get_chars(1)

        return Token(accepted_special_signs[chars], chars)

    def ignore_spaces(self):
        while(self.fm.peek_chars(1).isspace()):
            self.fm.get_chars(1)
        return

    def unexpected_sign(self):
        chars = ""
        chars += self.fm.get_chars(1)

        self.raise_error("ERROR - UNEXPECTED CHAR", chars)

    def end_of_file(self):
        return Token("END_OF_FILE", "")

    def raise_error(self, message, value):
        error_manager.manage_error(self.fm, value)
        raise error_manager.ErrorManager(message)