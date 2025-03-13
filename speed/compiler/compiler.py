from .lexer import Lexer
from .parser import Parser
from .codegen import CodeGenerator

class Compiler:
    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self.codegen = CodeGenerator()

    def compile(self, source_code):
        # Tokenize the source code
        tokens = self.lexer.get_lexer().lex(source_code)
        
        # Parse the tokens into an AST
        ast = self.parser.get_parser().parse(tokens)
        
        # Generate LLVM IR from the AST
        self.codegen.generate(ast)
        
        # Return the LLVM module
        return self.codegen.module

    def compile_to_file(self, source_code, output_file):
        # Compile the source code
        module = self.compile(source_code)
        
        # Write the LLVM IR to a file
        with open(output_file, 'w') as f:
            f.write(str(module))
        
        return output_file

    def compile_to_object(self, source_code, output_file):
        # Compile the source code
        module = self.compile(source_code)
        
        # TODO: Implement LLVM IR to object file compilation
        # This will require integration with LLVM's native compilation pipeline
        raise NotImplementedError("Object file compilation not yet implemented") 