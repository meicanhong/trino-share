import os
import pydash

from src.utils.common.constant import PROJECT_PATH
from src.utils.common.file_util import read_yaml_file
# from src.utils.common.logger import logger

cfg_file = '{}/profiles.yml'.format(PROJECT_PATH)


def get_cfg_info():
    info = read_yaml_file(cfg_file)
    target = os.environ.get('ENVIRONMENT', 'dev')
    env_info = pydash.get(info, 'trino_share.outputs.{}'.format(target))
    env_info['target'] = target
    env_info['need_warn'] = os.environ.get('need_warn', False)
    return env_info


TASK_CONTEXT = get_cfg_info()
