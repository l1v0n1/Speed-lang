class Node:
    pass

class Program(Node):
    def __init__(self, statements):
        self.statements = statements

class Statement(Node):
    pass

class Expression(Node):
    pass

class Type(Node):
    def __init__(self, name):
        self.name = name

class Parameter(Node):
    def __init__(self, name, type):
        self.name = name
        self.type = type

class FunctionDeclaration(Statement):
    def __init__(self, name, parameters, return_type, body):
        self.name = name
        self.parameters = parameters
        self.return_type = return_type
        self.body = body

class ClassDeclaration(Statement):
    def __init__(self, name, members):
        self.name = name
        self.members = members

class VariableDeclaration(Statement):
    def __init__(self, name, type, initializer):
        self.name = name
        self.type = type
        self.initializer = initializer

class ReturnStatement(Statement):
    def __init__(self, expression):
        self.expression = expression

class IfStatement(Statement):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ForStatement(Statement):
    def __init__(self, initializer, condition, increment, body):
        self.initializer = initializer
        self.condition = condition
        self.increment = increment
        self.body = body

class Literal(Expression):
    def __init__(self, value):
        self.value = value

class BinaryOp(Expression):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class UnaryOp(Expression):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

class Call(Expression):
    def __init__(self, function, arguments):
        self.function = function
        self.arguments = arguments

class Identifier(Expression):
    def __init__(self, name):
        self.name = name

class Assignment(Expression):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class ImportStatement(Statement):
    def __init__(self, imports, module):
        self.imports = imports
        self.module = module

class MemberAccess(Expression):
    def __init__(self, object_name, member_name):
        self.object_name = object_name
        self.member_name = member_name 