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

    def __init__(self, output_widget = None):
        self.memory = Memory()
        self.output_widget = output_widget

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

    @_('type IDENTIFIER ASSIGN expr SEMICOLON')
    def statement(self, p):
        print("type variable = value", p.expr)
        var_name = p.IDENTIFIER
        value = p.expr
        # print("Scope is", self.memory.scopes)
        # if self.memory.is_declared(var_name):
        #     raise ValueError(f"Variable '{var_name}' already declared in this scope.")
        # self.memory.set(variable_name=var_name, value=value, data_type=type(value))
        return ('declare', var_name, value)

    # Single or multiple variable declarations without assignments (e.g., int a; or int a, b, c;)
    @_('type ident_list SEMICOLON')
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
    

    # General rule for addition and string concatenation
    @_('expr PLUS expr')
    def expr(self, p):
        return ('plus', p.expr0, p.expr1)


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
        return p.STRING_LITERAL #.strip('"')  # Remove quotes from string literals

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
        # return ('identifier', var_name)
        # if var_name in self.memory:
        #     return self.memory.get(var_name)  # Looks up in current or outer scopes
        # else:
        #     raise ValueError(f'Hi! Undefined variable: {var_name}')
        return var_name
    
    # a = 2
    @_('IDENTIFIER ASSIGN expr SEMICOLON')
    def statement(self, p):
        var_name = p.IDENTIFIER
        print("Statement ", var_name)
        value = p.expr
        # Check if variable exists in any scope before updating
        # self.memory.get(var_name)  # Raises error if undefined
        # self.memory.set(variable_name=var_name, value=value, data_type=type(value))
        return ('update', var_name, value)

    # Parenthesized expression rule
    # @_('LPAREN expr RPAREN')
    # def expr(self, p):
    #     return p.expr  # Return the expression inside parentheses

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
    

    @_('IF LPAREN expr RPAREN LBRACE statements RBRACE')
    def statement(self, p):
        print("Processing if with block")
        condition = self.evaluate_expr(p.expr)
        if condition:
            self.memory.enter_scope()
            self.execute_statement(p.statements)
            self.memory.exit_scope()
        return ('if_block', p.expr, p.statements)

    @_('WHILE LPAREN expr RPAREN LBRACE statements RBRACE')
    def statement(self, p):
        print("Processing while block")
        condition = self.evaluate_expr(p.expr)
        while condition:
            self.memory.enter_scope()
            self.execute_statement(p.statements)
            self.memory.exit_scope()
            condition = self.evaluate_expr(p.expr)
        return ('while_block', p.expr, p.statements)


    @_('FUNCTION IDENTIFIER LPAREN RPAREN LBRACE statements RBRACE')
    def statement(self, p):
        print(f"Defining function {p.IDENTIFIER}")
        self.memory.enter_scope()  # Enter function scope
        function_body = p.statements  # Parse the body in this scope
        self.memory.set_function(p.IDENTIFIER, function_body)
        self.memory.exit_scope()  # Exit scope after parsing
        return ('function', p.IDENTIFIER)


    @_('IDENTIFIER LPAREN RPAREN SEMICOLON')
    def statement(self, p):
        function_name = p.IDENTIFIER
        print(f"Calling function {function_name}")
        function_body = self.memory.get_function(function_name)
        # if function_body:
        #     print("Entered scope")
        #     self.memory.enter_scope()  # Enter new scope for execution
        #     # self.execute_statement(function_body)  # Execute with local scope
        #     print("Exited scope")
        #     self.memory.exit_scope()  # Exit scope after execution
        # else:
        #     raise ValueError(f"Function '{function_name}' is not defined.")
        return ('call', function_name, function_body)


    def execute_statement(self, stmt):
        if isinstance(stmt, list):
            for s in stmt:
                self.execute_statement(s)
        elif isinstance(stmt, tuple):
            if stmt[0] == 'declare':
                var_name, value = stmt[1], stmt[2]
                # Only set if not already set globally during parsing
                if var_name not in self.memory.scopes[0]:  # Skip global declarations
                    if self.memory.is_declared(var_name):
                        raise ValueError(f"Variable '{var_name}' already declared in this scope.")
                    self.memory.set(variable_name=var_name, value=value, data_type=type(value))
            
            elif stmt[0] == 'update':
                var_name, value = stmt[1], stmt[2]
                # Only set if not already set globally during parsing
                # if var_name not in self.memory.scopes[0]:  # Skip global declarations
                if not self.memory.is_declared(var_name):
                    raise ValueError(f"Variable '{var_name}' not declared.")
                self.memory.set(variable_name=var_name, value=value, data_type=type(value))

            elif stmt[0] == 'print':
                value = self.evaluate_expr(stmt[1])
                self.output_widget.append("-> "+str(value))

            # elif stmt[0] == "plus":
            #     if isinstance(stmt[1], str) and isinstance(stmt[2], str):
            #         return stmt[1] + stmt[2]  # String concatenation
            #     elif isinstance(stmt[1], (int, float)) and isinstance(stmt[2], (int, float)):
            #         return stmt[1] + stmt[2]  # Numerical addition
            #     else:
            #         raise TypeError(f"Unsupported operands: {type(stmt[1])} + {type(stmt[2])}")

            elif stmt[0] == 'call':
                function_name = stmt[1]
                function_body = self.memory.get_function(function_name)
                if function_body:
                    self.memory.enter_scope()
                    self.execute_statement(function_body)
                    self.memory.exit_scope()
                else:
                    raise ValueError(f"Function '{function_name}' is not defined.")


    # Helper method to evaluate expressions at execution time
    def evaluate_expr(self, expr):
    # Case 1: String literal (starts and ends with quotes)
        if isinstance(expr, str) and expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]  # Strip the quotes and return the string literal
        
        # Case 2: Variable name
        if isinstance(expr, str): # and expr in self.memory.is_declared(expr):
            return self.memory.get(expr)  # Retrieve the variable value from memory
    
        elif isinstance(expr, (int, float, bool, str)):  # Literal value
            print("I should be here bro")
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
    
    @_('PRINT LPAREN expr RPAREN SEMICOLON')
    def statement(self, p):
        value = p.expr
        if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
            value =  value[1:-1]  # Strip the quotes and return the string literal
        # self.output_widget.append("-> " + str(value))
        return ('print', p.expr)  # Always return the AST representation

    # # Execute all statements after parsing
    def execute(self, ast):
        print("List is ", ast)
        if isinstance(ast, list):
            for stmt in (ast):
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