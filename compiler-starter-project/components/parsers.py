from sly import Parser
from components.lexica import Lexer
from components.memory import Memory

class ASTParser(Parser):
    debugfile = 'parser.out'
    start = 'statements'
    tokens = Lexer.tokens

    precedence = (
        ('left', 'EQ', 'NE'),
        ('left', 'LT', 'LE', 'GT', 'GE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'UMINUS'),  # Unary minus
    )

    def __init__(self, output_widget=None):
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

    # Typed declaration: [const] type IDENTIFIER = expr;
    # @_('CONST type IDENTIFIER ASSIGN expr SEMICOLON')
    # def statement(self, p):
    #     print(" I am const")
    #     return ('declare', p.type, p.IDENTIFIER, p.expr, p.lineno, True)

    @_('type IDENTIFIER ASSIGN expr SEMICOLON')
    def statement(self, p):
        print("I am variable")
        return ('declare', p.type, p.IDENTIFIER, p.expr, p.lineno, False)
    
    # Assignment
    @_('IDENTIFIER ASSIGN expr SEMICOLON')
    def statement(self, p):
        return ('assign', p.IDENTIFIER, p.expr, p.lineno)

    # @_('CONST type IDENTIFIER SEMICOLON')
    # def statement(self, p):
    #     return ('declare', p.type, p.IDENTIFIER, None, p.lineno, True)

    @_('type IDENTIFIER SEMICOLON')
    def statement(self, p):
        return ('declare', p.type, p.IDENTIFIER, None, p.lineno, False)

    # Print statement: print(expr);
    @_('PRINT LPAREN expr RPAREN SEMICOLON')
    def statement(self, p):
        return ('print', p.expr, p.lineno)

    # If statement: if (expr) { statements }
    @_('IF LPAREN expr RPAREN LBRACE statements RBRACE')
    def statement(self, p):
        return ('if', p.expr, p.statements)

    # If statement: if (expr) { statements } else {statements}
    @_('IF LPAREN expr RPAREN LBRACE statements RBRACE ELSE LBRACE statements RBRACE')
    def statement(self, p):
        return ('if_else', p.expr, p.statements0, p.statements1)

    # While statement: while (expr) { statements }
    @_('WHILE LPAREN expr RPAREN LBRACE statements RBRACE')
    def statement(self, p):
        return ('while', p.expr, p.statements)

    # # Function definition: function IDENTIFIER() { statements }
    # @_('FUNCTION IDENTIFIER LPAREN RPAREN LBRACE statements RBRACE')
    # def statement(self, p):
    #     return ('function', p.IDENTIFIER, p.statements)
    
        # Function: function IDENTIFIER(param_list) { statements }
    @_('VOID FUNCTION IDENTIFIER LPAREN param_list RPAREN LBRACE statements RBRACE')
    def statement(self, p):
        return ('function', None, p.IDENTIFIER, p.statements, p.param_list, p.lineno)
    
    @_('type FUNCTION IDENTIFIER LPAREN param_list RPAREN LBRACE statements RBRACE')
    def statement(self, p):
        return ('function', p.type, p.IDENTIFIER, p.statements, p.param_list, p.lineno)

    @_('RETURN expr SEMICOLON')
    def statement(self, p):
        print("I AM IN RETURN")
        return ('return', p.expr, p.lineno)

   # Function call
    @_('IDENTIFIER LPAREN arg_list RPAREN SEMICOLON')
    def statement(self, p):
        return ('call', p.IDENTIFIER, p.arg_list, p.lineno)

    # assign the function to a value
    @_('IDENTIFIER LPAREN arg_list RPAREN')
    def expr(self, p):
        print(f"Parsing expr call: {p.IDENTIFIER}()")
        return ('call', p.IDENTIFIER, p.arg_list, p.lineno)

    # Parameter list: [const] type IDENTIFIER, ...
    @_('CONST type IDENTIFIER')
    def param_list(self, p):
        return [('const', p.type, p.IDENTIFIER)]

    @_('type IDENTIFIER')
    def param_list(self, p):
        return [('var', p.type, p.IDENTIFIER)]

    @_('param_list COMMA CONST type IDENTIFIER')
    def param_list(self, p):
        return p.param_list + [('const', p.type, p.IDENTIFIER)]

    @_('param_list COMMA type IDENTIFIER')
    def param_list(self, p):
        return p.param_list + [('var', p.type, p.IDENTIFIER)]

    @_('')
    def param_list(self, p):
        return []

    # Argument list
    @_('expr')
    def arg_list(self, p):
        return [p.expr]

    @_('arg_list COMMA expr')
    def arg_list(self, p):
        return p.arg_list + [p.expr]

    @_('')
    def arg_list(self, p):
        return []
    

    # Type rules
    @_('TYPE_INT')
    def type(self, p):
        return int

    @_('TYPE_FLOAT')
    def type(self, p):
        return float

    @_('TYPE_BOOL')
    def type(self, p):
        return bool

    @_('TYPE_STRING')
    def type(self, p):
        return str

    # Expressions
    @_('expr PLUS expr')
    def expr(self, p):
        return ('plus', p.expr0, p.expr1)

    @_('expr MINUS expr')
    def expr(self, p):
        return ('minus', p.expr0, p.expr1)
    
    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return ('u_minus', p.expr)

    @_('expr TIMES expr')
    def expr(self, p):
        return ('times', p.expr0, p.expr1)

    @_('expr DIVIDE expr')
    def expr(self, p):
        return ('divide', p.expr0, p.expr1)

    @_('expr LT expr')
    def expr(self, p):
        return ('lt', p.expr0, p.expr1)

    @_('expr LE expr')
    def expr(self, p):
        return ('le', p.expr0, p.expr1)

    @_('expr GT expr')
    def expr(self, p):
        return ('gt', p.expr0, p.expr1)

    @_('expr GE expr')
    def expr(self, p):
        return ('ge', p.expr0, p.expr1)

    @_('expr EQ expr')
    def expr(self, p):
        return ('eq', p.expr0, p.expr1)

    @_('expr NE expr')
    def expr(self, p):
        return ('ne', p.expr0, p.expr1)

    # Literals
    @_('INT_LITERAL')
    def expr(self, p):
        return int(p.INT_LITERAL)

    @_('FLOAT_LITERAL')
    def expr(self, p):
        return float(p.FLOAT_LITERAL)

    @_('BOOL_LITERAL')
    def expr(self, p):
        return p.BOOL_LITERAL == "true"

    @_('STRING_LITERAL')
    def expr(self, p):
        return p.STRING_LITERAL.strip('"')

    # Variable reference
    @_('IDENTIFIER')
    def expr(self, p):
        return ('var', p.IDENTIFIER)

    # Parenthesized expression
    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    def get_default_value(self, var_type):
        if var_type == int:
            return 0
        elif var_type == float:
            return 0.0
        elif var_type == bool:
            return False
        elif var_type == str:
            return ""
        raise ValueError(f"Unknown type: {var_type}")

    def validate_type(self, value, declared_type):
        if declared_type == int and not isinstance(value, int):
            raise ValueError(f"Type mismatch: expected int, got {type(value).__name__}")
        elif declared_type == float and not isinstance(value, (int, float)):
            raise ValueError(f"Type mismatch: expected float, got {type(value).__name__}")
        elif declared_type == bool and not isinstance(value, bool):
            raise ValueError(f"Type mismatch: expected bool, got {type(value).__name__}")
        elif declared_type == str and not isinstance(value, str):
            raise ValueError(f"Type mismatch: expected string, got {type(value).__name__}")

    def evaluate_expr(self, expr):
        if isinstance(expr, tuple):
            op = expr[0]
            if op == 'var':
                if not self.memory.is_declared(expr[1]):
                    raise ValueError(f"Undefined variable: {expr[1]}")
                value = self.memory.get(expr[1])
                print(f"Evaluating var {expr[1]}: {value}")
                return value
            
            elif op == 'plus':
                left = self.evaluate_expr(expr[1])
                right = self.evaluate_expr(expr[2])
                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
                elif isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    return left + right
                else:
                    raise TypeError(f'Illegal operation "+" on {type(left)} and {type(right)}')
            
            elif op == 'minus':
                left = self.evaluate_expr(expr[1])
                right = self.evaluate_expr(expr[2])
                if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                    raise TypeError(f'Illegal operation "-" on {type(left)} and {type(right)}')
                return left - right
            
            elif op == 'u_minus':
                value = self.evaluate_expr(expr[1])
                if not isinstance(value, (int, float)):
                    raise ValueError(f"Unary minus applied to non-numeric value")
                return -value
            
            elif op == 'times':
                left = self.evaluate_expr(expr[1])
                right = self.evaluate_expr(expr[2])
                if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                    raise TypeError(f'Illegal operation "*" on {type(left)} and {type(right)}')
                return left * right
            
            elif op == 'divide':
                left = self.evaluate_expr(expr[1])
                right = self.evaluate_expr(expr[2])
                if right == 0:
                    raise ValueError("Division by zero")
                if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                    raise TypeError(f'Illegal operation "/" on {type(left)} and {type(right)}')
                return left / right
            
            elif op == 'lt':
                return self.evaluate_expr(expr[1]) < self.evaluate_expr(expr[2])
            elif op == 'le':
                return self.evaluate_expr(expr[1]) <= self.evaluate_expr(expr[2])
            elif op == 'gt':
                return self.evaluate_expr(expr[1]) > self.evaluate_expr(expr[2])
            elif op == 'ge':
                return self.evaluate_expr(expr[1]) >= self.evaluate_expr(expr[2])
            elif op == 'eq':
                return self.evaluate_expr(expr[1]) == self.evaluate_expr(expr[2])
            elif op == 'ne':
                return self.evaluate_expr(expr[1]) != self.evaluate_expr(expr[2])

            elif op == 'call':
                name, args, lineno = expr[1], expr[2], expr[3]
                print(f"Executing call: {name} at line {lineno}")
                func = self.memory.get_function(name)

                if func is None:
                    raise ValueError(f"Undefined function: {name} at line {lineno}")

                return_type, params, body = func  # Adjusted to match function tuple
                result = self.execute_call(name, args, lineno)

                if return_type is not None and result is None:
                    result = self.get_default_value(return_type)
                    # raise ValueError(f"Function {name} expected to return {return_type.__name__} at line {lineno}")
                    print("RETURNED DEFAULT VALUE FOR THE FUNCTION ", name)

                elif return_type is None and result is not None:
                    raise ValueError(f"Void function `{name}` cannot return any value.")
                
                self.validate_type(result, return_type)
                return result

        return expr  # Literal value (int, float, bool, str)

    def execute_statement(self, stmt):
        lineno = stmt[-1]
        print(f"Executing statement: {stmt}")
        if isinstance(stmt, list):
            for s in stmt:
                result = self.execute_statement(s)
                if result is not None:
                    return result
            return None
        elif isinstance(stmt, tuple):
            op = stmt[0]
            lineno = stmt[-1]
            if op == 'declare':
                var_type, var_name, expr, lineno, is_constant = stmt[1], stmt[2], stmt[3], stmt[4], stmt[5]
                print(f"Declaring {var_name} = {expr}")

                if self.memory.is_declared_in_current_scope(var_name):
                    raise ValueError(f"{'Constant' if is_constant else 'Variable'} '{var_name}' already declared at line {lineno}")

                if expr is None:
                    value = self.get_default_value(var_type)
                else:
                    value = self.evaluate_expr(expr)
                    self.validate_type(value, var_type)
                self.memory.set(var_name, value, var_type, is_constant)

            elif op == 'assign':
                var_name, expr, lineno = stmt[1], stmt[2], stmt[3]
                if not self.memory.is_declared(var_name):
                    raise ValueError(f"Variable '{var_name}' not declared at line {lineno}")

                if var_name in self.memory.constants:
                    raise ValueError(f"Cannot assign to constant '{var_name}' at line {lineno}")

                value = self.evaluate_expr(expr)
                var_type = self.memory.get_type(var_name)
                self.validate_type(value, var_type)
                self.memory.update(var_name, value, var_type)

            elif op == 'print':
                expr, lineno = stmt[1], stmt[2]
                value = self.evaluate_expr(expr)
                if self.output_widget:
                    self.output_widget.append(f"Line {lineno}: -> {value}")

            elif op == 'if':
                condition, statements = stmt[1], stmt[2]
                if self.evaluate_expr(condition):
                    self.memory.enter_scope()
                    result = self.execute_statement(statements)
                    self.memory.exit_scope()
                    return result

            elif op == 'if_else':
                condition, statements_true, statements_false = stmt[1], stmt[2], stmt[3]
                if self.evaluate_expr(condition):
                    self.memory.enter_scope()
                    result = self.execute_statement(statements_true)
                    self.memory.exit_scope()
                    return result
                else:
                    self.memory.enter_scope()
                    result = self.execute_statement(statements_false)
                    self.memory.exit_scope()
                    return result

            elif op == 'while':
                condition, statements = stmt[1], stmt[2]
                while self.evaluate_expr(condition):
                    self.memory.enter_scope()
                    result = self.execute_statement(statements)
                    self.memory.exit_scope()
                    if result is not None:
                        return result

            elif op == 'function':
                return_type, name, body, params = stmt[1], stmt[2], stmt[3], stmt[4]
                print(f"Storing function: {name}")
                self.memory.set_function(name, (return_type, params, body))

            elif op == 'call':
                name, args, lineno = stmt[1], stmt[2], stmt[3]
                print(f"Executing statement call: {name} at line {lineno}")
                result = self.execute_call(name, args, lineno)
                return result

            elif op == 'return':
                expr = stmt[1]
                value = self.evaluate_expr(expr)
                print("RETURNED VALUE", value)
                return value

            else:
                raise ValueError(f"Unknown operation '{op}' at line {lineno}")
        else:
            raise ValueError(f"Invalid statement: {stmt} at line {lineno}")
        return None

    def execute_call(self, name, args, lineno):
        func = self.memory.get_function(name)
        if func is None:
            raise ValueError(f"Undefined function: {name} at line {lineno}")
        return_type, params, body = func
        if len(args) != len(params):
            raise ValueError(f"Expected {len(params)} arguments, got {len(args)} at line {lineno}")
        
        self.memory.enter_scope()

        for (param_mode, param_type, param_name), arg in zip(params, args):
            if param_mode == 'const':
                if isinstance(arg, tuple) and arg[0] == 'var':
                    arg_name = arg[1]
                    # if arg_name not in self.memory.constants:
                    #     raise ValueError(f"Cannot pass non-constant variable '{arg_name}' as constant parameter at line {lineno}")
                    value = self.evaluate_expr(arg)
                elif isinstance(arg, (int, float, str, bool)):
                    value = arg
                # else:
                #     raise ValueError(f"Constant parameter '{param_name}' requires a constant variable or literal at line {lineno}")
                self.validate_type(value, param_type)
                self.memory.set(param_name, value, param_type, is_constant=True)

            elif param_mode == 'var':
                    if not isinstance(arg, tuple) or arg[0] != 'var':
                        raise ValueError(f"Variable parameter '{param_name}' requires a variable, got expression at line {lineno}")
                    arg_name = arg[1]
                    if not self.memory.is_declared(arg_name):
                        raise ValueError(f"Undefined variable: {arg_name} at line {lineno}")
                    if arg_name in self.memory.constants:
                        raise ValueError(f"Cannot pass constant '{arg_name}' as variable parameter at line {lineno}")
                    scope, var_type, ref_var = self.memory.get_variable_ref(arg_name)
                    self.validate_type(self.memory.get(arg_name), param_type)
                    self.memory.scopes[-1][param_name] = (scope, var_type, ref_var)

        result = self.execute_statement(body)
        self.memory.exit_scope()
        return result

    def execute(self, ast):
        self.execute_statement(ast)


# if __name__ == "__main__":
#     lexer = Lexer()  # Initialize Lexer
#     parser = ASTParser()  # Initialize the Parser

#     # Example input with multiple statements
#     input_code = """
#     for (int i = 0; i < 5; i = i + 1) {
#         print(i);
#     }
#     """
#     tokens = lexer.tokenize(input_code)  # Tokenize the input
#     token_list = [t for t in tokens]
#     print("Token stream:", token_list)
    
#     # Parse the token list
#     result = parser.parse(tokens)
#     print("Parse result:", result)  # Should output something like: [('declare', 'a', 2), ('declare', 'b', 3)]









    