{{ config(
    materialized='table',
    indexes=[
        {'columns': ['date_key'], 'unique': true},
        {'columns': ['full_date'], 'unique': true},
        {'columns': ['year', 'month']},
        {'columns': ['quarter']},
        {'columns': ['day_of_week']}
    ],
    tags=['dimension', 'core', 'date']
) }}

with date_spine as (
    {{ dbt_utils.date_spine(
        datepart="day",
        start_date="cast('2008-01-01' as date)",
        end_date="cast('2010-12-31' as date)"
    ) }}
),

final as (
    select
        -- Primary key
        cast({{ dbt_utils.date_trunc('day', 'date_day') }} as date) as full_date,
        cast(to_char(date_day, 'YYYYMMDD') as integer) as date_key,

        -- Year attributes
        extract(year from date_day) as year,
        extract(quarter from date_day) as quarter,
        extract(month from date_day) as month,
        extract(week from date_day) as week_of_year,
        extract(day from date_day) as day_of_month,
        extract(dow from date_day) + 1 as day_of_week,  -- 1=Sunday, 7=Saturday
        extract(doy from date_day) as day_of_year,

        -- Month attributes
        to_char(date_day, 'Month') as month_name,
        to_char(date_day, 'Mon') as month_short_name,
        'Q' || extract(quarter from date_day) as quarter_name,
        extract(year from date_day) || '-Q' || extract(quarter from date_day) as year_quarter,

        -- Week attributes
        to_char(date_day, 'Day') as day_name,
        to_char(date_day, 'Dy') as day_short_name,
        case
            when extract(dow from date_day) in (0, 6) then true
            else false
        end as is_weekend,
        case
            when extract(dow from date_day) in (1, 2, 3, 4, 5) then true
            else false
        end as is_weekday,

        -- First/last day flags
        case
            when extract(day from date_day) = 1 then true
            else false
        end as is_first_day_of_month,
        case
            when date_day = date_trunc('month', date_day) + interval '1 month - 1 day' then true
            else false
        end as is_last_day_of_month,

        -- Holiday flags (US federal holidays - simplified)
        case
            when extract(month from date_day) = 1 and extract(day from date_day) = 1 then true  -- New Year's Day
            when extract(month from date_day) = 7 and extract(day from date_day) = 4 then true  -- Independence Day
            when extract(month from date_day) = 12 and extract(day from date_day) = 25 then true  -- Christmas
            else false
        end as is_holiday,

        -- Fiscal year (assuming Oct 1 - Sep 30)
        case
            when extract(month from date_day) >= 10 then extract(year from date_day) + 1
            else extract(year from date_day)
        end as fiscal_year,

        case
            when extract(month from date_day) >= 10 then extract(quarter from date_day) - 3
            when extract(month from date_day) >= 7 then extract(quarter from date_day) + 1
            when extract(month from date_day) >= 4 then extract(quarter from date_day) + 2
            else extract(quarter from date_day) + 3
        end as fiscal_quarter,

        -- Relative date flags
        case when date_day = current_date then true else false end as is_today,
        case when date_day = current_date - 1 then true else false end as is_yesterday,
        case when date_day > current_date then true else false end as is_future,
        case when date_day < current_date then true else false end as is_past

    from date_spine
)

select * from final
order by full_date