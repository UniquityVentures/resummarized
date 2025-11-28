import inspect


def test_func():
    pass


def get_module_info(module):
    out = {}
    for item in dir(module):
        val = getattr(module, item)

        if type(val) is type(test_func):
            out[val.__name__] = val

        if type(val) is type(inspect):
            out[val.__name__] = get_module_info(val)

def top_level_module_info(module) -> str:
    module_info = get_module_info(module)

    output_str = ""
    for k, v in module_info.items():
        if type(v) is type(test_func):
            output_str += f"{module.__name__}.{v.__name__} : {inspect.signature(v)}\n"


    
