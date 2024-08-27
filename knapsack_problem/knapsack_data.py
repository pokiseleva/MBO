import random
import time
import math
import numpy as np



def knapSack(wt, val, n, W): 
    K = [[0.0 for x in range(int(W*10) + 1)] for x in range(n + 1)] 
    combination = []
    for i in range(n + 1): 
        for w in range(int(W*10) + 1): 
            if i == 0 or w == 0:
                K[i][w] = 0
            elif wt[i-1]*10 <= w:
                K[i][w] = max(val[i-1] + K[i-1][w-int(wt[i-1]*10)], K[i-1][w])
            else:
                K[i][w] = K[i-1][w]
    combination = []
    i = n
    j = int(W*10)
    while i > 0 and j > 0:
        if K[i][j] != K[i-1][j]:
            combination.append(1)
            j -= int(wt[i-1]*10)
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
num_items, max_W, weight, value = read_knapsack_problem_from_file('UI_output.txt')
for i in range(0, len(num_items)):
    start_time = time.time()
    best_comb, best_v = knapSack(weight[i], value[i], num_items[i], max_W[i])
    best_combination.append(best_comb)
    best_value.append(best_v)
    end_time = time.time()
    knapsack_time.append(end_time-start_time)

 
with open("UI_data_result.txt", "w") as file:
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

