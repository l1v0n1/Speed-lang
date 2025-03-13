from llvmlite import ir
from .ast import *
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CodeGenerator:
    def __init__(self, module_name="speed_module"):
        logger.debug(f"Initializing code generator with module name: {module_name}")
        self.module = ir.Module(name=module_name)
        self.builder = None
        self.function = None
        self.variables = {}  # Store variable allocations
        self.strings = []  # Store string constants
        
        # Define types
        self.types = {
            'int': ir.IntType(32),
            'float': ir.DoubleType(),
            'bool': ir.IntType(1),
            'void': ir.VoidType(),
            'string': ir.PointerType(ir.IntType(8))
        }
        logger.debug("Types defined")

    def get_llvm_type(self, type_node):
        if isinstance(type_node, str):
            type_name = type_node
        else:
            type_name = type_node.name
        
        if type_name in self.types:
            return self.types[type_name]
        else:
            # For user-defined types (classes), create a struct type
            struct_type = ir.global_context.get_identified_type(type_name)
            if not struct_type.is_literal:
                # Define the struct fields if not already defined
                field_types = []  # This should be populated based on class definition
                struct_type.set_body(*field_types)
            return struct_type

    def get_llvm_type_from_value(self, value):
        if isinstance(value, int):
            return ir.IntType(32)
        elif isinstance(value, float):
            return ir.DoubleType()
        elif isinstance(value, bool):
            return ir.IntType(1)
        elif isinstance(value, str):
            return ir.ArrayType(ir.IntType(8), len(value) + 1)
        else:
            raise ValueError(f"Unsupported literal type: {type(value)}")

    def generate(self, node):
        logger.debug(f"Generating code for node type: {type(node)}")
        if isinstance(node, Program):
            logger.debug("Generating program")
            for stmt in node.statements:
                self.generate(stmt)
            return self.module
        elif isinstance(node, FunctionDeclaration):
            logger.debug(f"Generating function: {node.name}")
            return self.generate_function(node)
        elif isinstance(node, ReturnStatement):
            logger.debug("Generating return statement")
            return self.generate_return(node)
        elif isinstance(node, VariableDeclaration):
            logger.debug(f"Generating variable declaration: {node.name}")
            return self.generate_variable_declaration(node)
        elif isinstance(node, ClassDeclaration):
            logger.debug(f"Generating class declaration: {node.name}")
            return self.generate_class_declaration(node)
        elif isinstance(node, ImportStatement):
            logger.debug(f"Generating import statement for module: {node.module}")
            return self.generate_import(node)
        elif isinstance(node, (Literal, Identifier, BinaryOp, UnaryOp, Call, MemberAccess)):
            logger.debug(f"Generating expression: {type(node)}")
            return self.generate_expression(node)
        else:
            logger.error(f"Unknown node type: {type(node)}")
            raise ValueError(f"Unknown node type: {type(node)}")

    def generate_statements(self, statements):
        result = None
        for stmt in statements:
            result = self.generate(stmt)
        return result

    def generate_function(self, node):
        logger.debug(f"Generating function {node.name} with {len(node.parameters)} parameters")
        # Get function parameters
        param_types = [self.get_llvm_type(param.type) for param in node.parameters]
        return_type = self.get_llvm_type(node.return_type)
        
        # Create function type
        fnty = ir.FunctionType(return_type, param_types)
        
        # Create function without quotes in name
        func = ir.Function(self.module, fnty, node.name.strip('"'))
        
        # Create entry block
        block = func.append_basic_block('entry')
        self.builder = ir.IRBuilder(block)
        
        # Store parameters in local variables
        for i, param in enumerate(node.parameters):
            logger.debug(f"Processing parameter {param.name} of type {param.type.name}")
            # Create alloca without quotes in name
            alloca = self.builder.alloca(param_types[i], name=param.name.strip('"'))
            self.builder.store(func.args[i], alloca)
            self.variables[param.name] = alloca
        
        # Generate function body
        logger.debug("Generating function body")
        self.generate_statements(node.body)
        
        # Ensure the function returns a value if needed
        if not block.is_terminated:
            if return_type == ir.VoidType():
                self.builder.ret_void()
            else:
                self.builder.ret(ir.Constant(return_type, 0))
        
        return func

    def generate_return(self, node):
        value = self.generate(node.expression)
        return self.builder.ret(value)

    def generate_expression(self, node):
        logger.debug(f"Generating expression for node type: {type(node)}")
        # Convert tokens to AST nodes
        if hasattr(node, 'gettokentype'):
            logger.debug(f"Converting token {node.gettokentype()} to AST node")
            if node.gettokentype() == 'IDENTIFIER':
                node = Identifier(node.getstr())
            elif node.gettokentype() in ['INTEGER', 'FLOAT', 'STRING', 'BOOLEAN']:
                node = Literal(node.value)

        if isinstance(node, Literal):
            logger.debug(f"Generating literal with value: {node.value} of type {type(node.value)}")
            if isinstance(node.value, str):
                # Create string constant without quotes in name
                string_val = node.value.strip('"')
                string_const = ir.GlobalVariable(self.module, ir.ArrayType(ir.IntType(8), len(string_val) + 1), 
                                              name=f"str_{len(self.strings)}")
                string_const.global_constant = True
                string_const.initializer = ir.Constant(ir.ArrayType(ir.IntType(8), len(string_val) + 1), 
                                                     bytearray(string_val.encode('utf8') + b'\00'))
                self.strings.append(string_const)
                return string_const
            else:
                return ir.Constant(self.get_llvm_type_from_value(node.value), node.value)
        elif isinstance(node, Identifier):
            logger.debug(f"Generating identifier reference: {node.name}")
            # Load value from local variable
            if node.name not in self.variables:
                raise ValueError(f"Undefined variable: {node.name}")
            return self.builder.load(self.variables[node.name])
        elif isinstance(node, BinaryOp):
            logger.debug(f"Generating binary operation: {node.op}")
            left = self.generate_expression(node.left)
            right = self.generate_expression(node.right)
            logger.debug(f"Binary operation operands - left: {type(left)}, right: {type(right)}")
            
            if node.op in ['+', '-', '*', '/']:
                if isinstance(left.type, ir.IntType):
                    if node.op == '+':
                        return self.builder.add(left, right)
                    elif node.op == '-':
                        return self.builder.sub(left, right)
                    elif node.op == '*':
                        return self.builder.mul(left, right)
                    elif node.op == '/':
                        return self.builder.sdiv(left, right)
                else:
                    if node.op == '+':
                        return self.builder.fadd(left, right)
                    elif node.op == '-':
                        return self.builder.fsub(left, right)
                    elif node.op == '*':
                        return self.builder.fmul(left, right)
                    elif node.op == '/':
                        return self.builder.fdiv(left, right)
            elif node.op in ['==', '!=', '<', '>', '<=', '>=']:
                if isinstance(left.type, ir.IntType):
                    return self.builder.icmp_signed(node.op, left, right)
                else:
                    return self.builder.fcmp_ordered(node.op, left, right)
            else:
                logger.error(f"Unknown binary operator: {node.op}")
                raise ValueError(f"Unknown binary operator: {node.op}")
        elif isinstance(node, UnaryOp):
            operand = self.generate_expression(node.operand)
            if node.op == 'NOT':
                return self.builder.not_(operand)
            else:
                raise ValueError(f"Unknown unary operator: {node.op}")
        elif isinstance(node, Call):
            func = self.module.get_global(node.function.strip('"'))
            if func is None:
                raise ValueError(f"Function {node.function} not found")
            args = [self.generate_expression(arg) for arg in node.arguments]
            return self.builder.call(func, args)
        elif isinstance(node, MemberAccess):
            # Get the object
            obj = self.variables.get(node.object_name)
            if obj is None:
                raise ValueError(f"Undefined object: {node.object_name}")
            
            # Get the member index
            struct_type = obj.type.pointee
            try:
                idx = [name for name, _ in struct_type.elements].index(node.member_name)
            except ValueError:
                raise ValueError(f"Member not found: {node.member_name}")
            
            # Get pointer to member
            zero = ir.Constant(ir.IntType(32), 0)
            indices = [zero, ir.Constant(ir.IntType(32), idx)]
            ptr = self.builder.gep(obj, indices, inbounds=True)
            
            return self.builder.load(ptr)
        else:
            logger.error(f"Unknown expression type: {type(node)}")
            raise ValueError(f"Unknown expression type: {type(node)}")

    def generate_import(self, node):
        # For now, just declare the imported functions
        for imp in node.imports:
            if node.module == "io":
                if imp == "print":
                    fnty = ir.FunctionType(self.types['void'], [self.types['string']])
                    ir.Function(self.module, fnty, name="print")
            elif node.module == "math":
                if imp in ["sin", "cos"]:
                    fnty = ir.FunctionType(self.types['float'], [self.types['float']])
                    ir.Function(self.module, fnty, name=f"math_{imp}")
            elif node.module == "string":
                if imp == "length":
                    fnty = ir.FunctionType(self.types['int'], [self.types['string']])
                    ir.Function(self.module, fnty, name="string_length")
                elif imp in ["concat", "split", "join"]:
                    fnty = ir.FunctionType(self.types['string'], [self.types['string'], self.types['string']])
                    ir.Function(self.module, fnty, name=f"string_{imp}")

    def generate_variable_declaration(self, node):
        logger.debug(f"Generating variable declaration: {node.name}")
        if node.initializer is None:
            # For class fields without initializers
            return None
        value = self.generate_expression(node.initializer)
        var_type = self.get_llvm_type(node.type.name) if node.type else value.type
        var = self.builder.alloca(var_type, name=node.name)
        self.builder.store(value, var)
        self.variables[node.name] = var
        return var

    def generate_class_declaration(self, node):
        # Create struct type for class
        struct_type = ir.global_context.get_identified_type(f"struct.{node.name}")
        
        # Collect field types
        field_types = []
        field_names = []
        for member in node.members:
            if isinstance(member, VariableDeclaration):
                field_types.append(self.types[member.type.name])
                field_names.append(member.name)
        
        # Set struct body with named elements
        struct_type.set_body(*field_types, packed=False)
        struct_type.elements = list(zip(field_names, field_types))
        
        # Generate methods
        for member in node.members:
            if isinstance(member, FunctionDeclaration):
                self.generate(member)
        
        return struct_type 