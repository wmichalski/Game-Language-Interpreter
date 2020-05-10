class Token:
    def __init__(self, token_type, value=None):
        self.type = token_type
        self.value = value


keyword_types = {
    "or": "LOGICAL_OR",
    "and": "LOGICAL_AND",
    "return": "RETURN",
    "def": "FUNCTION_DEF",
    "var": "VARIABLE_ASSIGN",
    "while": "WHILE",
    "if": "IF",
    "choice": "CHOICE",
    "forEachPlayer": "FOR_EACH_PLAYER",
    "roll": "ROLL",
    "else": "ELSE",
    "break": "BREAK",
    "PLAYERS": "PLAYERS",
    "GAME": "GAME",
    "INDIVIDUAL": "INDIVIDUAL",
    "FUNCTIONS": "FUNCTIONS",
    "RUN": "RUN",
    "WIN": "WIN",
}

accepted_special_signs = {
    "(": "LEFT_ROUND",
    ")": "RIGHT_ROUND",
    "{": "LEFT_CURLY",
    "}": "RIGHT_CURLY",
    "+": "PLUS",
    "-": "MINUS",
    "*": "MULTIPLICATION",
    "/": "DIVISION",
    "=": "ASSIGNMENT",
    "<": "LOWER",
    ">": "GREATER",
    "[": "LEFT_SQUARE",
    "]": "RIGHT_SQUARE",
    ":": "COLON",
    "!": "LOGICAL_NOT",
    ";": "SEMICOLON",
    ",": "COMMA"
}

comparison_operators = {
    "==": "EQUAL_TO",
    "!=": "NOT_EQUAL_TO",
    "<=": "LOWER_OR_EQUAL",
    ">=": "GREATER_OR_EQUAL"
}

nest_tokens = {
    
}