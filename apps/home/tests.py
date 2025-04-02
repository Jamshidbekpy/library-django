from django.test import TestCase

import types
 
code_string = """

a = 5
a += 6
b = 10

c = a + b

s = sqrt(16)

"""
# my_namespace = types.SimpleNamespace()
# exec(code_string, my_namespace.__dict__)
# print(my_namespace.c)  # 11
# print(my_namespace.s)  # 4.0
# print(my_namespace)  # 11

# a = 5
# b = 8
# formula = """
# def solution(a, b):
#     return a + b
    
# """
# my_namespace = types.SimpleNamespace()
# exec(formula,  my_namespace.__dict__)

# res = my_namespace.solution(a, b)
# print(res)  # 13





# import ast

# # formula (funksiya) o'zgaruvchilarini aniqlash uchun yordamchi funksiya
# def get_function_variables(formula):
#     tree = ast.parse(formula)
#     function_def = next(node for node in tree.body if isinstance(node, ast.FunctionDef))
#     variables = {arg.arg for arg in function_def.args.args}
#     return variables

# formula = """
# def solution(aa, b):
#     return aa + b
# """

# # Funksiya o'zgaruvchilarini aniqlash
# variables = get_function_variables(formula)
# print(variables)  # {'a', 'b'}

# # Keyin funksiya yordamida qiymatlarni hisoblash
# a = 5
# b = 8
# my_namespace = types.SimpleNamespace()
# exec(formula,  my_namespace.__dict__)
# res = my_namespace.solution(a, b)
# print(res)  # 13





import ast

# formula (funksiya) ichidagi barcha o'zgaruvchilarni aniqlash uchun yordamchi funksiya
def get_function_variables(formula):
    tree = ast.parse(formula)
    function_def = next(node for node in tree.body if isinstance(node, ast.FunctionDef))
    variables = [arg.arg for arg in function_def.args.args]
    return variables

formula = """
def solution(a, b, c):
    d = a+b
    e = d*c
    return e
"""

# Funksiya ichidagi barcha o'zgaruvchilarni aniqlash
all_variables = get_function_variables(formula)
print(all_variables)  # {'a', 'b', 'c'}

# Funksiyani bajarish uchun kerakli qiymatlarni tayyorlash
a = 5
b = 8
c = 10
my_namespace = types.SimpleNamespace()
exec(formula,  my_namespace.__dict__)
res = my_namespace.solution(a, b, c)
print(res)  # 23
