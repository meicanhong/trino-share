import os

PROJECT_PATH = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../../'))
SRC_DIR = '{}/src'.format(PROJECT_PATH)
DBT_MODELS_DIR = '{}/models'.format(SRC_DIR)
TEMP_CACHE_PATH = '{}/.cache'.format(SRC_DIR)
TARGET_DIR = '{}/target'.format(SRC_DIR)
DATA_DIR = '{}/../data'.format(PROJECT_PATH)
TEST_SQL_FILE_PATH = '{}/run/gaia_dbt/src/models'.format(TARGET_DIR)
TARGET_PROD = 'prod'
TARGET_DEV = 'dev'

EVENT_PARSER_YML_CONFIG_PATH = f'{PROJECT_PATH}/src/domain/events/event_parser/yml_config'
EVENT_PARSER_SQL_OUTPUT_PATH = f'{PROJECT_PATH}/src/domain/events/'
EVENT_PARSER_RESOURCE_PATH = f'{PROJECT_PATH}/src/domain/events/event_parser/resources/'
