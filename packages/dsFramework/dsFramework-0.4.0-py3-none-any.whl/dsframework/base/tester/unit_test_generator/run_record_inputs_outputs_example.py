# Usage example to record inputs and outputs
# ==========================================


# from dsframework.base.tester.unit_test_generator.save_results import new_inputs_outputs_decorator
# from test_folder.minus_class import MinusClass
# from test_folder.multply_class import MultiplyClass
# from test_folder.plus_class import PlusClass
# from test_folder.src_test import DoCalculations
#
# DoCalculations.__new__ = new_inputs_outputs_decorator
# PlusClass.__new__ = new_inputs_outputs_decorator
# MinusClass.__new__ = new_inputs_outputs_decorator
# MultiplyClass.__new__ = new_inputs_outputs_decorator
#
# if __name__ == '__main__':
#     calc = DoCalculations('do_calculations')
#     res = calc.do_calc(5, 6)
#     print(res)
