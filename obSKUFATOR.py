import re
import random
import string

def obfuscate_c_code(input_file, output_file):
    # Читаем исходный код
    with open(input_file, 'r') as f:
        code = f.read()
    
    # 1. Удаляем комментарии
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)  # Многострочные
    code = re.sub(r'//.*?$', '', code, flags=re.MULTILINE)   # Однострочные
    
    # 2. Удаляем лишние пробелы
    code = re.sub(r'[ \t]+', ' ', code)          # Множественные пробелы/табы
    code = re.sub(r'^[ \t]+', '', code, flags=re.MULTILINE)  # Пробелы в начале строки
    code = re.sub(r'[ \t]+$', '', code, flags=re.MULTILINE)  # Пробелы в конце строки
    code = re.sub(r'\n\s*\n', '\n', code)        # Пустые строки
    
    # 3. Заменяем имена переменных и функций
    variables = set(re.findall(r'\b(int|float|double|char)\s+([a-zA-Z_]\w*)', code))
    functions = set(re.findall(r'\b([a-zA-Z_]\w*)\s*\(', code))
    
    # Создаем словари для замены имен
    var_map = {name: f'v{random.randint(1, 999)}' for _, name in variables}
    func_map = {name: f'f{random.randint(1, 999)}' for name in functions}
    
    # Заменяем имена переменных
    for old_name, new_name in var_map.items():
        code = re.sub(r'\b' + old_name + r'\b', new_name, code)
    
    # Заменяем имена функций (кроме main)
    for old_name, new_name in func_map.items():
        if old_name != 'main':
            code = re.sub(r'\b' + old_name + r'\b', new_name, code)
    
    # 4. Добавляем мусорный код
    junk_code = generate_junk_code()
    code = code.replace('{', '{\n' + junk_code, 1)  # Добавляем в начало main
    
    # Записываем обфусцированный код
    with open(output_file, 'w') as f:
        f.write(code)

def generate_junk_code():
    """Генерирует простой мусорный код"""
    junk = []
    for _ in range(random.randint(3, 17)):  # 3 мусорных элемента
        # Мусорная переменная
        var_name = random.choice(['cnt', 'compare', 'move', 'teamlead', "Vorob'ev", 'Dota 2 is a piece of shit', 'wesrdthfgj']) + str(random.randint(1, 99))
        var_type = random.choice(['int', 'float', 'double', 'long'])
        value = random.randint(0, 100) if var_type == 'int' else f"{random.random()*10:.1f}f"
        junk.append(f"{var_type} {var_name} = {value};")
        
        # Мусорный if
        junk.append(f"if ({var_name} > {random.randint(0, 50)}) {{ }}")
    
    return '\n'.join(junk)

# Пример использования
if __name__ == "__main__":
    obfuscate_c_code('passworxor.c', 'Scufpasswordxor.c')
    print("Обскуфация завершена! Теперь код - скуфчик")