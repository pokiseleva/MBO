def process_line(line):
    # Разбиваем строку на компоненты
    components = [x.strip() for x in line.split(',')]

    # Извлекаем значения
    values_1 = list(map(int, components[0][1:-1].split()))
    values_2 = list(map(int, components[1][1:-1].split()))
    value_3 = int(components[2])

    # Форматируем вывод
    result = f"{len(values_1)}\n{value_3}\n{' '.join(map(str, values_1))}\n{' '.join(map(str, values_2))}"
    
    return result

# Имя входного файла
input_file_name = "knapsack_data.txt"
# Имя выходного файла
output_file_name = "knapsack_data_result.txt"

# Читаем строки из входного файла
with open(input_file_name, 'r') as input_file:
    lines = input_file.readlines()

# Обрабатываем строки и записываем результат в выходной файл
with open(output_file_name, 'w') as output_file:
    for line in lines:
        result = process_line(line)
        output_file.write(result + '\n\n')
