import random
import re
import os
import json

CONFIG_PATH = 'config.json'

def load_config(path=CONFIG_PATH):
    with open(path, 'r') as f:
        return json.load(f)

def obfuscate(input_file, output_file, config):
    def load_names_from_file(filename='names.txt'):
        if not os.path.exists(filename):
            default_names = ['alpha', 'beta', 'gamma', 'delta', 'omega', 'zulu']
            with open(filename, 'w') as f:
                f.write('\n'.join(default_names))
            return default_names
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip()]

    def remove_comments(code):
        code = re.sub(r'//.*', '', code)
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        return code

    def remove_spaces_tabs(code):
        if config["remove_tabs"]:
            code = code.replace('\t', '')
        if config["remove_spaces"]:
            code = re.sub(r'[ ]{2,}', ' ', code)
        return code

    def remove_newlines(code):
        code = re.sub(r'\n{3,}', '\n\n', code)
        code = re.sub(r'\n+\s*}', '}', code)
        code = re.sub(r'{\n+', '{', code)
        code = re.sub(r'\n\s*\n', '\n', code)
        return code

    def clean_code(code):
        if config["remove_comments"]:
            code = remove_comments(code)
        code = remove_spaces_tabs(code)
        if config["remove_newlines"]:
            code = remove_newlines(code)
        return code

    def generate_random_name():
        return f"{random.choice(name_pool)}_{random.randint(1000, 9999)}"

    def generate_trash_function():
        ret_type = random.choice(ALL_TYPES)
        param_type = random.choice(ALL_TYPES)
        param_name = generate_random_name()
        return f"""{ret_type} {generate_random_name()}({param_type} {param_name}) {{
    {random.choice(ALL_TYPES)} {generate_random_name()} = {random.randint(0, 1000)};
    if ({random.randint(0,100)} > {random.randint(0,100)}) {{
        return {random.randint(0, 100)};
    }}
    return {param_name} + {random.randint(1, 100)};
}}"""

    def insert_trash_functions(code):
        last_include_pos = 0
        for match in re.finditer(r'#(include|define)\b', code):
            last_include_pos = match.end()
        if last_include_pos > 0:
            end_pos = code.find('\n', last_include_pos)
            if end_pos == -1: end_pos = len(code)
            code = code[:end_pos] + "\n" + generate_trash_function() + code[end_pos:]

        main_pos = code.find('int main(')
        if main_pos != -1:
            code = code[:main_pos] + generate_trash_function() + "\n" + code[main_pos:]
        return code

    code = input_file.read()
    name_pool = load_names_from_file()
    ALL_TYPES = ['int', 'float', 'double', 'long int', 'long long int', 'char']

    if config["add_trash_functions"]:
        code = insert_trash_functions(code)

    main_match = re.search(r'int main\s*\([^)]*\)\s*\{', code)
    if main_match and (config["add_trash_variables"] or config["add_trash_ifs"]):
        main_start = main_match.end()
        inserts = []
        if config["add_trash_variables"]:
            for _ in range(random.randint(3, 6)):
                var_type = random.choice(ALL_TYPES)
                name = generate_random_name()
                value = f"'{random.choice('ABCDE')}'" if var_type == 'char' else random.randint(1, 1000)
                inserts.append(f"{var_type} {name} = {value};")
        if config["add_trash_ifs"]:
            inserts.append(f"if ({random.randint(1,100)} > {random.randint(1,100)}) {{ int {generate_random_name()} = {random.randint(0,999)}; }}")
        code = code[:main_start] + "\n" + '\n'.join(inserts) + "\n" + code[main_start:]

    code = clean_code(code)
    output_file.write(code)

if __name__ == "__main__":
    with open('/home/mefodiy/Documents/codes/newpassword.c', 'r') as infile:
        with open('/home/mefodiy/Documents/codes/scuf.c', 'w') as outfile:
            config = load_config()
            obfuscate(infile, outfile, config)

    print("Обфускация успешно завершена!")
