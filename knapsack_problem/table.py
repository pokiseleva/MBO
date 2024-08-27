import numpy as np
from collections import defaultdict
import tkinter as tk
from tkinter import ttk
import pandas as pd

# Словарь для хранения суммарного процента отклонения и максимального процента отклонения для каждой размерности
dimension_deviation_UI = defaultdict(lambda: {'total': 0, 'max': 0, 'count': 0})
dimension_deviation_WCI = defaultdict(lambda: {'total': 0, 'max': 0, 'count': 0})
dimension_deviation_SCI = defaultdict(lambda: {'total': 0, 'max': 0, 'count': 0})
dimension_deviation_ISCI = defaultdict(lambda: {'total': 0, 'max': 0, 'count': 0})

# Функция для чтения данных из файла и заполнения словаря отклонений
def read_deviation_file(file_path, deviation_dict):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 3):
            dimension = int(lines[i].rstrip('\n'))
            percentage = float(lines[i + 1].rstrip('%\n'))
            deviation_dict[dimension]['total'] += percentage
            deviation_dict[dimension]['max'] = max(deviation_dict[dimension]['max'], percentage)
            deviation_dict[dimension]['count'] += 1

# Чтение данных из файлов
read_deviation_file('deviation_UI.txt', dimension_deviation_UI)
read_deviation_file('deviation_WCI.txt', dimension_deviation_WCI)
read_deviation_file('deviation_SCI.txt', dimension_deviation_SCI)
read_deviation_file('deviation_ISCI.txt', dimension_deviation_ISCI)

# Функция для вычисления среднего и максимального отклонения
def calculate_deviation_stats(deviation_dict):
    avg_deviation = [round(deviation_dict[dim]['total'] / deviation_dict[dim]['count'], 2) for dim in sorted(deviation_dict.keys())]
    max_deviation = [deviation_dict[dim]['max'] for dim in sorted(deviation_dict.keys())]
    return avg_deviation, max_deviation

# Вычисление статистики отклонений
dimension_avg_deviation_UI, dimension_max_deviation_UI = calculate_deviation_stats(dimension_deviation_UI)
dimension_avg_deviation_WCI, dimension_max_deviation_WCI = calculate_deviation_stats(dimension_deviation_WCI)
dimension_avg_deviation_SCI, dimension_max_deviation_SCI = calculate_deviation_stats(dimension_deviation_SCI)
dimension_avg_deviation_ISCI, dimension_max_deviation_ISCI = calculate_deviation_stats(dimension_deviation_ISCI)

# Создание DataFrame для каждого типа задач
def create_deviation_dataframe(dimension_keys, avg_deviation, max_deviation):
    return pd.DataFrame({
        'Размерность': [str(dim) for dim in sorted(dimension_keys)],
        'Средний процент': avg_deviation,
        'Максимальный процент': max_deviation
    })

df_UI = create_deviation_dataframe(dimension_deviation_UI.keys(), dimension_avg_deviation_UI, dimension_max_deviation_UI)
df_WCI = create_deviation_dataframe(dimension_deviation_WCI.keys(), dimension_avg_deviation_WCI, dimension_max_deviation_WCI)
df_SCI = create_deviation_dataframe(dimension_deviation_SCI.keys(), dimension_avg_deviation_SCI, dimension_max_deviation_SCI)
df_ISCI = create_deviation_dataframe(dimension_deviation_ISCI.keys(), dimension_avg_deviation_ISCI, dimension_max_deviation_ISCI)

# Функция для создания окна с таблицей
def create_table_window(df, title):
    window = tk.Toplevel(root)
    window.title(title)

    tree = ttk.Treeview(window)
    tree["columns"] = list(df.columns)
    tree["show"] = "headings"
    
    for column in tree["columns"]:
        tree.heading(column, text=column)

    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    tree.pack(fill="both", expand=True)

# Создание основного окна
root = tk.Tk()
root.title("Таблицы отклонений")

# Кнопки для открытия таблиц в отдельном окне
btn_UI = tk.Button(root, text="Некоррелированные задачи", command=lambda: create_table_window(df_UI, "Отклонения для UI"))
btn_UI.pack(pady=5)

btn_WCI = tk.Button(root, text="Слабо коррелированные задачи", command=lambda: create_table_window(df_WCI, "Отклонения для WCI"))
btn_WCI.pack(pady=5)

btn_SCI = tk.Button(root, text="Сильно коррелированные задачи", command=lambda: create_table_window(df_SCI, "Отклонения для SCI"))
btn_SCI.pack(pady=5)

btn_ISCI = tk.Button(root, text="Обратно сильно коррелированные задачи", command=lambda: create_table_window(df_ISCI, "Отклонения для ISCI"))
btn_ISCI.pack(pady=5)

root.mainloop()
