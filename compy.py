# ---------------------------
# 1. ANALISE LÉXICA (LEXER)
# ---------------------------

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
    
    def advance(self):
        self.pos += 1
    
    def current(self):
        return self.text[self.pos] if self.pos < len(self.text) else None
    
    def generate_tokens(self):
        tokens = []
        while self.current() is not None:
            char = self.current()
            
            if char.isspace():
                self.advance()
            elif char.isdigit():
                tokens.append(self.number())
            elif char == '+':
                tokens.append(Token('PLUS')); self.advance()
            elif char == '-':
                tokens.append(Token('MINUS')); self.advance()
            elif char == '*':
                tokens.append(Token('MUL')); self.advance()
            elif char == '/':
                tokens.append(Token('DIV')); self.advance()
            elif char == '(':
                tokens.append(Token('LPAREN')); self.advance()
            elif char == ')':
                tokens.append(Token('RPAREN')); self.advance()
            else:
                raise Exception("Caractere inválido: " + char)
        tokens.append(Token('EOF'))
        return tokens
    
    def number(self):
        num = ""
        while self.current() is not None and self.current().isdigit():
            num += self.current()
            self.advance()
        return Token('NUMBER', int(num))

# ---------------------------
# 2. ANALISE SINTÁTICA (PARSER)
# ---------------------------

class NumberNode:
    def __init__(self, value):
        self.value = value

class BinOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def current(self):
        return self.tokens[self.pos]
    
    def eat(self, type_):
        if self.current().type == type_:
            self.pos += 1
        else:
            raise Exception(f"Esperado {type_}")
    
    def parse(self):
        return self.expr()
    
    def expr(self):
        node = self.term()
        while self.current().type in ['PLUS', 'MINUS']:
            op = self.current()
            self.eat(op.type)
            node = BinOpNode(node, op, self.term())
        return node
    
    def term(self):
        node = self.factor()
        while self.current().type in ['MUL', 'DIV']:
            op = self.current()
            self.eat(op.type)
            node = BinOpNode(node, op, self.factor())
        return node
    
    def factor(self):
        tok = self.current()
        if tok.type == 'NUMBER':
            self.eat('NUMBER')
            return NumberNode(tok.value)
        elif tok.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.expr()
            self.eat('RPAREN')
            return node
        else:
            raise Exception("Fator inválido")

# ---------------------------
# 3. GERAÇÃO DE CÓDIGO
# ---------------------------

class CodeGen:
    def __init__(self):
        self.instructions = []
    
    def generate(self, node):
        if isinstance(node, NumberNode):
            self.instructions.append(f"PUSH {node.value}")
        elif isinstance(node, BinOpNode):
            self.generate(node.left)
            self.generate(node.right)
            self.instructions.append(self.op_to_instr(node.op.type))
        return self.instructions
    
    def op_to_instr(self, op):
        return {
            'PLUS': 'ADD',
            'MINUS': 'SUB',
            'MUL': 'MUL',
            'DIV': 'DIV'
        }[op]

# ---------------------------
# EXECUÇÃO
# ---------------------------

text = "8 + 3 * (2 - 1)"
lexer = Lexer(text)
tokens = lexer.generate_tokens()

parser = Parser(tokens)
ast = parser.parse()

codegen = CodeGen()
instr = codegen.generate(ast)

print("Código gerado:")
for i in instr:
    print(i)
