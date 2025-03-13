from llvmlite import ir

def create_math_functions(module):
    # Create math function types
    math_types = {
        'sin': ir.FunctionType(ir.FloatType(), [ir.FloatType()]),
        'cos': ir.FunctionType(ir.FloatType(), [ir.FloatType()]),
        'tan': ir.FunctionType(ir.FloatType(), [ir.FloatType()]),
        'sqrt': ir.FunctionType(ir.FloatType(), [ir.FloatType()]),
        'pow': ir.FunctionType(ir.FloatType(), [ir.FloatType(), ir.FloatType()]),
        'abs': ir.FunctionType(ir.FloatType(), [ir.FloatType()]),
        'floor': ir.FunctionType(ir.FloatType(), [ir.FloatType()]),
        'ceil': ir.FunctionType(ir.FloatType(), [ir.FloatType()]),
        'round': ir.FunctionType(ir.FloatType(), [ir.FloatType()]),
        'min': ir.FunctionType(ir.FloatType(), [ir.FloatType(), ir.FloatType()]),
        'max': ir.FunctionType(ir.FloatType(), [ir.FloatType(), ir.FloatType()]),
        'exp': ir.FunctionType(ir.FloatType(), [ir.FloatType()]),
        'log': ir.FunctionType(ir.FloatType(), [ir.FloatType()]),
        'log10': ir.FunctionType(ir.FloatType(), [ir.FloatType()]),
        'pi': ir.FloatType(),
        'e': ir.FloatType(),
    }
    
    # Create math functions
    math_funcs = {}
    
    for name, func_type in math_types.items():
        if isinstance(func_type, ir.FunctionType):
            # Create function
            func = ir.Function(module, func_type, name=f"math_{name}")
            
            # Create entry block
            block = func.append_basic_block(name="entry")
            builder = ir.IRBuilder(block)
            
            # Get corresponding C math function
            c_func_type = func_type
            c_func = ir.Function(module, c_func_type, name=name)
            
            # Call C math function
            result = builder.call(c_func, func.args)
            
            # Return result
            builder.ret(result)
            
            math_funcs[name] = func
        else:
            # Create constant
            if name == 'pi':
                value = 3.14159265358979323846
            else:  # e
                value = 2.71828182845904523536
            const = ir.GlobalVariable(module, func_type, name=f"math_{name}")
            const.global_constant = True
            const.initializer = ir.Constant(func_type, value)
            math_funcs[name] = const
    
    return math_funcs

def create_random_functions(module):
    # Create random function types
    random_types = {
        'random': ir.FunctionType(ir.FloatType(), []),
        'random_int': ir.FunctionType(ir.IntType(32), [ir.IntType(32), ir.IntType(32)]),
        'random_float': ir.FunctionType(ir.FloatType(), [ir.FloatType(), ir.FloatType()]),
        'seed': ir.FunctionType(ir.VoidType(), [ir.IntType(32)]),
    }
    
    # Create random functions
    random_funcs = {}
    
    for name, func_type in random_types.items():
        # Create function
        func = ir.Function(module, func_type, name=f"random_{name}")
        
        # Create entry block
        block = func.append_basic_block(name="entry")
        builder = ir.IRBuilder(block)
        
        if name == 'random':
            # Get rand function
            rand_type = ir.FunctionType(ir.IntType(32), [])
            rand = ir.Function(module, rand_type, name="rand")
            
            # Call rand and convert to float
            rand_result = builder.call(rand, [])
            float_result = builder.sitofp(rand_result, ir.FloatType())
            result = builder.fdiv(float_result, ir.Constant(ir.FloatType(), 32767.0))
            
            builder.ret(result)
            
        elif name == 'random_int':
            # Get rand function
            rand_type = ir.FunctionType(ir.IntType(32), [])
            rand = ir.Function(module, rand_type, name="rand")
            
            # Calculate range
            range_val = builder.sub(func.args[1], func.args[0])
            range_val = builder.add(range_val, ir.Constant(ir.IntType(32), 1))
            
            # Generate random number in range
            rand_result = builder.call(rand, [])
            result = builder.srem(rand_result, range_val)
            result = builder.add(result, func.args[0])
            
            builder.ret(result)
            
        elif name == 'random_float':
            # Get rand function
            rand_type = ir.FunctionType(ir.IntType(32), [])
            rand = ir.Function(module, rand_type, name="rand")
            
            # Calculate range
            range_val = builder.fsub(func.args[1], func.args[0])
            
            # Generate random number in range
            rand_result = builder.call(rand, [])
            float_result = builder.sitofp(rand_result, ir.FloatType())
            normalized = builder.fdiv(float_result, ir.Constant(ir.FloatType(), 32767.0))
            result = builder.fmul(normalized, range_val)
            result = builder.fadd(result, func.args[0])
            
            builder.ret(result)
            
        elif name == 'seed':
            # Get srand function
            srand_type = ir.FunctionType(ir.VoidType(), [ir.IntType(32)])
            srand = ir.Function(module, srand_type, name="srand")
            
            # Call srand
            builder.call(srand, [func.args[0]])
            builder.ret_void()
        
        random_funcs[name] = func
    
    return random_funcs 