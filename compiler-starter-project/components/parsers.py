from components.lexica import MyLexer
from components.memory import Memory
from sly import Parser
from components.lexica import MyLexer

# class MyParser(Parser):
#     debugfile = 'parser.out'
#     start = 'statement'
#     # Get the token list from the lexer (required)
#     tokens = MyLexer.tokens
#     precedence = (
#         ('left', "+", MINUS),
#         ('left', TIMES, DIVIDE),
#         ('right', UMINUS),
#         )

#     def __init__(self):
#         self.memory:Memory = Memory()

#     @_('NAME ASSIGN expr')
#     def statement(self, p):
#         var_name = p.NAME
#         value = p.expr
#         self.memory.set(variable_name=var_name,value=value, data_type=type(value))
#         # Note that I did not return anything

#     @_('expr')
#     # S -> E
#     def statement(self, p) -> int:
#         return p.expr

#     # The example with literals
#     @_('expr "+" expr')
#     # E -> E + E
#     def expr(self, p):
#         # You can refer to the token 2 ways
#         # Way1: using array
#         print(p[0], p[1], p[2])
#         # Way2: using symbol name. 
#         # Here, if you have more than one symbols with the same name
#         # You have to indiciate the number at the end.
#         return p.expr0 + p.expr1

#     # The example with normal token
#     @_('expr MINUS expr')
#     def expr(self, p):
#         print(p[0], p[1], p[2])
#         return p.expr0 - p.expr1

#     @_('expr TIMES expr')
#     def expr(self, p):
#         return p.expr0 * p.expr1

#     @_('expr DIVIDE expr')
#     def expr(self, p):
#         return p.expr0 / p.expr1

#     # https://sly.readthedocs.io/en/latest/sly.html#dealing-with-ambiguous-grammars
#     # `%prec UMINUS` is the way to override the `precedence` of MINUS to UMINUS.
#     @_('MINUS expr %prec UMINUS')
#     def expr(self, p):
#         return -p.expr

#     @_('LPAREN expr RPAREN')
#     def expr(self, p):
#         return p.expr

#     @_('NUMBER')
#     def expr(self, p):
#         return int(p.NUMBER)
    
#     # def is_prefix(self, p_tokens):
#     #     all_symbols = []

#     #     for token in p_tokens:
#     #         all_symbols.append(token.value)
#     #         yield token
            
#     #     print("All symbols", all_symbols)
#     #     # If first token is an operator and we have at least 3 tokens
#     #     return all_symbols[0] in {'+', '*'} and len(all_symbols) >= 3


#     # def parse_prefix(self, tokens):
#     #     """Evaluate prefix expression"""
#     #     if not tokens:
#     #         return 0
        
#     #     stack = []
#     #     # Reverse tokens since prefix is evaluated right to left
#     #     for token in reversed(tokens):
#     #         if token in {'+', '*'}:
#     #             operand1 = stack.pop()
#     #             operand2 = stack.pop()
#     #             if token == '+':
#     #                 stack.append(operand1 + operand2)
#     #             elif token == '*':
#     #                 stack.append(operand1 * operand2)
#     #         else:
#     #             stack.append(float(token))
#     #     return stack[0]

#     def parse(self, tokens):
#         # isTokenPrefix = self.is_prefix(tokens)
#         return super().parse(tokens)



class PrefixParser(Parser):
    debugfile = 'parser.out'
    start = 'statement'
    tokens = MyLexer.tokens
    precedence = (
        ('left', "+", MINUS),
        ('left', TIMES, DIVIDE),
        ('right', UMINUS),
    )

    def __init__(self, output_widget=None):
        self.memory = Memory()
        self.infix_stack = []  # stack to build infix expr


    def get_infix(self):
        return self.infix_stack[0] if self.infix_stack else ""


    @_('NAME ASSIGN expr')
    def statement(self, p):
        var_name = p.NAME
        value = p.expr
        self.memory.set(variable_name=var_name, value=value, data_type=type(value))
        self.infix_stack = [f"{var_name} = {self.infix_stack[0]}"]  # Update infix with assignment

    @_('expr')
    def statement(self, p) -> int:
        result = p.expr
        return result

    @_('"+" expr expr')
    def expr(self, p):
        result = p.expr0 + p.expr1
        # Pop two infix sub-expressions and combine them
        right = self.infix_stack.pop()
        left = self.infix_stack.pop()

        self.infix_stack.append(f"({left} + {right})")
        return result

    # @_('MINUS expr expr')
    # def expr(self, p):
    #     result = p.expr0 - p.expr1

    #     right = self.infix_stack.pop()
    #     left = self.infix_stack.pop()

    #     self.infix_stack.append(f"({left} - {right})")
    #     return result

    @_('TIMES expr expr')
    def expr(self, p):
        result = p.expr0 * p.expr1

        right = self.infix_stack.pop()
        left = self.infix_stack.pop()

        self.infix_stack.append(f"({left} * {right})")
        return result

    # @_('DIVIDE expr expr')
    # def expr(self, p):
    #     result = p.expr0 / p.expr1

    #     right = self.infix_stack.pop()
    #     left = self.infix_stack.pop()
        
    #     self.infix_stack.append(f"({left} / {right})")
    #     return result

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        result = -p.expr

        expr = self.infix_stack.pop()

        self.infix_stack.append(f"-{expr}")
        return result

    # @_('LPAREN expr RPAREN')
    # def expr(self, p):
    #     return p.expr

    @_('NUMBER')
    def expr(self, p):
        num = int(p.NUMBER)
        self.infix_stack.append(str(num))
        return num

    def parse(self, tokens):
        self.infix_stack = []  # reset
        return super().parse(tokens)


from components.ast.statement import Expression, Expression_math, Expression_number, Operations
class ASTParser(Parser):
    debugfile = 'parser.out'
    start = 'statement'
    # Get the token list from the lexer (required)
    tokens = MyLexer.tokens
    precedence = (
        ('left', "+", MINUS),
        # ('left', TIMES, DIVIDE),
        # ('right', UMINUS),
        )

    @_('expr')
    def statement(self, p) -> int:
        p.expr.run()
        return p.expr.value

    @_('expr "+" expr')
    def expr(self, p) -> Expression:
        parameter1 = p.expr0
        parameter2 = p.expr1
        expr = Expression_math(operation=Operations.PLUS, parameter1=parameter1, parameter2=parameter2)
        return expr
    
    @_('expr MINUS expr')
    def expr(self, p) -> Expression:
        parameter1 = p.expr0
        parameter2 = p.expr1
        expr = Expression_math(operation=Operations.MINUS, parameter1=parameter1, parameter2=parameter2)
        return expr

    @_('NUMBER')
    def expr(self, p) -> Expression:
        return Expression_number(number=p.NUMBER)
        
        

        
if __name__ == "__main__":
    lexer = MyLexer()
    # parser = MyParser()
    text = "9 + 2 + 3"
    memory = Memory()
    parser = ASTParser()
    # text = "1 + 2 + 3"
    result = parser.parse(lexer.tokenize(text))
    print(result)
    # print(memory)