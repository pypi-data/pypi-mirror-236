import os.path

from dsframework.base.tester.unit_test_generator.generate_unit_test import GenerateUnitTests

if __name__ == '__main__':

    json_path = '../../inputs_outputs_log.json'

    if os.path.exists(json_path):
        save_tests_path = 'unit_tests/'
        gen_unit = GenerateUnitTests(save_tests_path)

        unit_data_dict = gen_unit.build_dictionary_from_json(json_path)

        gen_unit.create_unit_test_files(unit_data_dict)
    else:
        print("""
        Run pipeline_test.py with:
            .__new__ = new_inputs_outputs_decorator - for all classes that need to be tested.
            This will generate inputs_outputs_log.json file.
        """)
