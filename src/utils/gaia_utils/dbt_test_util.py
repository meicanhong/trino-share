from datetime import datetime
import json
import pydash

from src.utils.common.file_util import read_file
from src.utils.common.constant import PROJECT_PATH

TIMELINESS = 'Timeliness'  # 时效性
UNIQUENESS = 'Uniqueness'  # 唯一性/重复性
CONTINUITY = 'Continuity'  # 连续性
NOT_NULL = 'Not_null'  # 空值校验
AVAILABILITY = 'Availability'  # 数值合理性
BUSINESS_ASSOCIATED = 'Business_associated'  # 业务校验
EXTERNAL_VALIDATION = 'External_validation'  # 业务外部校验


def format_result(domain, block_name, results):
    result = []
    for item in results:
        test_name = pydash.get(item, 'unique_id').split(".")[2].replace('dbt_utils_', '')
        unexpected_count = pydash.get(item, 'failures') if pydash.get(item, 'status') != 'error' else 0

        idx = test_name.index(block_name)
        _test_category = test_name[0:idx-1]

        test_column_start_idx = idx + len(block_name) + 1
        # 空值校验
        if _test_category == 'not_null':
            test_category = NOT_NULL

            test_column_end_idx = len(test_name)
            test_columns = test_name[test_column_start_idx:test_column_end_idx]

            notes = f'check if {test_columns} is not null.'
        # 数值合理性
        elif _test_category == 'accepted_range':
            test_category = AVAILABILITY

            end_idx = test_name.index('__')
            test_columns = test_name[test_column_start_idx:end_idx]

            _filter = test_name[end_idx+2:len(test_name)]
            arr = _filter.split('__')
            notes = f'check if {test_columns} between {arr[1]} and {arr[0]}.'
        # 连续性
        elif _test_category == 'expect_date_continuity':
            test_category = CONTINUITY

            end_idx = test_name.index('__')
            test_columns = test_name[test_column_start_idx:end_idx]

            notes = f'check date continuity.'
        # 唯一性
        elif _test_category == 'unique_combination_of_columns':
            test_category = UNIQUENESS

            test_column_end_idx = len(test_name)
            test_columns = test_name[test_column_start_idx:test_column_end_idx]

            notes = f'check if {test_columns} is unique.'
        # 时效性
        elif _test_category == 'expect_row_values_to_have_recent_data':
            test_category = TIMELINESS

            end_idx = test_name.index('__')
            test_columns = test_name[test_column_start_idx:end_idx]

            notes = f'check if there is any record yesterday.'
        else:
            test_category = ''
            test_columns = ''
            notes = ''

        expectation_suite_name = f'{block_name}_{test_category.lower()}_{test_columns}'
        expectation_args = test_columns

        data = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'domain': domain,
            'block': block_name,
            'category': 'dbt_test',
            'test_category': test_category,
            'test_name': test_name,
            'status': pydash.get(item, 'status'),
            'expectation_suite_name': expectation_suite_name,
            'test_columns': test_columns,
            'element_count': 0,
            'unexpected_count': unexpected_count,
            'unexpected_percent': 0.0,
            'notes': notes,
            'expectation_args': expectation_args,
            'message': pydash.get(item, 'message'),
            'on_date': datetime.now().strftime("%Y-%m-%d")
        }
        result.append(data)

    return result


def get_dbt_test_result(domain, block_name):
    json_data = json.loads(read_file('{}/target/run_results.json'.format(PROJECT_PATH)))
    result = format_result(domain, block_name, results=pydash.get(json_data, 'results'))
    return result



