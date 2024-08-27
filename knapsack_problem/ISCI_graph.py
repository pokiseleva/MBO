import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

# Словарь для хранения суммарного процента отклонения и максимального процента отклонения для каждой размерности
dimension_deviation = defaultdict(lambda: {'total': 0, 'max': 0, 'count': 0})

with open('deviation_ISCI.txt', 'r') as file:
    lines = file.readlines()
    for i in range(0, len(lines), 3):
        dimension = int(lines[i].rstrip('\n'))
        percentage = float(lines[i + 1].rstrip('%\n'))
        dimension_deviation[dimension]['total'] += percentage
        dimension_deviation[dimension]['max'] = max(dimension_deviation[dimension]['max'], percentage)
        dimension_deviation[dimension]['count'] += 1
    
# Вычисление среднего отклонения для каждой размерности
dimension_avg_deviation = [dimension_deviation[dim]['total'] / dimension_deviation[dim]['count'] for dim in sorted(dimension_deviation.keys())]
# Вычисление максимального отклонения для каждой размерности
dimension_max_deviation = [dimension_deviation[dim]['max'] for dim in sorted(dimension_deviation.keys())]

# Создание списка размерностей
dimensions = sorted(dimension_deviation.keys())

# Создание списка индексов для позиционирования столбцов
index = np.arange(len(dimensions))
# Ширина каждого столбца
width = 0.4
plt.ylim(0, 13)
# Создание столбчатой диаграммы для среднего отклонения
plt.bar(index, dimension_avg_deviation, width=width, color='skyblue', label='Среднее отклонение')
# Создание столбчатой диаграммы для максимального отклонения
plt.bar(index + width, dimension_max_deviation, width=width, color='salmon', label='Максимальное отклонение')

# Настройка осей и заголовка
plt.xlabel('Размерность')
plt.ylabel('Процент отклонения')
plt.title('График для обратно сильно коррелированных задач')
plt.xticks(index + width / 2, dimensions)

# Добавление легенды
plt.legend()

# Отображение графика
plt.grid(True)
plt.show()
