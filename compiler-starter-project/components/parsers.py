from sly import Parser
from components.lexica import Lexer
from components.memory import Memory

class ASTParser(Parser):
    debugfile = 'parser.out'
    start = 'statement'  # Start with 'statements' to handle multiple statements
    tokens = Lexer.tokens  # Use the tokens from the Lexer class

    precedence = (
        ('left', 'PLUS', 'MINUS'),  # Left-associative for plus and minus
        ('left', 'TIMES', 'DIVIDE'),  # Left-associative for multiplication and division
    )

    def __init__(self, output_widget=None):
        self.memory = Memory()

    # Rule for handling multiple statements
    # @_('statement SEMICOLON statements')
    # def statements(self, p):
    #     return p.statement + p.statements  # Combine statements into a list

    # Allow for no further statements after a single one
    # @_('statement SEMICOLON')
    # def statements(self, p):
    #     return p.statement  # Single statement (base case)

    # Rule to handle variable declarations with any type (int, float, bool, string)
    @_('type IDENTIFIER ASSIGN expr SEMICOLON')
    def statement(self, p):
        var_name = p.IDENTIFIER  # The name of the variable
        value = p.expr  # The value assigned to the variable
        self.memory.set(variable_name=var_name, value=value, data_type=type(value))  # Store in memory
        return None  # Return the assigned value
    

    # Rule for print statement (e.g., print(1 + 2);)
    @_('PRINT LPAREN expr RPAREN SEMICOLON')
    def statement(self, p):
        value = p.expr  # Get the evaluated value of the expression
        print(value)  # Print the result
        return value  # Return the value for further processing

    # Rule for expressions (arithmetic operations)
    @_('expr PLUS expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr MINUS expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('expr TIMES expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr DIVIDE expr')
    def expr(self, p):
        return p.expr0 / p.expr1

    # Literal rules for INT, FLOAT, BOOL, and STRING
    @_('INT_LITERAL')
    def expr(self, p):
        return int(p.INT_LITERAL)

    @_('FLOAT_LITERAL')
    def expr(self, p):
        return float(p.FLOAT_LITERAL)

    @_('BOOL_LITERAL')
    def expr(self, p):
        return True if p.BOOL_LITERAL == "true" else False

    @_('STRING_LITERAL')
    def expr(self, p):
        return p.STRING_LITERAL.strip('"')  # Remove quotes from string literals

    # Define rule for variable type (int, float, bool, string)
    @_('TYPE_INT') 
    def type(self, p):
        return int  # Return the type for integers
    
    @_('TYPE_FLOAT') 
    def type(self, p):
        return float  # Return the type for floats

    @_('TYPE_BOOL') 
    def type(self, p):
        return bool  # Return the type for booleans

    @_('TYPE_STRING') 
    def type(self, p):
        return str  # Return the type for strings
    
    # Handle variable lookup from memory (when encountering an identifier)
    @_('IDENTIFIER')
    def expr(self, p):
        var_name = p.IDENTIFIER
        if var_name in self.memory:
            return self.memory.get(var_name)  # Look up the value of the variable from memory
        else:
            raise ValueError(f"Undefined variable: {var_name}")
    
    # Parenthesized expression rule
    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr  # Return the expression inside parentheses


# if __name__ == "__main__":
#     lexer = Lexer()  # Initialize Lexer with some code to tokenize
#     parser = ASTParser()  # Initialize the Parser

#     input_code = "int a = 2; int b = 3;"  # Example input
#     tokens = lexer.tokenize(input_code)  # Tokenize the input
#     print(f"Here {tokens}")
#     # Parse the token list directly (no need to pass 'tokens=')
#     result = parser.parse(tokens)

#     print(result)  # Print the result of the parsing
