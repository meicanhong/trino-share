# Trino-Share
此项目主要分享我使用Trino落地实践过的一点经验

## Trino部署
参考项目下 /docker 目录，提供了连接各种 catalog 的方法，权限控制，认证校验和 Trino 内存调优的方法

## Trino稳定性调优
[Trino Worker 规避 OOM 思路](./doc/Trino-worker-memory-optimization.md)

## Trino-DBT生产数据
参考Demo: src/domain/dbt/demo.sql

所有指标生产都是按表来进行领域划分，每一个指标称之为一个 block

block 有俩个属性 domain 和 name，domain 为领域，name 为模型的名称

## Trino-Iceberg 表优化
todo

## Trino监控
todo

## Trino-Gateway
移步 [trino-gateway](https://github.com/meicanhong/trino-gateway)