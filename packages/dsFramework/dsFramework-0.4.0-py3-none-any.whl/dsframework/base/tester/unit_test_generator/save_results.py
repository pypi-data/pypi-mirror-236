import base64
import inspect
import json
import dill
import sys
from os.path import realpath, commonpath


def new_inputs_outputs_decorator(cls, *args, **kwargs):
    attributes = dir(cls)
    x = object.__new__(cls)

    cls_functions = [getattr(cls, attr) for attr in attributes if inspect.isfunction(getattr(cls, attr))]

    for func in cls_functions:
        decorated_func = inputs_outputs_function_decorator(func)
        setattr(cls, func.__name__, decorated_func)

    return x


def inputs_outputs_function_decorator(func):
    def wrapper(*args, **kwargs):

        if not in_venv(func):
            signature = inspect.signature(func)

            bound_args = signature.bind(*args, **kwargs)
            bound_args.apply_defaults()
            bound_args.arguments.pop('self', None)

            import_statements = []
            if len(bound_args.arguments) > 0:

                for inst_name, param in bound_args.arguments.items():
                    if hasattr(param, '__module__'):
                        module = param.__module__
                        name = type(param).__name__
                        import_statements.append(f'from {module} import {name}')

            serialized_input_args = dill.dumps(bound_args.arguments)
            serialized_input_base64 = base64.b64encode(serialized_input_args).decode('utf-8')

            result = func(*args, **kwargs)

            serialized_output = dill.dumps(result)
            serialized_output_base64 = base64.b64encode(serialized_output).decode('utf-8')

            class_name = func.__qualname__.rsplit('.', 1)[0]
            function_name = func.__name__

            module = inspect.getmodule(func)
            module_name = module.__file__ if module else None

            data = {
                'module': module_name,
                'class': class_name,
                'function': function_name,
                'input': serialized_input_base64,
                'output': serialized_output_base64,
                'import_statements': ",".join(import_statements)
            }

            with open('inputs_outputs_log.json', 'a') as file:

                json.dump(data, file)
                file.write('\n')

            return result
        else:
            return func(*args, **kwargs)

    return wrapper


def in_venv(func):

    func_module = inspect.getmodule(func)
    if func_module:
        module_path = realpath(func_module.__file__)
        venv_path = realpath(sys.prefix)
        common_path = commonpath([module_path, venv_path])
        return common_path == venv_path
    return False
