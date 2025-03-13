from rply import ParserGenerator
from .ast import *
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Parser:
    def __init__(self):
        logger.debug("Initializing parser")
        self.pg = ParserGenerator(
            # A list of all token names, accepted by the parser.
            ['INTEGER', 'FLOAT', 'STRING', 'BOOLEAN', 'IDENTIFIER',
             'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'MODULO',
             'ASSIGN', 'EQUALS', 'NOT_EQUALS', 'LESS_THAN', 'GREATER_THAN',
             'LESS_EQUALS', 'GREATER_EQUALS', 'AND', 'OR', 'NOT',
             'PIPE', 'ARROW',
             'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
             'COMMA', 'COLON', 'SEMICOLON', 'DOT',
             'FUNCTION', 'CLASS', 'LET', 'CONST', 'IF', 'ELSE', 'WHILE',
             'FOR', 'RETURN', 'IMPORT', 'FROM', 'AS', 'PUBLIC', 'PRIVATE',
             'PROTECTED', 'STATIC', 'ASYNC', 'AWAIT', 'NEW',
             'TYPE_INT', 'TYPE_FLOAT', 'TYPE_STRING', 'TYPE_BOOL',
             'TYPE_VOID', 'TYPE_ANY'],
            precedence=[
                ('left', ['PLUS', 'MINUS']),
                ('left', ['MULTIPLY', 'DIVIDE', 'MODULO']),
                ('left', ['EQUALS', 'NOT_EQUALS', 'LESS_THAN', 'GREATER_THAN', 'LESS_EQUALS', 'GREATER_EQUALS']),
                ('left', ['AND', 'OR']),
            ]
        )
        logger.debug("Setting up grammar")
        self._setup_grammar()

    def _setup_grammar(self):
        logger.debug("Setting up grammar rules")
        @self.pg.production('program : statements')
        def program(p):
            logger.debug("Parsing program")
            return Program(p[0])

        @self.pg.production('statements : statement')
        @self.pg.production('statements : statements statement')
        def statements(p):
            logger.debug(f"Parsing statements, length: {len(p)}")
            if len(p) == 1:
                return [p[0]]
            return p[0] + [p[1]]

        @self.pg.production('statement : import_statement')
        @self.pg.production('statement : function_declaration')
        @self.pg.production('statement : class_declaration')
        @self.pg.production('statement : variable_declaration')
        @self.pg.production('statement : return_statement')
        @self.pg.production('statement : expression')
        def statement(p):
            logger.debug(f"Parsing statement of type: {type(p[0]).__name__}")
            return p[0]

        @self.pg.production('expression : IDENTIFIER')
        @self.pg.production('expression : literal')
        @self.pg.production('expression : binary_operation')
        @self.pg.production('expression : unary_operation')
        @self.pg.production('expression : function_call')
        @self.pg.production('expression : member_access')
        @self.pg.production('expression : new_expression')
        @self.pg.production('expression : LPAREN expression RPAREN')
        def expression(p):
            logger.debug(f"Parsing expression: {[token.gettokentype() if hasattr(token, 'gettokentype') else type(token) for token in p]}")
            if len(p) == 3:  # Parenthesized expression
                return p[1]
            return p[0]

        @self.pg.production('literal : INTEGER')
        @self.pg.production('literal : FLOAT')
        @self.pg.production('literal : STRING')
        @self.pg.production('literal : BOOLEAN')
        def literal(p):
            return Literal(p[0].value)

        @self.pg.production('binary_operation : expression PLUS expression')
        @self.pg.production('binary_operation : expression MINUS expression')
        @self.pg.production('binary_operation : expression MULTIPLY expression')
        @self.pg.production('binary_operation : expression DIVIDE expression')
        @self.pg.production('binary_operation : expression EQUALS expression')
        @self.pg.production('binary_operation : expression NOT_EQUALS expression')
        @self.pg.production('binary_operation : expression LESS_THAN expression')
        @self.pg.production('binary_operation : expression GREATER_THAN expression')
        @self.pg.production('binary_operation : expression LESS_EQUALS expression')
        @self.pg.production('binary_operation : expression GREATER_EQUALS expression')
        def binary_operation(p):
            logger.debug(f"Parsing binary operation: {p[1].gettokentype()} with operands {type(p[0])} and {type(p[2])}")
            op_map = {
                'PLUS': '+',
                'MINUS': '-',
                'MULTIPLY': '*',
                'DIVIDE': '/',
                'EQUALS': '==',
                'NOT_EQUALS': '!=',
                'LESS_THAN': '<',
                'GREATER_THAN': '>',
                'LESS_EQUALS': '<=',
                'GREATER_EQUALS': '>='
            }
            return BinaryOp(op_map[p[1].gettokentype()], p[0], p[2])

        @self.pg.production('unary_operation : NOT expression')
        def unary_operation(p):
            return UnaryOp(p[0].gettokentype(), p[1])

        @self.pg.production('function_call : IDENTIFIER LPAREN arguments RPAREN')
        @self.pg.production('function_call : member_access LPAREN arguments RPAREN')
        def function_call(p):
            if isinstance(p[0], MemberAccess):
                return Call(p[0], p[2])
            else:
                return Call(p[0].getstr(), p[2])

        @self.pg.production('arguments : expression_list')
        @self.pg.production('arguments : ')
        def arguments(p):
            return p[0] if p else []

        @self.pg.production('expression_list : expression')
        @self.pg.production('expression_list : expression_list COMMA expression')
        def expression_list(p):
            if len(p) == 1:
                return [p[0]]
            else:
                p[0].append(p[2])
                return p[0]

        @self.pg.production('member_access : expression DOT IDENTIFIER')
        def member_access(p):
            return MemberAccess(p[0], p[2].getstr())

        @self.pg.production('new_expression : NEW IDENTIFIER LPAREN arguments RPAREN')
        def new_expression(p):
            return NewExpression(p[1].getstr(), p[3])

        @self.pg.production('variable_declaration : LET IDENTIFIER COLON type ASSIGN expression SEMICOLON')
        @self.pg.production('variable_declaration : LET IDENTIFIER ASSIGN expression SEMICOLON')
        def variable_declaration(p):
            if len(p) == 7:  # With type annotation
                return VariableDeclaration(p[1].getstr(), p[3], p[5])
            else:  # Type inference
                return VariableDeclaration(p[1].getstr(), None, p[3])

        @self.pg.production('function_declaration : FUNCTION IDENTIFIER LPAREN parameters RPAREN COLON type LBRACE statements RBRACE')
        def function_declaration(p):
            return FunctionDeclaration(p[1].getstr(), p[3], p[6], p[8])

        @self.pg.production('parameters : parameter_list')
        @self.pg.production('parameters : ')
        def parameters(p):
            return p[0] if p else []

        @self.pg.production('parameter_list : parameter')
        @self.pg.production('parameter_list : parameter_list COMMA parameter')
        def parameter_list(p):
            if len(p) == 1:
                return [p[0]]
            else:
                p[0].append(p[2])
                return p[0]

        @self.pg.production('parameter : IDENTIFIER COLON type')
        def parameter(p):
            return Parameter(p[0].getstr(), p[2])

        @self.pg.production('type : TYPE_INT')
        @self.pg.production('type : TYPE_FLOAT')
        @self.pg.production('type : TYPE_STRING')
        @self.pg.production('type : TYPE_BOOL')
        @self.pg.production('type : TYPE_VOID')
        @self.pg.production('type : TYPE_ANY')
        @self.pg.production('type : IDENTIFIER')
        def type(p):
            logger.debug(f"Parsing type: {p[0].gettokentype()}")
            return Type(p[0].getstr())

        @self.pg.production('if_statement : IF LPAREN expression RPAREN LBRACE statements RBRACE')
        @self.pg.production('if_statement : IF LPAREN expression RPAREN LBRACE statements RBRACE ELSE LBRACE statements RBRACE')
        def if_statement(p):
            if len(p) == 7:
                return IfStatement(p[2], p[5])
            return IfStatement(p[2], p[5], p[9])

        @self.pg.production('while_statement : WHILE LPAREN expression RPAREN LBRACE statements RBRACE')
        def while_statement(p):
            return WhileStatement(p[2], p[5])

        @self.pg.production('for_statement : FOR LPAREN variable_declaration expression SEMICOLON expression RPAREN LBRACE statements RBRACE')
        def for_statement(p):
            return ForStatement(p[2], p[3], p[5], p[8])

        @self.pg.production('return_statement : RETURN expression SEMICOLON')
        def return_statement(p):
            return ReturnStatement(p[1])

        @self.pg.production('class_declaration : CLASS IDENTIFIER LBRACE class_members RBRACE')
        def class_declaration(p):
            return ClassDeclaration(p[1].getstr(), p[3])

        @self.pg.production('class_members : class_member')
        @self.pg.production('class_members : class_members class_member')
        @self.pg.production('class_members : ')
        def class_members(p):
            if len(p) == 0:
                return []
            elif len(p) == 1:
                return [p[0]]
            else:
                p[0].append(p[1])
                return p[0]

        @self.pg.production('class_member : IDENTIFIER COLON type SEMICOLON')
        @self.pg.production('class_member : function_declaration')
        def class_member(p):
            if len(p) == 4:  # Field declaration
                return VariableDeclaration(p[0].getstr(), p[2], None)
            else:  # Method declaration
                return p[0]

        @self.pg.production('import_statement : IMPORT LBRACE import_items RBRACE FROM STRING')
        def import_statement(p):
            logger.debug(f"Parsing import statement with items: {p[2]}")
            return ImportStatement(p[2], p[5].getstr().strip('"'))

        @self.pg.production('import_items : IDENTIFIER')
        @self.pg.production('import_items : import_items COMMA IDENTIFIER')
        def import_items(p):
            if len(p) == 1:
                return [p[0].getstr()]
            return p[0] + [p[2].getstr()]

        @self.pg.error
        def error_handle(token):
            logger.error(f"Parser error: Unexpected token {token.gettokentype()} with value {token.getstr()}")
            raise ValueError(f"Unexpected token {token.gettokentype()} with value {token.getstr()}")

    def get_parser(self):
        logger.debug("Building parser")
        return self.pg.build() 