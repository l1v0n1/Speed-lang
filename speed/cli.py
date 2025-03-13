import argparse
import sys
from .compiler.compiler import Compiler

def main():
    parser = argparse.ArgumentParser(description='Speed Programming Language Compiler')
    parser.add_argument('input_file', help='Input Speed source file')
    parser.add_argument('-o', '--output', help='Output file (default: input.ll)')
    parser.add_argument('--object', action='store_true', help='Generate object file instead of LLVM IR')
    parser.add_argument('--version', action='version', version='Speed 0.1.0')
    
    args = parser.parse_args()
    
    # Read input file
    try:
        with open(args.input_file, 'r') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find input file '{args.input_file}'", file=sys.stderr)
        sys.exit(1)
    
    # Determine output file
    if args.output:
        output_file = args.output
    else:
        output_file = args.input_file.rsplit('.', 1)[0] + '.ll'
    
    # Create compiler
    compiler = Compiler()
    
    try:
        if args.object:
            compiler.compile_to_object(source_code, output_file)
        else:
            compiler.compile_to_file(source_code, output_file)
        print(f"Successfully compiled '{args.input_file}' to '{output_file}'")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main() 