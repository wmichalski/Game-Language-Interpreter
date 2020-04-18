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
    "PLAYERS": "PLAYERS",
    "GAME": "GAME",
    "INDIVIDUAL": "INDIVIDUAL",
    "FUNCTIONS": "FUNCTIONS",
    "RUN": "RUN",
    "WIN": "WIN",
}

accepted_special_signs = {
    "(": "( OPERATOR",
    ")": ") OPERATOR",
    "{": "{ OPERATOR",
    "}": "} OPERATOR",
    "+": "+/- OPERATOR",
    "-": "+/- OPERATOR",
    "*": "*// OPERATOR",
    "/": "*// OPERATOR",
    "=": "= OPERATOR",
    "<": "< OPERATOR",
    ">": "> OPERATOR",
    "[": "[ OPERATOR",
    "]": "] OPERATOR",
    ":": ": OPERATOR",
    "!": "! OPERATOR",
    ";": "; OPERATOR"
}

comparison_operators = {
    "==": "EQUAL_TO",
    "!=": "NOT_EQUAL_TO",
    "<=": "LOWER_OR_EQUAL",
    ">=": "GREATER_OR_EQUAL"
}
