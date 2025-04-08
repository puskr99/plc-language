from sly import Parser
from components.lexica import Lexer
from components.memory import Memory

class ASTParser(Parser):
    debugfile = 'parser.out'
    start = 'statements'  # Start with 'statements' to handle multiple statements
    tokens = Lexer.tokens  # Use the tokens from the Lexer class

    precedence = (
        ('left', 'PLUS', 'MINUS'),  # Left-associative for plus and minus
        ('left', 'TIMES', 'DIVIDE'),  # Left-associative for multiplication and division
        ('nonassoc', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NE'),
    )

    def __init__(self):
        self.memory = Memory()

    # Rule for handling multiple statements
    @_('statement SEMICOLON statements')
    def statements(self, p):
        return [p.statement] + p.statements  # Combine statements into a list

    # Base case: single statement
    @_('statement SEMICOLON')
    def statements(self, p):
        return [p.statement]  # Single statement as a list
    
    # Allow standalone statements without semicolon (e.g., if)
    @_('statements statement')
    def statements(self, p):
        print("Combining statements without semicolon")
        return p.statements + [p.statement]

    @_('statement')
    def statements(self, p):
        print("Single statement without semicolon")
        return [p.statement]

    # Rule to handle variable declarations with any type (int, float, bool, string)
    @_('type IDENTIFIER ASSIGN expr')
    def statement(self, p):
        print("type variable = value", p.expr)
        var_name = p.IDENTIFIER
        value = p.expr
        if var_name in self.memory:
            raise ValueError(f"Variable '{var_name}' already declared.")
        self.memory.set(variable_name=var_name, value=value, data_type=type(value))
        return ('declare', var_name, value)

    # Single or multiple variable declarations without assignments (e.g., int a; or int a, b, c;)
    @_('type ident_list')
    def statement(self, p):
        print("type variables without value")
        # Process each identifier in the list
        default_value = self.get_default_value(p.type)
        declarations = []
        for var_name in p.ident_list:
            if var_name in self.memory:
                raise ValueError(f"Variable '{var_name}' already declared.")
            self.memory.set(variable_name=var_name, value=default_value, data_type=p.type)
            declarations.append(('declare', var_name, default_value))
        return declarations if len(declarations) > 1 else declarations[0]

    # List of identifiers (e.g., a or a, b, c)
    @_('IDENTIFIER')
    def ident_list(self, p):
        return [p.IDENTIFIER]

    @_('ident_list COMMA IDENTIFIER')
    def ident_list(self, p):
        return p.ident_list + [p.IDENTIFIER]

    # Helper method to assign default values based on type
    def get_default_value(self, var_type):
        if var_type == int:
            return 0
        elif var_type == float:
            return 0.0
        elif var_type == bool:
            return False
        elif var_type == str:
            return ""
        else:
            return None  # Fallback for unsupported types


    # Rule for print statement (e.g., print(1 + 2);)
    @_('PRINT LPAREN expr RPAREN')
    def statement(self, p):
        value = p.expr  # Get the evaluated value of the expression
        print("Print called with ",value)  # Print the result
        return ('print', value)  # Return a tuple representing the print statement
    

    # General rule for addition and string concatenation
    @_('expr PLUS expr')
    def expr(self, p):
        if isinstance(p.expr0, str) and isinstance(p.expr1, str):
            return p.expr0 + p.expr1  # String concatenation
        elif isinstance(p.expr0, (int, float)) and isinstance(p.expr1, (int, float)):
            return p.expr0 + p.expr1  # Numerical addition
        else:
            raise TypeError(f"Unsupported operands: {type(p.expr0)} + {type(p.expr1)}")


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
        print("Variable: ", var_name)
        if var_name in self.memory:
            return self.memory.get(var_name)  # Look up the value of the variable from memory
        else:
            raise ValueError(f"Undefined variable: {var_name}")
    
    # a = 2
    @_('IDENTIFIER ASSIGN expr')
    def statement(self, p):
        var_name = p.IDENTIFIER
        print("Statement ", var_name)

        if var_name not in self.memory:
            raise ValueError(f"Variable {var_name} not declared.")  # Ensure variable is declared

        value = p.expr  # The value to assign
        self.memory.set(variable_name=var_name, value=value, data_type=type(value))  # Update memory
        return ('update', var_name, value)


    # Parenthesized expression rule
    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr  # Return the expression inside parentheses
    

    # Rules for comparison expressions
    @_('expr LT expr')  # Less than
    def expr(self, p):
        print("Exp less than exp ", p.expr0," ", p.expr1)
        return p.expr0 < p.expr1

    @_('expr LE expr')  # Less than or equal to
    def expr(self, p):
        return p.expr0 <= p.expr1

    @_('expr GT expr')  # Greater than
    def expr(self, p):
        return p.expr0 > p.expr1

    @_('expr GE expr')  # Greater than or equal to
    def expr(self, p):
        return p.expr0 >= p.expr1

    @_('expr EQ expr')  # Equal to
    def expr(self, p):
        return p.expr0 == p.expr1

    @_('expr NE expr')  # Not equal to
    def expr(self, p):
        return p.expr0 != p.expr1
    

    # If-Else rule
    @_('IF LPAREN expr RPAREN LBRACE statements RBRACE ELSE LBRACE statements RBRACE')
    def statement(self, p):
        print("Inside If condiditon")
        condition = p.expr  # The condition to evaluate (p.expr will be the expression)
        if condition:  # Evaluate the condition
            print("Executing 'if' block")
            self.execute_statement(p.statements0)  # Execute the 'if' block (p.statements0 contains the list of statements)
        else:
            print("Executing 'else' block")
            self.execute_statement(p.statements1)  # Execute the 'else' block (p.statements1 contains the list of statements)

    # If statement with block (e.g., if (a < b) { print(a); })
    @_('IF LPAREN expr RPAREN LBRACE statements RBRACE')
    def statement(self, p):
        print("Processing if with block")
        return ('if_block', p.expr, p.statements)

    # while statement
    @_('WHILE LPAREN expr RPAREN LBRACE statements RBRACE')
    def statement(self, p):
        print("Processing while block")
        return ('while_block', p.expr, p.statements)

    # Helper method to execute statements
    def execute_statement(self, stmt):
        if isinstance(stmt, list):
            for s in stmt:
                self.execute_statement(s)
        elif isinstance(stmt, tuple):
            if stmt[0] == 'declare':
                var_name, value = stmt[1], stmt[2]
                self.memory.set(variable_name=var_name, value=value, data_type=type(value))
            elif stmt[0] == 'update':
                var_name, value = stmt[1], stmt[2]
                self.memory.set(variable_name=var_name, value=value, data_type=type(value))
            elif stmt[0] == 'print':
                value = self.evaluate_expr(stmt[1])
                print(value)
            elif stmt[0] == 'if':
                condition = self.evaluate_expr(stmt[1])
                if condition:
                    self.execute_statement(stmt[2])
            elif stmt[0] == 'if_block':
                condition = self.evaluate_expr(stmt[1])
                if condition:
                    for s in stmt[2]:
                        self.execute_statement(s)
            elif stmt[0] == 'while_block':
                condition = self.evaluate_expr(stmt[1])
                while condition:
                    for s in stmt[2]:
                        self.execute_statement(s)
                    condition = self.evaluate_expr(stmt[1])  # Re-evaluate condition each iteration


    # Helper method to evaluate expressions at execution time
    def evaluate_expr(self, expr):
        if isinstance(expr, str):  # Identifier
            if expr in self.memory:
                return self.memory.get(expr)
            raise ValueError(f"Undefined variable: {expr}")
        elif isinstance(expr, (int, float, bool, str)):  # Literal value
            return expr
        elif isinstance(expr, tuple):  # Binary operation or comparison
            if expr[0] == '<':
                left = self.evaluate_expr(expr[1])
                right = self.evaluate_expr(expr[2])
                return left < right
            elif expr[0] == '+':
                left = self.evaluate_expr(expr[1])
                right = self.evaluate_expr(expr[2])
                return left + right
        return expr

    # Execute all statements after parsing
    def execute(self, ast):
        if isinstance(ast, list):
            for stmt in ast:
                self.execute_statement(stmt)


if __name__ == "__main__":
    lexer = Lexer()  # Initialize Lexer
    parser = ASTParser()  # Initialize the Parser

    # Example input with multiple statements
    input_code = """
    for (int i = 0; i < 5; i = i + 1) {
        print(i);
    }
    """
    tokens = lexer.tokenize(input_code)  # Tokenize the input
    token_list = [t for t in tokens]
    print("Token stream:", token_list)
    
    # Parse the token list
    result = parser.parse(tokens)
    print("Parse result:", result)  # Should output something like: [('declare', 'a', 2), ('declare', 'b', 3)]