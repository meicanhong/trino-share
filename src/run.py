from src.core.block.block_helper import BlockHelper

if __name__ == '__main__':
    args = {
        # 'compile_sql': True,
        # 'full_refresh' : True
        "vars": {
        }
    }
    BlockHelper.run_single_block('dbt', 'demo', args)
