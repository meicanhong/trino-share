{{config(
    materialized='incremental',
    unique_key=['block_timestamp'],
    incremental_strategy='merge',
)}}
select current_timestamp as block_timestamp, 'trino-dbt-demo' as name