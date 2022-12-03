{{config(
    materialized='incremental',
    unique_key=['token_address'],
    incremental_strategy='merge',
)}}
select 1 =1