import datetime

from airflow import models
from airflow.operators.python_operator import PythonOperator

from src.utils.common.logger import logger

dag_info = {
    'catchup': False,
    'schedule_interval': None,
    'description': None,
    'tags': ['indicator'],
    'on_success_callback': None,
    'on_failure_callback': None,
    'retries': 5,
    'retry_delay': datetime.timedelta(minutes=10),
    'start_date': datetime.datetime(2022, 1, 1)
}


def init_dag_info(**kwargs):
    for prop, val in kwargs.items():
        dag_info[prop] = val


def arrange_depend_injects(task, dependence, injects):
    for inject in injects:
        task << inject << dependence
        logger.debug('{} << {} << {}'.format(task, inject, dependence))
    return task


def arrange_depend(task, dependencies):
    for dependence in dependencies:
        task << dependence
        logger.debug('{} << {}'.format(task, dependence))
    return task


def create_dag(dag_id, **kwargs):
    init_dag_info(**kwargs)

    dag = models.DAG(
        dag_id=dag_id,
        catchup=dag_info['catchup'],
        schedule_interval=dag_info['schedule_interval'],
        description=dag_info['description'],
        tags=dag_info['tags'],
        on_success_callback=dag_info['on_success_callback'],
        on_failure_callback=dag_info['on_failure_callback'],
        default_args={
            'owner': 'airflow',
            'depends_on_past': False,
            'retries': 5 if not dag_info['retries'] else dag_info['retries'],
            'retry_delay': dag_info['retry_delay'],
            'start_date': dag_info['start_date']
        },
        concurrency=3
    )
    return dag


def create_task(dag, task_id, python_callable, op_kwargs=None, **kwargs):
    task = PythonOperator(
        dag=dag,
        task_id=task_id,
        python_callable=python_callable,
        op_kwargs=op_kwargs,
        **kwargs
    )
    return task
