# Trino Worker 规避 OOM 思路
Trino 内存管理是由 Master Coordinator 来做的
Trino 会每 2s 做一次内存分析：

- 分析当前集群内存是否溢出
   - 当前内存集群内存溢出：Trino 会检查当前集群内存溢出的持续时间，如果持续时间超过了预设值（默认5min），则会根据配置好的 Kill Query策略去 Kill 掉查询。
      - query-low-memory-killer-policy：
         - none ：不会杀死任何查询
         - total-reservation ：终止当前使用最多总内存的查询。
         - total-reservation-on-blocked-nodes：终止当前在内存不足的节点上使用最多内存的查询
- 分析当前时刻的所有查询是否超出了预设的内存上限
   - 分析查询是否超出了 query.max-memory-per-node / query.max-memory / query.max-total-memory，超出则 kill 掉

以上的内存管理是针对 query 的，不针对 master 节点解析SQL、分析、优化和调度的操作

Trino 资源组也可以限制用户使用内存
主要是通过 softMemoryLimit 限制内存的使用。
> 官方文档
> softMemoryLimit (required): maximum amount of distributed memory this group may use, before new queries become queued. May be specified as an absolute value (i.e. 1GB) or as a percentage (i.e. 10%) of the cluster’s memory.

意思是：在每个查询开始之前，会判断当前用户组使用集群的内存情况，如果超过了设定值，则在队列内等待。直至该用户组使用集群内存降下到预设值。
如：下面配置的意思是，所有的用户都属于admin组，admin组限制了在集群内最高并发50条查询，最长等待队列是300；当admin使用集群内存超过80%时，查询需要在队列中等待。
```json
{
  "rootGroups": [
    {
      "name": "admin",
      "softMemoryLimit": "80%",
      "hardConcurrencyLimit": 50,
      "maxQueued": 300,
    }
  ],
  "selectors": [
    {
      "user": ".*",
      "group": "admin"
    }
  ]
}
```

思路：

1. 配置每个查询的使用的内存上限
2. 降低当集群内存不足时， 降低 Trino kill query 的 delay time
3. 配置资源组，避免当集群内存负载高时插入新查询。
4. 开启 spill 选项，允许内存 load 到磁盘
