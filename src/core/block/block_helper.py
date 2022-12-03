import functools
import glob
import importlib.machinery as im
import inspect
import shutil
import pydash
from src.utils.common.file_util import read_yaml_file, ensure_dir_enhanced
from src.utils.common.constant import PROJECT_PATH, DBT_MODELS_DIR, SRC_DIR
from src.utils.common.logger import logger
from src.utils.gaia_utils.dbt_util import run_test_dbt, run_dbt
DOMAIN_PATHS = [PROJECT_PATH + '/src/domain']
MODELS_PATHS = [PROJECT_PATH + '/src/models/domain']


def build_dbt_cfg(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        blocks = func(*args, **kwargs)
        for block in blocks:
            if pydash.get(block, 'block.spark'):
                continue
            s_yml_path = pydash.get(block, 'file_path')
            d_yml_path = s_yml_path.replace(SRC_DIR, DBT_MODELS_DIR)
            ensure_dir_enhanced(d_yml_path)
            s_sql_path = s_yml_path.replace('.yml', '.sql')
            d_sql_path = s_sql_path.replace(SRC_DIR, DBT_MODELS_DIR)
            shutil.copy(s_yml_path, d_yml_path)
            shutil.copy(s_sql_path, d_sql_path)
        return blocks

    return wrapper


class BlockHelper:

    @staticmethod
    @build_dbt_cfg
    def get_domain_blocks(domain: str):
        # todo 放在这个文件全局
        return BlockHelper._get_domain_blocks(domain)

    @staticmethod
    def _get_domain_blocks(domain):
        domain_yml_info = []
        for item in DOMAIN_PATHS:
            file_list = glob.glob(item + f'/**/*.yml', recursive=True)
            for file_path in file_list:
                if 'template/' in file_path:
                    continue
                block = read_yaml_file(file_path)
                if pydash.get(block, 'block.spark'):
                    continue
                if pydash.get(block, 'block.domain') == domain:
                    block['file_path'] = file_path
                    logger.debug('find block: {}'.format(file_path.replace(item, '')))
                    domain_yml_info.append(block)
        if len(domain_yml_info) == 0:
            raise Exception(f'There is no define block in the domain {domain}')
        print(domain_yml_info)
        return domain_yml_info

    @staticmethod
    def get_domain_block(domain, block_name):
        blocks = BlockHelper.get_domain_blocks(domain)
        return pydash.find(blocks, {'block': {'name': block_name}})

    @staticmethod
    def get_domain_name(block: str):
        return pydash.get(block, 'block.domain')

    @staticmethod
    def get_block_sql_file_path(block):
        return pydash.get(block, 'file_path').replace('.yml', '.sql')

    @staticmethod
    def get_block_exec_file_path(block):
        # 默认执行文件为python
        return pydash.get(block, 'file_path').replace('.yml', '.py')

    @staticmethod
    def get_block_dbt_path(block):
        return BlockHelper.get_block_sql_file_path(block).replace(SRC_DIR, DBT_MODELS_DIR).replace(
            '{}/'.format(PROJECT_PATH), '')

    @staticmethod
    def get_block_class(block):
        exec_file = BlockHelper.get_block_exec_file_path(block)
        exec_module = im.SourceFileLoader('exec_module', exec_file).load_module()
        class_names = inspect.getmembers(exec_module, inspect.isclass)
        return [class_ for name, class_ in class_names if class_.__module__ == 'exec_module'][0]

    @staticmethod
    def run_block_dbt(block, args):
        dbt_path = BlockHelper.get_block_dbt_path(block)
        run_dbt(dbt_path, args)

    @staticmethod
    def _run_block(block, args):
        BlockHelper.run_block_dbt(block, args)

    @staticmethod
    def test_block_data(block):
        dbt_path = BlockHelper.get_block_dbt_path(block)
        run_test_dbt(dbt_path=dbt_path)

    @staticmethod
    def run_block(block, args: dict):
        try:
            # run task
            BlockHelper._run_block(block, args)
        except Exception as e:
            raise e

    @staticmethod
    def run_single_block(domain: str, block_name: str, args: dict):
        block = BlockHelper.get_domain_block(domain, block_name)
        BlockHelper.run_block(block, args)

    @staticmethod
    def test_single_block(domain: str, block_name: str, args: dict):
        args['run_test'] = True
        BlockHelper.run_single_block(domain, block_name, args)
