import base64
import json
import dill
import os
import importlib.util
import re

from dsframework.base.tester.unit_test_generator.read_files import create_json_generator
from dsframework.base.tester.unit_test_generator.json_encoder import SanitizerEncoder


class GenerateUnitTests:

    header = ['import pytest']

    def __init__(self, unit_path):
        self.unit_path = unit_path

    def append_imports(self, list_imports: []):
        self.header.extend(list_imports)

    def create_file_header(self):

        with open(self.unit_path + '', 'w') as file:
            file.writelines(self.header)

    def build_dictionary_from_json(self, json_path):
        json_gen = create_json_generator(json_path)

        data_dict = {}
        for json_data in json_gen:

            module_path = json_data['module']
            class_name = json_data['class']
            import_statements = json_data['import_statements']

            import_str_key, unit_file_name = self.path_to_import(module_path)
            if import_str_key:
                import_str_key = f'from {import_str_key} import {class_name}'
            else:
                continue

            serialized_input = base64.b64decode(json_data["input"])
            serialized_output = base64.b64decode(json_data["output"])
            input_data = dill.loads(serialized_input)
            output_data = dill.loads(serialized_output)

            function_info = {
                "unit_filename": unit_file_name,
                "class_name": class_name,
                "function": json_data["function"],
                "input": input_data,
                "output": output_data,
                "import_statements": import_statements
            }

            if import_str_key not in data_dict:
                data_dict[import_str_key] = [function_info]
            else:
                data_dict[import_str_key].append(function_info)

        return data_dict

    def path_to_import(self, filepath):
        filename = os.path.basename(filepath)
        module_name, _ = os.path.splitext(filename)
        module_path = os.path.dirname(filepath)

        module_parts = []
        while module_path != '/' and module_path != '':
            module_path, folder = os.path.split(module_path)
            module_parts.insert(0, folder)

        module_parts.append(module_name)

        package_location = self.get_package_location(module_parts)
        return package_location, module_name

    def get_package_location(self, module_parts):
        package_name = None
        spec = None

        for i in range(len(module_parts) - 1, -1, -1):
            partial_module_parts = module_parts[i:]
            package_name = '.'.join(partial_module_parts)

            try:
                spec = importlib.util.find_spec(package_name)
            except ModuleNotFoundError as E:
                pass

            if spec is not None:
                break

        return package_name

    def camel_to_underscore(self, string):

        converted = re.sub(r'([A-Z])', r'_\1', string)

        converted = converted.lower().lstrip('_')
        return converted

    def create_unit_test_files(self, unit_data_dict):

        for key_import, value_funcs in unit_data_dict.items():

            file_name = 'unit_test_' + value_funcs[0]['unit_filename'] + '.py'
            class_name = value_funcs[0]['class_name']
            init_input_params = self.create_param_str_line(self.get_init_params(value_funcs))
            underscore_class_name = self.camel_to_underscore(class_name)
            import_statements = self.get_import_statements(value_funcs)

            if not os.path.isdir(self.unit_path):
                os.mkdir(self.unit_path)

            with open(os.path.join(self.unit_path, file_name), 'w') as file:
                file.write('import pytest\n')
                file.write('import json\n')
                file.write('from dsframework.base.tester.unit_test_generator.json_encoder import SanitizerEncoder\n')
                file.write('from dsframework.base.tester.unit_test_generator.utils import standardize_string\n')

                file.write(key_import + '\n')
                for import_statement in import_statements:
                    file.write(import_statement + '\n')
                file.write('\n')
                file.write(f'{underscore_class_name} = {class_name}({init_input_params})\n')
                file.write('\n')
                file.write('\n')

                for func in value_funcs:
                    if func["function"] == '__init__':
                        continue
                    file.write(f'def test_{func["function"]}():\n')
                    file.write('\n')

                    input_block_str = self.get_input_str(func['input'])

                    results = json.dumps(func['output'], cls=SanitizerEncoder)

                    file.write(f'    res = {underscore_class_name}.{func["function"]}({input_block_str})\n')
                    file.write(f'    result = json.dumps(res, cls=SanitizerEncoder)\n')
                    file.write(f'    expected_result = standardize_string(\'{results}\')\n')
                    file.write(f'    actual_result = standardize_string(result)\n')
                    file.write('\n')
                    file.write(f'    assert actual_result == expected_result\n')
                    file.write('\n')
                    file.write('\n')

    def get_init_params(self, value_funcs):
        for func in value_funcs:
            if func["function"] == '__init__':
                return func['input']

    def create_param_str_line(self, params):

        param_str = ''

        for key, value in params.items():
            if param_str != '':
                param_str += ', '
            param_str += f'{key}=\'{value}\''

        return param_str

    def get_input_str(self, input_param):

        input_str = ''

        for key, value in input_param.items():

            if input_str != '':
                input_str += ', '

            values = self.object_to_code(value)
            if isinstance(value, dict):
                input_str += f'{values}'
            else:
                input_str += f'{key}={values}'

        return input_str

    def get_results(self, output):
        res = output['result'][0]
        return res

    def object_to_code(self, obj, depth=0, max_depth=5):
        if depth > max_depth:
            return None

        if isinstance(obj, (int, float, complex, bool, str, type(None))):
            return repr(obj)

        if isinstance(obj, list):
            elements = ", ".join(self.object_to_code(item, depth + 1, max_depth) for item in obj)
            return f"[{elements}]"

        if isinstance(obj, tuple):
            elements = ", ".join(self.object_to_code(item, depth + 1, max_depth) for item in obj)
            return f"({elements})"

        if isinstance(obj, dict):
            return f'**{obj}'

        if hasattr(obj, "__dict__"):
            attributes = vars(obj)
            attribute_strings = [f"{attr}={self.object_to_code(value, depth + 1, max_depth)}" for attr, value in
                                 attributes.items()]
            return f"{type(obj).__name__}({', '.join(attribute_strings)})"

        return None

    def get_import_statements(self, func_metadata_list):

        import_statements = set()

        for func_metadata in func_metadata_list:
            import_stat = list(filter(None, str.split(func_metadata['import_statements'], ',')))

            if len(import_stat) > 0:
                import_statements.update(import_stat)

        return import_statements
