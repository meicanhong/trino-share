from src.core.block.block_helper import BlockHelper

if __name__ == '__main__':
    args = {
        'tag': 'eth_dex_price'
    }
    BlockHelper.test_single_block('dbt', 'demo', args)
