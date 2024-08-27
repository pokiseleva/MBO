import numpy as np
from scipy.stats import levy
import math
import random
import time

Maxgen = 50 #максимальное поколение
Smax = 1 #максимальный шаг, который моет пройти бабочка за один раз
t = 1 #номер текущего поколения
p = 5/12 #доля бабочек на Земле 1
BAR = 5/12 #скорость регулировки бабочек
NP = 20 #общая численность популяции
NP1 = 8 #кол-во бабочек на Земле 1
NP2 = 12 #кол-во бабочек на Земле 2
peri = 1.2 #период миграции

#считаем общий вес и общую ценность 
def ValueAndWeights(x , с , w): #x имеет размерность x[NP, d*2+2], d равен размерность v. 
    #До d пробегает от 0 до d-1 => исходная популяция. 
    d = int((x.shape[1]-2)/2)
    NP = x.shape[0]
    for i in range(NP):
        total_с = 0
        total_w = 0
        for j in range(d,d*2): #от d, тк там заданы 0 и 1 задачи о ранце 0-1
            total_с = total_с + x[i,j] * с[j-d]
            total_w = total_w  + x[i,j] * w[j-d]
        w_index = d*2 + 1
        с_index = d*2 
        x[i,с_index] = float(total_с)
        x[i,w_index] = float(total_w)
    return x 


def sigmoid(x):
    y = 1/(1+np.exp(-x))
    return y

def Binary(x): #гибридная схема кодирования
    d = int((x.shape[1]-2)/2)
    for i in range(x.shape[0]):
        for j in range(d,d*2):
            if sigmoid(x[i,j-d]) >= 0.5:
                x[i,j] = 1
            else :
                x[i,j] = 0
    return x
    
def GeneratePopulation(NP , С, W ): #создаем популяцию
    d = С.shape[0] 
    data = np.empty([NP , d*2+2])
    for i in range(NP):
        for j in range(d):
            data[i,j] = random.uniform(-3,3)
    Binary(data)
    ValueAndWeights(data, С, W)
    return data

def SortFitness(x, num_items): #сортировка по приспособленности
    x = x[x[:, num_items*2].argsort()]
    x = np.flip(x,0)
    return x

def Update(x , с ,w): #обновление поколений 
    x = Binary(x)
    x = ValueAndWeights(x, с, w)
    return x


def MigrationOperator(SP1 , SP2 , peri , p , с , w): #оператор Миграции
    NP1 = SP1.shape[0] 
    d = int((SP1.shape[1]-2)/2) 
    NP2 = SP2.shape[0]
    p = NP1 / (NP1 + NP2)
    r = 0
    r1 = 0
    r2 = 0
    for i in range(NP1):
        for j in range(d):
            r = np.random.uniform(0 , 1) * peri 
            if r <= p:
                r1 = np.random.randint(0,NP1)
                SP1[i,j] =  SP1[r1,j] 
            else:
                r2 = np.random.randint(0,NP2)
                SP1[i,j] =  SP2[r2,j]
    SP1 = Update(SP1 , с, w)
    return SP1

def AdjustingOperator(SP2 , Xbest , Maxgen , Smax , t , p , BAR , с , w) : #регулирующий оператор
    NP2 = SP2.shape[0]
    d   = int((SP2.shape[1] - 2) / 2)
    dx = np.empty(d)
    omega = Smax / (t**2) 
    for i in range(d):
        StepSize = math.ceil(np.random.exponential(2 * Maxgen)) 
        dx[i] = levy.pdf(StepSize)
    for i in range(NP2):
        for j in range(d):
            rand = np.random.uniform(0 , 1)
            if rand <= p:
                SP2[i,j] = Xbest[j]
            else:
                r3 = np.random.randint(0,NP2)
                SP2[i,j] = SP2[r3,j]
                if rand > BAR:
                    SP2[i,j] = SP2[i,j] + omega * (dx[j] - 0.5) 
    Update(SP2, с, w)
    return SP2 


#упорядочим по плотности
def ArrangeDensity(W, С):
    dim = W.shape[0]
    index = np.arange(W.shape[0]).reshape(W.shape[0], 1)
    density = С / W  # удельная полезность
    H = np.concatenate((density, index), axis=1)
    H = H[np.argsort(H[:, 0])]
    H = np.flip(H, 0)
    H = H[:, 1]
    H = H[::-1]
    result = H.astype(int).reshape(dim, 1)
    return result

