import json
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger('trino_share')

logger.setLevel('INFO')

if __name__ == '__main__':
    logger.info('Hello, world!')
    logger.warning('This is too cool for stdlib')
    logger.error('error')
    logger.debug('debug log')
    logger.info(json.dumps({'a': 1, 'b': 2}, indent=4))
