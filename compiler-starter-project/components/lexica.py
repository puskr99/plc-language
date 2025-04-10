from sly import Lexer

class Lexer(Lexer):
    # List of token names
    tokens = {
        PRINT, TYPE_INT, TYPE_FLOAT, TYPE_BOOL, TYPE_STRING,
        BOOL_LITERAL, STRING_LITERAL, FLOAT_LITERAL, INT_LITERAL, IDENTIFIER,
        ASSIGN, SEMICOLON, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN, LBRACE, RBRACE,
        FOR, LT, GT, LE, GE, EQ, NE, COMMA, IF, ELSE, WHILE, FUNCTION
    }

    # Ignore spaces and tabs
    ignore = ' \t\n'

    # Define token patterns
    FUNCTION = r'function'
    PRINT = r'print'
    TYPE_INT = r'int'
    TYPE_FLOAT = r'float'
    TYPE_BOOL = r'bool'
    TYPE_STRING = r'string'
    FOR = r'for'
    EQ = r'=='
    NE = r'!='
    LE = r'<='
    GE = r'>='
    LT = r'<'
    GT = r'>'
    ASSIGN = r'='
    SEMICOLON = r';'
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACE = r'\{'
    RBRACE = r'\}'
    BOOL_LITERAL = r'true|false'
    STRING_LITERAL = r'"[^"]*"'
    FLOAT_LITERAL = r'\d+\.\d+'
    INT_LITERAL = r'\d+'
    IF = r'if'
    ELSE = r'else'
    COMMA = r','
    WHILE = r'while'
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'




    # Error handling
    def error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        self.index += 1  # Skip over the bad character


# if __name__ == "__main__":
#     lexer = Lexer()  # Initialize the Lexer

#     input_code = "int a = 2;"  # Example input
#     tokens = lexer.tokenize(input_code)  # Tokenize the input

#     # Parse the token list directly (no need to pass 'tokens=')
#     result = Parser().parse(tokens)

#     print(result)  # Print the result of the parsing
