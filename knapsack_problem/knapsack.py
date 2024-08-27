import random
import time
import math
import numpy as np

def generate_knapsack_problem(n, c_min, c_max, w_min, w_max):
    # Создаем список предметов с случайными весами и стоимостями
    w = []
    c = []
    for _ in range(n):
        value = np.random.uniform(c_min, c_max)
        weight = np.random.uniform(w_min, w_max)
        w.append(weight)
        c.append(value)
    return w, c

def generate_max_weight(n, c_min, c_max, w_min, w_max):
    w, c = generate_knapsack_problem(n, c_min, c_max, w_min, w_max)
    A = 0
    for j in range(n):
        A += w[j]
    W = A/4
    return W, w, c

with open("knapsack_problems.txt", "w") as file:
    for num_items in range(5, 20):
        capacity, weight, value = generate_max_weight(num_items, 1, 5, 1, 5)
        file.write(f"{num_items}\n")
        file.write(f"{capacity}\n")
        line1 = ' '.join(map(str, weight))
        file.write(line1+"\n")
        line2 = ' '.join(map(str, value))
        file.write(line2+"\n")
        file.write("\n")

def knapSack(w, c, n, W): 
    K = [[0.0 for x in range(int(W*10) + 1)] for x in range(n + 1)] 
    combination = []
    for i in range(n + 1): 
        for wt in range(int(W*10) + 1): 
            if i == 0 or wt == 0:
                K[i][wt] = 0
            elif w[i-1]*10 <= wt:
                K[i][wt] = max(c[i-1] + K[i-1][wt-int(w[i-1]*10)], K[i-1][wt])
            else:
                K[i][wt] = K[i-1][wt]
    combination = []
    i = n
    j = int(W*10)
    while i > 0 and j > 0:
        if K[i][j] != K[i-1][j]:
            combination.append(1)
            j -= int(w[i-1]*10)
        else:
            combination.append(0)
        i -= 1
    while len(combination)<n:
        combination.append(0)
    combination.reverse()     
    return combination, K[n][int(W*10)]


def read_knapsack_problem_from_file(filename):
    # Открываем файл на чтение
    with open(filename, 'r') as file:
        # Читаем строки из файла
        lines = file.readlines()
        num_items = []
        capacity = []
        weight = []
        value = []
        # Считываем значения num_items, capacity, weight и value
        for i in range(0, len(lines), 5):
            num_items.append(int(lines[i].strip()))
            capacity.append(float(lines[i+1].strip()))
            weight.append(list(map(float, lines[i+2].split())))
            value.append(list(map(float, lines[i+3].split())))
        # Возвращаем значения в виде массива
        return num_items, capacity, weight, value


# Чтение данных из файла
best_combination = []
best_value = []
knapsack_time = []
num_items, max_W, weight, value = read_knapsack_problem_from_file('knapsack_problems.txt')
for i in range(0, len(num_items)):
    start_time = time.time()
    best_comb, best_v = knapSack(weight[i], value[i], num_items[i], max_W[i])
    best_combination.append(best_comb)
    best_value.append(best_v)
    end_time = time.time()
    knapsack_time.append(end_time-start_time)

 
with open("solution_knapsack_problems.txt", "w") as file:
    for i in range(len(num_items)):  
        file.write(f"{num_items[i]}\n")
        file.write(f"{max_W[i]}\n")
        line1 = ' '.join(map(str, weight[i]))
        file.write(line1+"\n")
        line2 = ' '.join(map(str, value[i]))
        file.write(line2+"\n")
        file.write(str(best_combination[i])+"\n")
        file.write(str(best_value[i])+"\n")
        file.write(str(knapsack_time[i])+"\n")
        file.write("\n")
