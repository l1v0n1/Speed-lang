"""
Speed Programming Language
A universal programming language combining Python's simplicity with C++'s performance
"""

from .compiler.compiler import Compiler
from .compiler.lexer import Lexer
from .compiler.parser import Parser
from .compiler.codegen import CodeGenerator

__version__ = "0.1.0"
__all__ = ["Compiler", "Lexer", "Parser", "CodeGenerator"] 