from llvmlite import ir

def create_print_function(module):
    # Create print function type
    print_type = ir.FunctionType(ir.VoidType(), [ir.PointerType(ir.IntType(8))])
    
    # Create print function
    print_func = ir.Function(module, print_type, name="print")
    
    # Create entry block
    block = print_func.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)
    
    # Get printf function
    printf_type = ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))], var_arg=True)
    printf = ir.Function(module, printf_type, name="printf")
    
    # Create format string
    format_str = builder.global_string("%s\n")
    
    # Call printf
    builder.call(printf, [format_str, print_func.args[0]])
    
    # Return void
    builder.ret_void()
    
    return print_func

def create_readline_function(module):
    # Create readline function type
    readline_type = ir.FunctionType(ir.PointerType(ir.IntType(8)), [])
    
    # Create readline function
    readline_func = ir.Function(module, readline_type, name="readline")
    
    # Create entry block
    block = readline_func.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)
    
    # Get gets function
    gets_type = ir.FunctionType(ir.PointerType(ir.IntType(8)), [ir.PointerType(ir.IntType(8))])
    gets = ir.Function(module, gets_type, name="gets")
    
    # Allocate buffer
    buffer = builder.alloca(ir.ArrayType(ir.IntType(8), 1024))
    buffer_ptr = builder.gep(buffer, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])
    
    # Call gets
    result = builder.call(gets, [buffer_ptr])
    
    # Return result
    builder.ret(result)
    
    return readline_func

def create_file_open_function(module):
    # Create file_open function type
    file_open_type = ir.FunctionType(
        ir.PointerType(ir.IntType(8)),
        [ir.PointerType(ir.IntType(8)), ir.PointerType(ir.IntType(8))]
    )
    
    # Create file_open function
    file_open_func = ir.Function(module, file_open_type, name="file_open")
    
    # Create entry block
    block = file_open_func.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)
    
    # Get fopen function
    fopen_type = ir.FunctionType(
        ir.PointerType(ir.IntType(8)),
        [ir.PointerType(ir.IntType(8)), ir.PointerType(ir.IntType(8))]
    )
    fopen = ir.Function(module, fopen_type, name="fopen")
    
    # Call fopen
    result = builder.call(fopen, [file_open_func.args[0], file_open_func.args[1]])
    
    # Return result
    builder.ret(result)
    
    return file_open_func

def create_file_close_function(module):
    # Create file_close function type
    file_close_type = ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))])
    
    # Create file_close function
    file_close_func = ir.Function(module, file_close_type, name="file_close")
    
    # Create entry block
    block = file_close_func.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)
    
    # Get fclose function
    fclose_type = ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))])
    fclose = ir.Function(module, fclose_type, name="fclose")
    
    # Call fclose
    result = builder.call(fclose, [file_close_func.args[0]])
    
    # Return result
    builder.ret(result)
    
    return file_close_func

def create_file_read_function(module):
    # Create file_read function type
    file_read_type = ir.FunctionType(
        ir.IntType(32),
        [ir.PointerType(ir.IntType(8)), ir.PointerType(ir.IntType(8)), ir.IntType(32)]
    )
    
    # Create file_read function
    file_read_func = ir.Function(module, file_read_type, name="file_read")
    
    # Create entry block
    block = file_read_func.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)
    
    # Get fread function
    fread_type = ir.FunctionType(
        ir.IntType(32),
        [ir.PointerType(ir.IntType(8)), ir.IntType(32), ir.IntType(32), ir.PointerType(ir.IntType(8))]
    )
    fread = ir.Function(module, fread_type, name="fread")
    
    # Call fread
    result = builder.call(fread, [
        file_read_func.args[1],  # buffer
        ir.Constant(ir.IntType(32), 1),  # size
        file_read_func.args[2],  # count
        file_read_func.args[0]   # file
    ])
    
    # Return result
    builder.ret(result)
    
    return file_read_func

def create_file_write_function(module):
    # Create file_write function type
    file_write_type = ir.FunctionType(
        ir.IntType(32),
        [ir.PointerType(ir.IntType(8)), ir.PointerType(ir.IntType(8)), ir.IntType(32)]
    )
    
    # Create file_write function
    file_write_func = ir.Function(module, file_write_type, name="file_write")
    
    # Create entry block
    block = file_write_func.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)
    
    # Get fwrite function
    fwrite_type = ir.FunctionType(
        ir.IntType(32),
        [ir.PointerType(ir.IntType(8)), ir.IntType(32), ir.IntType(32), ir.PointerType(ir.IntType(8))]
    )
    fwrite = ir.Function(module, fwrite_type, name="fwrite")
    
    # Call fwrite
    result = builder.call(fwrite, [
        file_write_func.args[1],  # buffer
        ir.Constant(ir.IntType(32), 1),  # size
        file_write_func.args[2],  # count
        file_write_func.args[0]   # file
    ])
    
    # Return result
    builder.ret(result)
    
    return file_write_func 