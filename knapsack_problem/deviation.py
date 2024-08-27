import random
import time
import math
import numpy as np

with open('UI_data_result.txt', 'r') as f1:
    lines1 = f1.readlines()

# Открываем второй файл с 180 задачами о ранце
with open('solution_MBO_data_UI.txt', 'r') as f2:
    lines2 = f2.readlines()

# Создаем новый файл для хранения информации
with open('deviation_UI_data.txt', 'w') as f_new:
    # Проходим по строкам из первого файла
    for i in range(0, len(lines1), 7):
        # Записываем первую строку
        f_new.write(lines1[i])
        x1=float(lines1[i+5].strip())
        x2=float(lines2[i+5].strip())
       # f_new.write(lines2[i+5]+'%'+'\n\n')
        f_new.write(str(round((x1-x2)/x1*100, 2))+'%'+'\n\n')

        
