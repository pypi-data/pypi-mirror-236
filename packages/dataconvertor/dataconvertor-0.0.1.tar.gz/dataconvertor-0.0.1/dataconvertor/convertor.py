def convert_data(data):
    # Получаем список ключей из первого элемента списка
    keys = list(data[0].keys())  
    # Получаем список значений для каждого ключа
    values = [[d[key] for key in keys] for d in data]  
    return [{'s': keys, 'd': values}]