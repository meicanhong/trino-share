import os
import yaml

from src.utils.common.constant import PROJECT_PATH
# from src.utils.common.logger import logger


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except FileExistsError:
            print('已存在目录,跳过')
            # logger.error('已存在目录,跳过')


def ensure_dir_enhanced(file_path):
    check_paths = file_path.replace('{}/'.format(PROJECT_PATH), '').split('/')
    check_path = PROJECT_PATH
    for item in check_paths:
        check_path += '/{}'.format(item)
        ensure_dir(check_path)


def read_file(filepath):
    with open(filepath) as file_handle:
        content = file_handle.read()
        return content


def read_yaml_file(yaml_filename):
    yaml_info = {}
    with open(yaml_filename, encoding='utf-8') as f:
        yaml_info = yaml.safe_load(f)
    return yaml_info


def write_yaml_file(yaml_file, py_object):
    ensure_dir(yaml_file)
    file = open(yaml_file, 'w', encoding='utf-8')
    yaml.dump(py_object, file, allow_unicode=True)
    file.close()


def write_append_file(filepath, s: str):
    with open(filepath, 'a+', encoding="utf-8") as file_handle:
        file_handle.write(s)


def write_file(filepath, s: str):
    ensure_dir(filepath)
    with open(filepath, 'w', encoding="utf-8") as file_handle:
        file_handle.write(s)
