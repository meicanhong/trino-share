import pydash
from src.utils.common.logger import logger
from src.core.block.block_helper import BlockHelper
from src.utils.gaia_utils.dag_utils import create_dag, create_task, arrange_depend, arrange_depend_injects


class BlockAirflowHelper:

    @staticmethod
    def build_dag(domain: str, **kwargs):
        all_blocks = BlockHelper._get_domain_blocks(domain)
        all_blocks = list(filter(lambda n: '/others/' not in pydash.get(n, 'file_path'), all_blocks))
        dag = create_dag(domain, **kwargs)
        # init all task
        tasks = BlockAirflowHelper.init_tasks(dag=dag, blocks=all_blocks)
        # build dependencies
        BlockAirflowHelper.build_dependencies(tasks=tasks, blocks=all_blocks)
        return dag

    @staticmethod
    def init_tasks(dag, blocks):
        tasks = dict()
        for block in blocks:
            block_name = pydash.get(block, 'block.name')
            domain = pydash.get(block, 'block.domain')

            def run_block_airflow(**kwargs):
                _domain = kwargs['domain']
                _block_name = kwargs['block_name']
                BlockHelper.run_single_block(domain=_domain, block_name=_block_name, args={})

            tasks[block_name] = create_task(dag=dag,
                                            task_id='{}_{}'.format(block_name, 'run_block'),
                                            python_callable=run_block_airflow,
                                            op_kwargs={'domain': domain, 'block_name': block_name}
                                            )
        return tasks

    @staticmethod
    def build_dependencies(tasks, blocks):
        for block in blocks:
            block_name = pydash.get(block, 'block.name')
            task = tasks[block_name]
            for dependence in pydash.get(block, 'block.dependencies', []):
                dependence_task = tasks[dependence]
                injects = [tasks[item] for item in list(map(lambda n: pydash.get(n, 'block.name'), list(
                    filter(lambda i: pydash.get(i, 'block.inject') == dependence, blocks))))]
                if len(injects) > 0:
                    arrange_depend_injects(task=task, dependence=dependence_task, injects=injects)
                else:
                    arrange_depend(task=task, dependencies=[dependence_task])
            injects = [tasks[item] for item in list(map(lambda n: pydash.get(n, 'block.name'), list(
                filter(lambda i: pydash.get(i, 'block.inject') == block_name, blocks))))]
            for inject in injects:
                inject << task
                logger.debug('{}<<{}'.format(inject, task))
