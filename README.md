# Speed Programming Language

Speed is a universal programming language that combines the simplicity and readability of Python and JavaScript with performance and advanced features on par with C++. It is designed for rapid development while delivering a performance uplift of at least 200% over popular scripting languages.

## Features

- **Familiar yet Unique Syntax**: Inspired by Python and JavaScript, but with unique constructs for clarity and efficiency
- **High Performance**: Outperforming Python/JavaScript by at least 200% through advanced compiler optimizations
- **Multi-Target Compilation**: Support for desktop/server (LLVM IR), browsers (WebAssembly), and development (JIT)
- **Gradual Type System**: Dynamic typing for prototyping with optional static types for performance
- **Modern Concurrency Model**: Built-in support for parallel and concurrent programming
- **Rich Standard Library**: Comprehensive set of built-in modules for common tasks
- **Memory Safety**: Automatic Reference Counting (ARC) with optional arena allocators

## Installation

```bash
# Clone the repository
git clone https://github.com/speed-lang/speed.git
cd speed

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Quick Start

1. Create a new Speed file (e.g., `hello.speed`):

```speed
fn main(): void {
    print("Hello, World!");
}
```

2. Compile and run:

```bash
# Compile to LLVM IR
speed hello.speed -o hello.ll

# Compile to native executable
speed hello.speed -o hello --object

# Run the program
./hello
```

## Language Features

### Basic Syntax

```speed
// Function definition
fn add(a: int, b: int): int {
    return a + b;
}

// Variable declaration
let x = 42;
const PI = 3.14159;

// Control flow
if x > 0 {
    print("Positive");
} else {
    print("Negative");
}

// Loops
while x > 0 {
    print(x);
    x = x - 1;
}

for let i = 0; i < 10; i = i + 1 {
    print(i);
}
```

### Classes and Objects

```speed
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

let p1 = new Point(0.0, 0.0);
let p2 = new Point(3.0, 4.0);
print(p1.distance(p2));
```

### Standard Library

```speed
import { print } from "io";
import { sin, cos } from "math";
import { length, concat } from "string";

fn main(): void {
    // IO operations
    print("Hello, World!");
    
    // Math operations
    let x = 3.14;
    print(sin(x));
    print(cos(x));
    
    // String operations
    let str1 = "Hello";
    let str2 = "World";
    print(concat(str1, str2));
}
```

### Concurrency

```speed
async fn fetch_data(url: string): string {
    let response = await http.get(url);
    return response.text();
}

fn main(): void {
    let urls = ["http://api1.com", "http://api2.com"];
    let results = await Promise.all(urls.map(url => fetch_data(url)));
    print(results);
}
```

## Development

### Building from Source

```bash
# Clone the repository
git clone https://github.com/speed-lang/speed.git
cd speed

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linter
black .
mypy .
```

### Project Structure

```
speed/
├── compiler/           # Compiler implementation
│   ├── lexer.py       # Tokenizer
│   ├── parser.py      # Parser
│   ├── ast.py         # Abstract Syntax Tree
│   └── codegen.py     # LLVM IR generator
├── runtime/           # Runtime implementation
├── stdlib/           # Standard library
│   ├── io.py         # Input/Output operations
│   ├── math.py       # Mathematical functions
│   └── string.py     # String operations
└── tests/            # Test suite
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- LLVM Project for the compiler infrastructure
- Python and JavaScript communities for inspiration
- All contributors to the Speed project
