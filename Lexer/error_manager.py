import sys
from Lexer import file_manager

class ErrorManager(Exception):
    def __init__(self, message):
        self.message = message

FAULTY_CODE_PEEK = 25

def manage_error(file_manager, value):
    position = file_manager.get_position()
    faulty_code = file_manager.get_errory_part(position, FAULTY_CODE_PEEK)
    print("Found error in this part:\n" + "..." + " " + faulty_code + " " + "...")