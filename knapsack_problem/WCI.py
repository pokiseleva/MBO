import random
import time
import math
import numpy as np


def generate_knapsack_problems_WCI(num_items):
    w = []
    c = []
    L=100
    for _ in range(num_items):
        weight = np.random.uniform(L/10 + 1, L)
        value = np.random.uniform(weight-L/10, weight+L/10)
        w.append(weight)
        c.append(value)
    A = 0
    for j in range(num_items):
        A += w[j]
    W = A/4 
    return w, c, W


with open("WCI_problems.txt", "w") as file:
    for num_items in range(10, 101, 10):
        for i in range(1, 10):
            weight, value, capacity = generate_knapsack_problems_WCI(num_items)
            file.write(f"{num_items}\n")
            file.write(f"{capacity}\n")
            line1 = ' '.join(map(str, weight))
            file.write(line1+"\n")
            line2 = ' '.join(map(str, value))
            file.write(line2+"\n")
            file.write("\n")
