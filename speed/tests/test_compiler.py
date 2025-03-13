import pytest
from speed.compiler.compiler import Compiler
from speed.compiler.lexer import Lexer
from speed.compiler.parser import Parser
from speed.compiler.codegen import CodeGenerator
from speed.compiler.ast import (
    FunctionDeclaration,
    Program,
    Parameter,
    Type,
    Literal,
    BinaryOp,
    Call,
    ReturnStatement,
    VariableDeclaration,
    ClassDeclaration
)

def test_lexer():
    lexer = Lexer()
    tokens = list(lexer.get_lexer().lex("""
        fn add(a: int, b: int): int {
            return a + b;
        }
    """))
    
    # Verify tokens
    assert len(tokens) > 0
    assert tokens[0].gettokentype() == 'FUNCTION'
    assert tokens[1].gettokentype() == 'IDENTIFIER'
    assert tokens[1].getstr() == 'add'

def test_parser():
    lexer = Lexer()
    parser = Parser()
    tokens = lexer.get_lexer().lex("""
        fn add(a: int, b: int): int {
            return a + b;
        }
    """)
    ast = parser.get_parser().parse(tokens)
    
    # Verify AST
    assert ast is not None
    assert len(ast.statements) == 1
    assert isinstance(ast.statements[0], FunctionDeclaration)
    assert ast.statements[0].name == 'add'
    assert len(ast.statements[0].parameters) == 2
    assert ast.statements[0].return_type.name == 'int'

def test_codegen():
    compiler = Compiler()
    source_code = """
        fn add(a: int, b: int): int {
            return a + b;
        }
    """
    module = compiler.compile(source_code)
    
    # Verify LLVM IR
    ir_str = str(module)
    assert 'define i32 @add(i32 %a, i32 %b)' in ir_str
    assert 'ret i32' in ir_str

def test_compiler_integration():
    compiler = Compiler()
    source_code = """
        fn fibonacci(n: int): int {
            if n <= 1 {
                return n;
            }
            return fibonacci(n - 1) + fibonacci(n - 2);
        }
    """
    module = compiler.compile(source_code)
    
    # Verify LLVM IR
    ir_str = str(module)
    assert 'define i32 @fibonacci(i32 %n)' in ir_str
    assert 'icmp sle i32' in ir_str  # Less than or equal comparison
    assert 'call i32 @fibonacci' in ir_str  # Recursive call

def test_standard_library():
    compiler = Compiler()
    source_code = """
        import { print } from "io";
        import { sin, cos } from "math";
        import { length, concat } from "string";
        
        fn main(): void {
            let x = 3.14;
            print(sin(x));
            print(cos(x));
            
            let str1 = "Hello";
            let str2 = "World";
            print(concat(str1, str2));
        }
    """
    module = compiler.compile(source_code)
    
    # Verify LLVM IR
    ir_str = str(module)
    assert 'declare void @print' in ir_str
    assert 'declare double @math_sin' in ir_str
    assert 'declare double @math_cos' in ir_str
    assert 'declare i32 @string_length' in ir_str
    assert 'declare i8* @string_concat' in ir_str

def test_error_handling():
    compiler = Compiler()
    
    # Test syntax error
    with pytest.raises(ValueError):
        compiler.compile("""
            fn add(a: int, b: int): int {
                return a + b
            }
        """)
    
    # Test type error
    with pytest.raises(ValueError):
        compiler.compile("""
            fn add(a: int, b: string): int {
                return a + b;
            }
        """)

def test_complex_program():
    compiler = Compiler()
    source_code = """
        import { print } from "io";
        import { random } from "math";
        import { length, split, join } from "string";
        
        class Point {
            x: float;
            y: float;
            
            fn init(x: float, y: float) {
                this.x = x;
                this.y = y;
            }
            
            fn distance(other: Point): float {
                let dx = this.x - other.x;
                let dy = this.y - other.y;
                return sqrt(dx * dx + dy * dy);
            }
        }
        
        fn main(): void {
            let p1 = new Point(0.0, 0.0);
            let p2 = new Point(3.0, 4.0);
            print(p1.distance(p2));
            
            let text = "Hello, World!";
            let parts = split(text, ",");
            let result = join(parts, " ");
            print(result);
        }
    """
    module = compiler.compile(source_code)
    
    # Verify LLVM IR
    ir_str = str(module)
    assert '%struct.Point' in ir_str
    assert 'define double @Point_distance' in ir_str
    assert 'call i8* @string_split' in ir_str
    assert 'call i8* @string_join' in ir_str 