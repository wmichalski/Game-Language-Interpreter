from Lekser.file_manager import FileManager
from Lekser.token import Token, keyword_types, accepted_special_signs, comparison_operators

class Tokeniser:
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
        while (self.fm.peek_chars(1).isalpha() or self.fm.peek_chars(1).isdigit()):
            chars += self.fm.get_chars(1)

        if (self.fm.peek_chars(1) == "."):
            if ((chars != "player") and (chars != "chosen")and (chars != "game")):
                raise ValueError("Found dot, but the keyword before it doesnt match neither 'player' nor 'chosen' nor 'game'")

            chars += self.fm.get_chars(1)

            if not (self.fm.peek_chars(1).isalpha()):
                raise ValueError("Found dot, but no variable name afterwards")

            while (self.fm.peek_chars(1).isalpha() or self.fm.peek_chars(1).isdigit()):
                chars += self.fm.get_chars(1)

        if chars in keyword_types.keys():
            return Token("KEYWORD", chars)
        else:
            return Token("NAME", chars)

    def get_number_token(self):
        chars = ""

        if self.fm.peek_chars(1) == "0":
            chars += self.fm.get_chars(1)

            if self.fm.peek_chars(1) == ".":
                chars += self.fm.get_chars(1)
                while (self.fm.peek_chars(1).isdigit()):
                    chars += self.fm.get_chars(1)

                return Token("REAL_NUMBER", chars)
            
            if self.fm.peek_chars(1).isdigit():
                raise ValueError("Number can't start with a 0 (unless it is a 0 itself)")

            return Token("REAL_NUMBER", chars) # not sure how to treat a zero

        while (self.fm.peek_chars(1).isdigit()):
            chars += self.fm.get_chars(1)

        if self.fm.peek_chars(1) == "." and self.fm.peek_chars(2)[-1].isdigit():
            chars += self.fm.get_chars(1)
            while (self.fm.peek_chars(1).isdigit()):
                chars += self.fm.get_chars(1)
            return Token("REAL_NUMBER", chars)

        return Token("NATURAL_NUMBER", chars)

    def get_special_sign(self):
        chars = ""
        if self.fm.peek_chars(2) in comparison_operators:
            chars += self.fm.get_chars(2)
            return Token(comparison_operators[chars], chars)

        chars += self.fm.get_chars(1)
        return Token(accepted_special_signs[chars], chars)

    def ignore_spaces(self):
        while(self.fm.peek_chars(1).isspace()):
            self.fm.get_chars(1)
        return

    def unexpected_sign(self):
        chars = ""
        chars += self.fm.get_chars(1)

        return Token("ERROR", chars)

    def end_of_file(self):
        return Token("END_OF_FILE", "")