def Greedy(X , Wt , C , H , W): 
    #восстановление
    n = H.shape[0] #Массив H - это индексы упорядоченных элементов по их вместимости.
    d = int((X.shape[0]-2)/2)
    weight = 0 
    value = 0
    temp = 0
    #считаем вес 
    weight = np.dot(X[d:d*2], Wt)
    if (weight>W): #проверяем, не превышает ли вес вместимость рюкзака 
        for i in range(d): #для каждого элемента в области исследования
            temp = temp + X[H[i]+d] * Wt[H[i]] #рассматриваем следующий по емкости элемент в массиве H 
                                                            #добавляем в переменную временного веса
            if (temp > W): #если выбранный элемент превышает вместимость рюкзака
                temp = temp - X[H[i]+d] * Wt[H[i]] #возвращаем предыдущий вес
                X[H[i] + d] = 0  #обновление двоичного значение
                X[H[i]] =  - 3 #обновляем реальное значение 
        weight = temp #текущий вес рюкзака

#оптимизация
    for i in range(d):# для всех элементов X[H]
        if (X[H[i]+d] == 0) and ((weight + Wt[H[i]]) <= W): 
            X[H[i]+d] = 1 #обновление двоичного значение
            X[H[i]] = 0 #обновляем реальное значение  
            weight = weight + X[H[i]+d] * Wt[H[i]] 
#вычисление
    value = np.dot(X[d:d*2], C) 
    return X


def read_knapsack_problem_from_file(filename):
    # Открываем файл на чтение
    with open(filename, 'r') as file:
        # Читаем строки из файла
        lines = file.readlines()
        num_items = []
        capacity = []
        weight = []
        value = []
        
        for i in range(0, len(lines), 5):# Считываем значения num_items, capacity, weight и value
            num_items.append(int(lines[i].strip()))
            capacity.append(float(lines[i+1].strip()))
            weight.append(np.array(list(map(float, lines[i+2].split()))))
            value.append(np.array(list(map(float, lines[i+3].split()))))
        # Возвращаем значения в виде массива
        return num_items, capacity, weight, value


num_items, capacity, weight, value = read_knapsack_problem_from_file('UI_output.txt')
solution = []
knapsack_time = []
for i in range(len(num_items)):
#создаем вектор весов и ценности
    start_time = time.time()
    w = weight[i].reshape(num_items[i], 1)
    c = value[i].reshape(num_items[i], 1)
    H = ArrangeDensity(c, w)
    #print(H)
    generate = GeneratePopulation(NP , c, w) 
    #print(generate)
#начало алгоритма
    t=1
    while t <= Maxgen:
        generate = SortFitness(generate, num_items[i]) #сортировка каждую бабочку по степени приспособленности 
    #разделим бабочек на 2 субпопуляции
        SP1 = generate[:NP1,:]
        SP2 = generate[NP1:,:]
        best = generate[0,:] #лучшая бабочка монарх на земле 1 и земле 2
        SP1 = MigrationOperator(SP1, SP1, peri, p , c , w) #новая субпопуляция 1
        SP2 = AdjustingOperator(SP2, best, Maxgen, Smax, t, p, BAR , c , w) #новая субпопуляция 2
        generate = np.concatenate((SP1, SP2)) #объединение 2-х созданных субпопуляций
    #оптимизируем особей в соответствии с жадным алгоритмом
        for j in range(generate.shape[0]):
            generate[j] = Greedy(generate[j] , w, c, H , capacity[i])
        Update(generate , c,w) #оценка новой популяции
        generate = SortFitness(generate, num_items[i])
        best_solution = generate[0]
        t+=1
        pass

    solution.append(best_solution)
    end_time = time.time()
    knapsack_time.append(end_time-start_time)



with open("solution_MBO_data_UI.txt", "w") as file:
    for i in range(len(num_items)):  
        file.write(f"{num_items[i]}\n")
        file.write(f"{capacity[i]}\n")
        line1 = ' '.join(map(str, weight[i]))
        file.write(line1+"\n")
        line2 = ' '.join(map(str, value[i]))
        file.write(line2+"\n")
        file.write(str(solution[i][len(value[i]):len(value[i])*2]).replace("\n", ""))
        file.write("\n")
        file.write(str(solution[i][len(value[i])*2])+"\n")
        file.write(str(knapsack_time[i])+"\n")
        file.write("\n")



    