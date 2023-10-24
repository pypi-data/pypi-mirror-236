import nbformat
from nbconvert import PythonExporter
import numpy as np
import pandas as pd
import time
import seaborn as sns
import math



def my_check_DZ_1(fil):

    checks = {
        "Task 1": lambda env: 1 if (env.get('number1') is not None and env.get('number2') is not None and isinstance(env['number1'], int) and isinstance(env['number2'], int) and env.get('num1') is not None and env['num1'] == env['number1'] + env['number2']) else 0,

        "Task 2": lambda env: 1 if (env.get('number1') is not None and env.get('number2') is not None and isinstance(env['number1'], int) and isinstance(env['number2'], int) and env.get('num2') is not None and env['num2'] == env['number1'] // env['number2']) else 0,

        "Task 3": lambda env: 1 if (env.get('number1') is not None and env.get('number2') is not None and isinstance(env['number1'], int) and isinstance(env['number2'], int) and env.get('num3') is not None and env['num3'] == env['number1'] % env['number2']) else 0,

        "Task 4": lambda env: 1 if (env.get('float_num1') is not None and env.get('float_num2') is not None and env.get('float_num3') is not None and env.get('num4') is not None and env['num4'] == env['float_num1'] * env['float_num2'] / env['float_num3']) else 0,

        "Task 5": lambda env: 1 if (env.get('num') is not None and env.get('num5') is not None and env['num5'] == round(env['num']**3 / 2, 1)) else 0,

        "Task 6": lambda env: 1 if (env.get('number1') is not None and env.get('number2') is not None and env.get('num6') is not None and env['num6'] == math.floor(env['number1'] - env['number2'])) else 0,

        "Task 7": lambda env: 1 if (env.get('number1') is not None and env.get('number2') is not None and env.get('num7') is not None and env['num7'] == math.ceil(env['number1'] - env['number2'])) else 0,

        "Task 8": lambda env: 1 if (env.get('a') is not None and env.get('b') is not None and env.get('num8') is not None and round(env['num8'], 1) in [round((env['a']**2 + env['b']**2)**.5, 1), round((env['a']**2 + env['b']**2)**.25, 1)]) else 0,

        "Task 9": lambda env: 1 if (env.get('pos_num') is not None and env.get('neg_num') is not None and env.get('num9') is not None and round(env['num9'], 1) in [round(abs(env['pos_num']) + abs(env['neg_num']), 1)]) else 0,

        "Task 10": lambda env: 1 if (env.get('temp') is not None and env.get('num10') is not None and round(5/9*(env['temp']-32), 2) == env['num10']) else 0,

        "Task 11": lambda env: 1 if (env.get('num11') is not None and round(((6 + 7/12 - 3 - 17/36)*2.5 - (4+1/3)/.65) / (16-.5), 5) == round(env['num11'], 5)) else 0,

        "Task 12": lambda env: 1 if (env.get('num12') is not None and round((11/4/1.1 + 3 + 1/3)/(2.5 - .4*10/3)/(5/7) - ((13/6+4.5)*.375)/(2.75-3/2), 3) == round(env['num12'], 3)) else 0,

        "Task 13": lambda env: 1 if (env.get('num13') is not None and round(11+ 2/5 + 15/2*(285.6/14 - 1-23/30 + 13/50)/(24.4 - 10.23), 3) == round(env['num13'], 3)) else 0,

        "Task 14": lambda env: 1 if (env.get('num14') is not None and round(((9-5-3/8)*(4+5/12 - 4/(2+2/3)) + (.3 - .5/4)*4/7) / (1/24 + .25/(40/3)), 3) == round(env['num14'], 3)) else 0,

        "Task 15": lambda env: 1 if (env.get('num15') is not None and round(5.75/.025) == round(env['num15'], 3)) else 0,

        "Task 16": lambda env: 1 if (env.get('num16') is not None and round(((.16*(3.2 - 3/40) + 25/11 * 4.125 / (3+3/4)) / (31/6*.3 - .3*4.5 + .3/3))*.4, 3) == round(env['num16'], 3)) else 0,

    }

    with open(fil, 'r', encoding='utf-8') as file:
        hw = nbformat.read(file, nbformat.NO_CONVERT)
        student_check = {}
        for row in hw.cells:
            if row.cell_type == 'markdown':
                if 'Task' in row['source'].split('\n')[0].replace('# ', ''):
                    task = row['source'].split('\n')[0].replace('# ', '')
                    student_check[task] = []
                else:
                    continue
            elif row.cell_type == 'code':
                student_check[task].append(row.source)

    student_result = []
    for task, codes in student_check.items():
        environment = {}
        for code in codes:
            environment = {"math": math, 'mt': math, 'ceil': math.ceil, 'sqrt': math.sqrt, 'floor': math.floor}
            try:
                exec(code, environment)
            except Exception as e:
                print(f"Ошибка при выполнении кода для {task}: {e}")

        try:
            checker = checks.get(task, lambda env: 0)
            student_result.append(checker(environment))
        except Exception:
            student_result.append(0)
    print(fil)
    print()
    return pd.Series(student_result, index=['Task_'+str(i) for i in range(1, 17)])




        