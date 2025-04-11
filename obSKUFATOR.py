import random
import re   #шелуха для создания регулярных выражений
import os

def obfuscate(input_file, output_file):
    def load_names_from_file(filename='/home/mefodiy/Documents/codes/Config_for_obfuskator.txt'):        #загружаем имена из файла
        if not os.path.exists(filename):   #если нет файла, то создаём свои
            default_names = [
                'gamma', 'dove', 'hippopotamus', 'numerolog89212215657',
                'lipton', 'carti_taro', 'DikiyBoris', 'DomashniyVladimir',
                'alpha', 'beta', 'sigma', 'omega', 'delta', 'epsilon'
            ]
            with open(filename, 'w') as f:
                f.write('\n'.join(default_names))
            return default_names
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip()]

    code = input_file.read()
    untouchable = ['#include', '#define', '_CRT_SECURE_NO_WARNINGS',
                   '<stdio.h>', '<stdlib.h>', '<string.h>', '<locale.h>']  #вообще тут имена, которые трогать нельзя, но вроде в коде этом не используются

    def remove_excessive_newlines(code):     #шняга, чтобы убирать переносы строк
        code = re.sub(r'\n{3,}', '\n\n', code)
        code = re.sub(r'\n+\s*}', '}', code)
        code = re.sub(r'{\n+', '{', code)
        return code

    def clean_code(code):    #тут убираем комменты, пробелы, табы
        code = re.sub(r'//.*', '', code)
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        code = re.sub(r'[ \t]+', ' ', code)
        code = re.sub(r'^[ \t]+', '', code, flags=re.MULTILINE)
        code = re.sub(r'[ \t]+$', '', code, flags=re.MULTILINE)
        code = re.sub(r'\n\s*\n', '\n', code)
        code = remove_excessive_newlines(code)    #а тут вызываем удаление переноса строк
        return code

    ALL_TYPES = ['int', 'float', 'double', 'long int', 'long long int', 'char']     #тут создаем списки типов данных для того, чтобы искать и заменять на другие 
    RANDOM_TYPES = ['int', 'float', 'double', 'long int', 'long long int']
    name_mapping = {}  #словарь для маппинга старых и новых имён переменных
    type_mapping = {}  # такая же хуйня для типов данных
    function_names = {}  #и для имен функций
    array_size_vars = set()
    name_pool = load_names_from_file()

    def generate_random_name(): #тут генерирум новые имена
        prefix = random.choice(name_pool)
        suffix = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=4))
        return f"{prefix}_{suffix}"

    array_size_pattern = r'\b(?:int|float|double|long\s+int|long\s+long\s+int|char)\s+([a-zA-Z_]\w*)\s*\[([^]]+)\]' #паттерн для поиска переменных, которые являются размером массива(не работает, да и хуй с этим)
    for match in re.finditer(array_size_pattern, code): #ваще тут мы ищем инты, которые являются размером массива, но эта залупа мозги ебёт и не хочет норм работать
        size_expr = match.group(2)
        var_matches = re.finditer(r'\b([a-zA-Z_]\w*)\b', size_expr)
        for var_match in var_matches:
            array_size_vars.add(var_match.group(1))

    protected_names = ['main', 'printf', 'scanf', 'malloc', 'free'] #тут имена функций, которые мы трогать не можем

    declaration_pattern = r'\b(int|float|double|long\s+int|long\s+long\s+int|char)\s+([a-zA-Z_]\w*(?:\s*,\s*[a-zA-Z_]\w*)*)(?=\s*(?:;|=|,))' #очередной паттерн для поиска переменных

    def process_declarations(match):   #функция обработки объявлений переменных
        original_type = match.group(1)   # исходный тип
        vars_str = match.group(2)   # строка с переменными
        var_names = [name.strip() for name in vars_str.split(',')]  # строка с переменными

        if any(name in protected_names for name in var_names):   #а тут короче если защищенно, то ретёним как было
            return match.group(0)

        if any(name in array_size_vars for name in var_names):
            new_type = 'int'
        elif original_type == 'char':
            new_type = 'char'
        else:
            new_type = random.choice(RANDOM_TYPES)

        if original_type not in type_mapping:
            type_mapping[original_type] = new_type

        new_vars = []   # список для новых имён, дальше шурудим там и проверям, чтобы все заменилось и ретёрним финалку
        for name in var_names:
            if name not in name_mapping:
                name_mapping[name] = generate_random_name()
            new_vars.append(name_mapping[name])

        return f"{type_mapping[original_type]} {', '.join(new_vars)}"

    code = re.sub(declaration_pattern, process_declarations, code)

    func_def_pattern = re.compile(r'\b(?:int|void|float|double|char|long\s+int|long\s+long\s+int)\s+([a-zA-Z_]\w*)\s*\([^;]*?\)\s*\{')    #ебать мой рот, но это очередной паттерн, но уже для функций

    for match in func_def_pattern.finditer(code):   #ну тут крч как до этого ищем, проверяем, чтобы название не было защищённым, меняем туда-сюда и ретёрним
        func_name = match.group(1)
        if func_name not in protected_names:
            function_names[func_name] = generate_random_name()

    def replace_func_definitions(m):
        full = m.group(0)
        old_name = m.group(1)
        if old_name in function_names:
            return full.replace(old_name, function_names[old_name], 1)
        return full

    code = func_def_pattern.sub(replace_func_definitions, code)

    if function_names:
        usage_pattern = r'\b(' + '|'.join(map(re.escape, function_names.keys())) + r')\b'
        code = re.sub(usage_pattern, lambda m: function_names[m.group(1)], code)    #а тут меняем имена при вызове функций, чтобы ide мозги не ебало, что я долбвёб и функцию не объявил

    if name_mapping:   #тут переменные подставляем новые
        usage_pattern = r'\b(' + '|'.join(map(re.escape, name_mapping.keys())) + r')\b'
        code = re.sub(usage_pattern, lambda m: name_mapping[m.group(1)], code)

    def generate_trash_function():   #генерирум мусорные функции
        func_name = generate_random_name() # ну тут крч генерим имена, типы данных и прочий творожок подзалупный
        ret_type = random.choice(ALL_TYPES)
        param_type = random.choice(ALL_TYPES)
        param_name = generate_random_name()

        #а тут крч шаблон для высера, который называется функцией
        func_code = f"""      
{ret_type} {func_name}({param_type} {param_name}){{           
    {random.choice(ALL_TYPES)} {generate_random_name()}={random.randint(0,1000)};
    {random.choice(ALL_TYPES)} {generate_random_name()}={random.randint(0,1000)};
    if({random.randint(0,1000)}>{random.randint(0,1000)}){{
        return {random.randint(0,1000)};}}
    return {param_name}+{random.randint(1,100)};}}
"""
        return clean_code(func_code)

    def insert_trash_functions(code):     #а тут мы уже залупно-мусорные функции вставляем в код, так, чтобы одна после инклудов и хуюдов была, а вторая перед main
        last_include_pos = 0
        for match in re.finditer(r'#(include|define)\b', code):
            last_include_pos = match.end()

        if last_include_pos > 0:
            end_pos = code.find('\n', last_include_pos)
            if end_pos == -1:
                end_pos = len(code)
            code = code[:end_pos] + "\n" + generate_trash_function() + code[end_pos:]

        main_pos = code.find('int main(')
        if main_pos != -1:
            code = code[:main_pos] + generate_trash_function() + "\n" + code[main_pos:]

        return code

    code = insert_trash_functions(code)   #тут применяем эту парашу

    main_match = re.search(r'int main\s*\([^)]*\)\s*\{', code)    #а тут переменные из говна вставляем, которые нахуй не всрались для работы кода, но нужны, чтобы все парашой измазать
    if main_match:
        main_start = main_match.end()
        trash_vars = []
        for _ in range(random.randint(5, 10)): #генерим рандомное количество переменных и вставляем в main 
            name = generate_random_name()
            var_type = random.choice(ALL_TYPES)
            value = f"'{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}'" if var_type == 'char' else random.randint(0, 10000)
            trash_vars.append(f'{var_type} {name}={value};')

        trash_if = f"if({random.randint(0,1000)}>{random.randint(0,1000)}){{{random.choice(ALL_TYPES)} {generate_random_name()}={random.randint(0,1000)};}}"    #а тут хуярим мусорный if 
        code = code[:main_start] + '\n' + '\n'.join(trash_vars) + '\n' + trash_if + code[main_start:]   #ебашим все в код

    code = clean_code(code)   #финальная уборка шлака нахуй из кода
    output_file.write(code) #записываем в код

with open('/home/mefodiy/Documents/codes/newpassword.c', 'r') as input_file:     #ну а тут уже читаем файлки-хуяйлки и наращиваем пивной живот коду
    with open('/home/mefodiy/Documents/codes/scuf.c', 'w') as output_file:
        obfuscate(input_file, output_file)

print("Обфускация успешно завершена!")   #чисто по приколу принт, можно член туда добавить
