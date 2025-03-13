from rply import LexerGenerator

class Lexer:
    def __init__(self):
        self.lexer = LexerGenerator()
        self._add_tokens()

    def _add_tokens(self):
        # Keywords
        self.lexer.add('FUNCTION', r'fn')
        self.lexer.add('CLASS', r'class')
        self.lexer.add('LET', r'let')
        self.lexer.add('CONST', r'const')
        self.lexer.add('IF', r'if')
        self.lexer.add('ELSE', r'else')
        self.lexer.add('WHILE', r'while')
        self.lexer.add('FOR', r'for')
        self.lexer.add('RETURN', r'return')
        self.lexer.add('IMPORT', r'import')
        self.lexer.add('FROM', r'from')
        self.lexer.add('AS', r'as')
        self.lexer.add('PUBLIC', r'public')
        self.lexer.add('PRIVATE', r'private')
        self.lexer.add('PROTECTED', r'protected')
        self.lexer.add('STATIC', r'static')
        self.lexer.add('ASYNC', r'async')
        self.lexer.add('AWAIT', r'await')
        self.lexer.add('NEW', r'new')

        # Types
        self.lexer.add('TYPE_INT', r'int')
        self.lexer.add('TYPE_FLOAT', r'float')
        self.lexer.add('TYPE_STRING', r'string')
        self.lexer.add('TYPE_BOOL', r'bool')
        self.lexer.add('TYPE_VOID', r'void')
        self.lexer.add('TYPE_ANY', r'any')

        # Literals
        self.lexer.add('INTEGER', r'\d+')
        self.lexer.add('FLOAT', r'\d+\.\d+')
        self.lexer.add('STRING', r'"[^"]*"')
        self.lexer.add('BOOLEAN', r'true|false')
        self.lexer.add('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*')

        # Operators
        self.lexer.add('PLUS', r'\+')
        self.lexer.add('MINUS', r'-')
        self.lexer.add('MULTIPLY', r'\*')
        self.lexer.add('DIVIDE', r'/')
        self.lexer.add('MODULO', r'%')
        self.lexer.add('ASSIGN', r'=')
        self.lexer.add('EQUALS', r'==')
        self.lexer.add('NOT_EQUALS', r'!=')
        self.lexer.add('LESS_THAN', r'<')
        self.lexer.add('GREATER_THAN', r'>')
        self.lexer.add('LESS_EQUALS', r'<=')
        self.lexer.add('GREATER_EQUALS', r'>=')
        self.lexer.add('AND', r'&&')
        self.lexer.add('OR', r'\|\|')
        self.lexer.add('NOT', r'!')
        self.lexer.add('PIPE', r'\|>')
        self.lexer.add('ARROW', r'=>')

        # Delimiters
        self.lexer.add('LPAREN', r'\(')
        self.lexer.add('RPAREN', r'\)')
        self.lexer.add('LBRACE', r'\{')
        self.lexer.add('RBRACE', r'\}')
        self.lexer.add('LBRACKET', r'\[')
        self.lexer.add('RBRACKET', r'\]')
        self.lexer.add('COMMA', r',')
        self.lexer.add('COLON', r':')
        self.lexer.add('SEMICOLON', r';')
        self.lexer.add('DOT', r'\.')

        # Ignore whitespace
        self.lexer.ignore(r'\s+')
        self.lexer.ignore(r'//.*\n')
        self.lexer.ignore(r'/\*[\s\S]*?\*/')

    def get_lexer(self):
        return self.lexer.build() 