import sys

def my_function_with_a_very_extremely_long_name_that_should_probably_be_shorter(arg1, arg2, arg3, arg4):
    pass

def my_function_with_many_arguments(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15):
    pass

def my_function_with_long_arguments(long_argument_variable_name_1, long_argument_variable_name_2, long_argument_variable_name_3):
    pass


if __name__ == "__main__":
    max_weight = 100

    # So when the weight provided through the first argument is larger than the max_weight, we print that it is not good. If it is below the max weight we print that it is good
    print "{} is good".format(sys.argv[1]) if int(sys.argv[1]) <= max_weight else "{} is not good".format(sys.argv[1])

    if sys.argv[1] > max_weight:  # Only if the weight argument is larger (not equal) to the max_weight do we print that it is good
        print "{} is good".format(sys.argv[1])

    variable_1, variable_2, variable_3, variable_4, variable_5 = 50 + 10000000000000000000000000000000000000, 100, 100, 100, 100
