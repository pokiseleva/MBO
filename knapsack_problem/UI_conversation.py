def process_data(input_filename, output_filename):
    # Чтение данных из исходного файла
    with open(input_filename, 'r') as file:
        lines = file.readlines()

    data = []
    i = 0
    while i < len(lines):
        # Получение и обработка строк
        num_elements = lines[i].strip()
        first_row = lines[i + 1].strip().replace(',', ' ')
        second_row = lines[i + 2].strip().replace(',', ' ')
        
        # Подсчет количества элементов в каждой строке
        first_row_elements = len(first_row.split())
        second_row_elements = len(second_row.split())
        
        # Добавление данных в список
        data.append((first_row_elements, num_elements, first_row, second_row))
        i += 3

    # Запись данных в новый файл
    with open(output_filename, 'w') as file:
        for item in data:
            file.write(str(item[0]) + '\n')  # Количество элементов первой строки
            file.write(item[1] + '\n')       # Первое число
            file.write(item[2] + '\n')       # Первая строка без запятых
            file.write(item[3] + '\n')       # Вторая строка без запятых
            file.write('\n')                 # Пустая строка для разделения блоков

# Пример использования функции
process_data("UI.txt", "UI_output.txt")
