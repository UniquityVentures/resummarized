import inspect


def test_func():
    pass


def get_module_info(module):
    out = {}
    for item in dir(module):
        val = getattr(module, item)

        if hasattr(val, "__name__"):
            out[val.__name__] = val
        else:
            out[f"{val}"] = val
    return out


def top_level_module_info(module, depth=2) -> str:
    if depth  < 1:
        return "\n"
    module_info = get_module_info(module)

    output_str = ""
    for k, v in module_info.items():
        output_str += f"{type(v)} "
        if type(v) is type(test_func):
            output_str += f"{module.__name__}.{k} : {inspect.signature(v)}\n"
        elif type(v) is type(inspect):
            output_str += f"{k}\n{top_level_module_info(v, depth=depth-1)}\n\n"
        else:
            output_str += f"{k} : {v}\n"
    
    return output_str
