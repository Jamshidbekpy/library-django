import ast

def get_function_variables(formula):
    tree = ast.parse(formula)
    function_def = next(node for node in tree.body if isinstance(node, ast.FunctionDef))
    variables = [arg.arg for arg in function_def.args.args]
    return variables




# from openpyxl import load_workbook


# old_data = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]
# new_data = [32, 54, 21, 33, 44, 55, 66, 77, 88, 99, 100, 66, 77, 88, 99, 100, 88, 45]


# wb = load_workbook('shablon.xlsx')

# def write_excel(ws, old_input, new_input, old_data, new_data):
#     for i in range(len(old_data)):
#         ws[old_input[i]] = old_data[i]
#         ws[new_input[i]] = new_data[i]


# ws = wb['ФХБ']
# old_input = [f"D{i}" for i in range(12, 30)]
# new_input = [f"F{i}" for i in range(12, 30)]

# write_excel(ws, old_input, new_input, old_data, new_data)


# # b2 -> s2
# # b3 -> s3
# ws2 = wb['даража']
# old_input2 = [f"{chr(66+i)}2" for i in range(len(old_data))]
# new_input2 = [f"{chr(66+i)}3" for i in range(len(old_data))]

# write_excel(ws2, old_input2, new_input2, old_data, new_data)



# # # b2 -> s2
# # # b3 -> s3
# ws3 = wb['%']
# # old_input3 = [f"{chr(66+i)}2" for i in range(len(old_data))]
# # new_input3 = [f"{chr(66+i)}3" for i in range(len(old_data))]

# write_excel(ws3, old_input2, new_input2, old_data, new_data)





# ws['C2'] = 'Full Name'
# ws['D3'] = '10.06.2003'
# ws['D4'] = '2'
# ws['D5'] = 'Address no'
# ws['D6'] = 'Manzil'


# wb.save("new_shablon.xlsx")

