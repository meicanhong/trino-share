import pandas as pd


class Block(object):
    block_config = None

    def __init__(self, block_cfg=None):
        self.block_config = block_cfg

    def load_data(self, run_date=None) -> pd.DataFrame:
        pass

    def run(self, depend_data=None, run_date=None):
        pass
