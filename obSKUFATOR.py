import random
import re

def obfuscate(input_file, output_file):
    code = input_file.read()
    untouchable = ['#include', '#define', '_CRT_SECURE_NO_WARNINGS', '<stdio.h>', '<stdlib.h>', '<string.h >', '<locale.h>'] #трогать эти штуки нельзя, тогда код на C/C++ работать не будет 

    code = re.sub('//.*', '', code) #удаление однстрочных комментов
    code = re.sub(r'/\*.*?\*/', '', code) # удаление многострочных комментов

    RANDOM_TYPES = ['int', 'float', 'double', 'long int', 'long long int']

    # Словарь для хранения соответствия старых и новых имен
    name_mapping = {}
    type_mapping = {}

    def generate_random_name(): # генератор нового имени 
        prefix = random.choice(['gamma', 'dove', 'hippopotamus', 'numerolog89212215657', 'lipton', 'carti_taro', 'DikiyBoris', 'DomashniyVladimir', 'This_is_our_obfuskator', 'Freestyle_wrestling', 'bread'])
        suffix = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=4))
        return f"{prefix}_{suffix}"

    pattern = r'\b(int|float|double)\s+([a-zA-Z_]\w*(?:\s*,\s*[a-zA-Z_]\w*)*)' # паттерн для поиска переменных
    matches = re.findall(pattern, code) # сам поиск 

    # Маппинги для имен и типов
    for original_type, vars_str in matches:
        # Маппинг для типа
        if original_type not in type_mapping:
            type_mapping[original_type] = random.choice(RANDOM_TYPES)
        
        # Маппинг для имен переменных
        var_names = [name.strip() for name in vars_str.split(',')]
        for var_name in var_names:
            if var_name not in name_mapping:
                name_mapping[var_name] = generate_random_name()

    def replace_match(match): #Функция для замены в коде
        original_type = match.group(1)
        vars_str = match.group(2)
        
        new_type = type_mapping[original_type] #Получаем новый тип
        
        var_names = [name.strip() for name in vars_str.split(',')] #Заменяем переменные
        new_vars = [name_mapping[name] for name in var_names]
        
        return f"{new_type} {', '.join(new_vars)}"

    code = re.sub(pattern, replace_match, code) # Заменяем все вхождения в коде 


def trash_code(): #создаём бесполезный if
    trash = []
    trash_name = random.choice(['counter', 'num', 'places', 'tablet', 'position'])
    trash_type = random.choice(['int', 'float', 'double', 'long int', 'long long int'])
    value = random.randint(0, 12683)
    trash.append(f"if ({random.randint(0, 995)} > {random.randint(0, 995)}) {{\n    {trash_type} {trash_name} = {value};\n    {trash_name}++;\n}}")
 
def trash_var(): #создаем рандомное кол-во мусорных переменных
    trash_var_code = []
    for _ in range(random.randint(1, 10)):
        trash_var_name = random.choice(['keys', 'crypto', 'cipher', 'dove', 'goose', 'trash_variable', 'rabbit', 'chocolate', 'orange', 'camp', 'mother', 'father', 'P_M_M_L', 'white'])
        trash_var_type = random.choice(['int', 'long int', 'long long int', 'float', 'double'])
        trash_var_value = random.randint(0, 2006)
        trash_var_code.append(f'{trash_var_type} {trash_var_name} = {trash_var_value};\n')
    return trash_var_code

input_file = open('passwrodxor.cpp', 'r')
