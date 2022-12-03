import json
import subprocess
import pydash
from src.utils.common.constant import PROJECT_PATH
from src.utils.common.config_utils import TASK_CONTEXT
from src.utils.common.logger import logger


def exec_dbt(dbt_cmd):
    logger.info(" ".join(dbt_cmd))
    sp = subprocess.Popen(
        dbt_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd='.',
        close_fds=True)
    sp = sp
    logger.info("Output:")
    line = ''
    for line in iter(sp.stdout.readline, b''):
        line = line.decode('utf-8').rstrip()
        logger.info(line)
    sp.wait()
    logger.info(
        "Command exited with return code %s",
        sp.returncode
    )

    if sp.returncode:
        logger.error("dbt command failed")
        if dbt_cmd[1] != 'test':
            raise Exception("dbt command failed")


def run_dbt(dbt_path, args):
    full_refresh = pydash.get(args, 'full_refresh', False)
    compile_sql = pydash.get(args, 'compile_sql', False)
    run_test = pydash.get(args, 'run_test', False)
    dbt_vars = pydash.get(args, 'vars', None)
    tag = pydash.get(args, 'tag', None)

    run_type = 'run'
    if compile_sql:
        run_type = 'compile'
    if run_test:
        run_type = 'test'
    if tag:
        dbt_path = f'tag:{tag}'
    dbt_cmd = ['dbt', run_type, '--profiles-dir', f'{PROJECT_PATH}/', '--project-dir', f'{PROJECT_PATH}/', '--select',
               dbt_path, '--target', TASK_CONTEXT["target"]]
    if full_refresh:
        dbt_cmd.extend(['--full-refresh'])
    # if run_type == 'test':
    #     dbt_cmd.extend(['--store-failures'])
    if run_type != 'test' and dbt_vars is not None:
        dbt_cmd.extend(['--vars', json.dumps(dbt_vars)])
    logger.info(' '.join(dbt_cmd))
    exec_dbt(dbt_cmd)


def run_test_dbt(dbt_path):
    dbt_cmd = ['dbt', 'test', '--profiles-dir', f'{PROJECT_PATH}/', '--project-dir', f'{PROJECT_PATH}/', '--select',
               dbt_path, '--target', TASK_CONTEXT["target"]]
    exec_dbt(dbt_cmd)


def gen_temp_dbt_model(table, sql_path):
    logger.debug('gen temp dbt model table:=====> {}'.format(table))
    with open(sql_path, 'w') as f:
        f.write("""select * from {}""".format(table))
