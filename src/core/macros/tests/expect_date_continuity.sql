{% test expect_date_continuity(model, column_name, continuity_of_columns, datepart= 'day') %}

with group_table as (
                select date({{column_name}}) as last_day, {{continuity_of_columns}}
                from {{model}}
                group by date({{column_name}}), {{continuity_of_columns}}
    ),
    group_by_date as (
        select
            *,
            lead(last_day, 1, current_date) OVER(partition by {{continuity_of_columns}} ORDER BY last_day) as next_day
        from group_table
    ),
    next_date as (
        select *
        from group_by_date
        where date_diff('{{datepart}}', next_day, last_day) = 1
    ),
    next_date_total as (
        select count(*) as total from next_date
    ),
    date_total as (
	  select count(*) as total from group_table
	),
    unexpect_data as (
	  select t1.total - t2.total as unexpected_count from date_total as t1, next_date_total as t2
	)
    select * from unexpect_data where unexpected_count != 0

{% endtest %}
