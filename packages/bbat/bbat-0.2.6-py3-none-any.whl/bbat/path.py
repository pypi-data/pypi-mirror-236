import os


def absolute_path(file_path):
    return os.path.abspath(file_path)

def file_extension(file_path) -> str:
    return os.path.splitext(file_path)[1]

def file_size(file_path):
    return os.path.getsize(file_path)

def is_exists(file_path):
    return os.path.exists(file_path)

def mkdir(path):
    os.makedirs(path, exist_ok=True)

def read_file(file_path):
    '''读取文件'''
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except IOError:
        print(f"Error reading file '{file_path}'.")
        return None
    
def write_file(file_path, content):
    '''写入文件'''
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
            print(f"Content written to file '{file_path}'.")
    except IOError:
        print(f"Error writing to file '{file_path}'.")


def save_pickle(data, filename):
    '''save pickle'''
    import pickle
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def load_pickle(filename):
    '''load pickle'''
    import pickle
    with open(filename, 'rb') as f:
        params = pickle.load(f)
    return params


def load_yaml(filename):
    '''读取yaml文件'''
    import yaml
    with open(filename, 'r', encoding='utf-8') as conf_file:
        config = yaml.safe_load(conf_file)
        return config

def load_json(filename):
    '''读取json文件'''
    import json
    with open(filename, 'r', encoding='utf-8') as conf_file:
        config = json.load(conf_file)
        return config