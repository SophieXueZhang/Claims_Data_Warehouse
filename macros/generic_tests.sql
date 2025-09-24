{% test expect_column_values_to_be_in_type_list(model, column_name, value_types) %}
    /*
    Test that ensures column values match expected data types
    Usage: expect_column_values_to_be_in_type_list:
             value_types: ['numeric', 'date', 'string']
    */
    select *
    from {{ model }}
    where {{ column_name }} is not null
      and not (
        {% for value_type in value_types -%}
          {% if value_type == 'numeric' -%}
            {{ column_name }} ~ '^[0-9]+\.?[0-9]*$'
          {% elif value_type == 'date' -%}
            {{ column_name }} ~ '^\d{4}-\d{2}-\d{2}$'
          {% elif value_type == 'string' -%}
            length({{ column_name }}) > 0
          {% endif -%}
          {%- if not loop.last %} or {% endif -%}
        {% endfor %}
      )
{% endtest %}

{% test expect_column_proportion_of_unique_values_to_be_between(model, column_name, min_value=0, max_value=1) %}
    /*
    Test that the proportion of unique values in a column falls within expected range
    */
    with validation as (
        select
            count(distinct {{ column_name }})::decimal / count(*) as proportion_unique
        from {{ model }}
        where {{ column_name }} is not null
    )
    select *
    from validation
    where proportion_unique < {{ min_value }}
       or proportion_unique > {{ max_value }}
{% endtest %}

{% test expect_column_values_to_match_like_pattern_list(model, column_name, like_pattern_list) %}
    /*
    Test that column values match at least one of the provided LIKE patterns
    Usage: expect_column_values_to_match_like_pattern_list:
             like_pattern_list: ['%@%.%', 'N/A', 'NULL']
    */
    select *
    from {{ model }}
    where {{ column_name }} is not null
      and not (
        {% for pattern in like_pattern_list -%}
          {{ column_name }} like '{{ pattern }}'
          {%- if not loop.last %} or {% endif -%}
        {% endfor %}
      )
{% endtest %}

{% test expect_multicolumn_sum_to_equal(model, column_list, sum_total) %}
    /*
    Test that the sum of multiple columns equals a specific total
    Usage: expect_multicolumn_sum_to_equal:
             column_list: [column_a, column_b, column_c]
             sum_total: 100
    */
    select *
    from {{ model }}
    where (
      {% for column in column_list -%}
        coalesce({{ column }}, 0)
        {%- if not loop.last %} + {% endif -%}
      {% endfor %}
    ) != {{ sum_total }}
{% endtest %}

{% test expect_column_pair_values_A_to_be_greater_than_B(model, column_A, column_B, or_equal=false) %}
    /*
    Test that values in column A are greater than (or equal to) values in column B
    */
    select *
    from {{ model }}
    where {{ column_A }} is not null
      and {{ column_B }} is not null
      and not (
        {{ column_A }} >{% if or_equal %}={% endif %} {{ column_B }}
      )
{% endtest %}

{% test expect_table_row_count_to_be_between(model, min_value=1, max_value=100000000) %}
    /*
    Test that table row count falls within expected range
    */
    with row_count as (
        select count(*) as actual_row_count
        from {{ model }}
    )
    select actual_row_count
    from row_count
    where actual_row_count < {{ min_value }}
       or actual_row_count > {{ max_value }}
{% endtest %}

{% test expect_table_columns_to_match_ordered_list(model, column_list) %}
    /*
    Test that table has exactly the expected columns in the specified order
    */
    {% set actual_columns_query %}
        select column_name
        from information_schema.columns
        where table_name = '{{ model.name }}'
          and table_schema = '{{ model.schema }}'
        order by ordinal_position
    {% endset %}

    {% set results = run_query(actual_columns_query) %}
    {% set actual_columns = results.columns[0].values() %}

    {% if actual_columns != column_list %}
        select
            '{{ actual_columns | join(", ") }}' as actual_columns,
            '{{ column_list | join(", ") }}' as expected_columns
        where 1=1  -- This will always return a row indicating the test failed
    {% else %}
        select 1 where false  -- This will return no rows indicating the test passed
    {% endif %}
{% endtest %}

{% test expect_column_quantile_values_to_be_between(model, column_name, quantile, min_value, max_value) %}
    /*
    Test that a specific quantile of a column falls within expected range
    */
    with quantile_value as (
        select
            percentile_cont({{ quantile }}) within group (order by {{ column_name }}) as quantile_result
        from {{ model }}
        where {{ column_name }} is not null
    )
    select quantile_result
    from quantile_value
    where quantile_result < {{ min_value }}
       or quantile_result > {{ max_value }}
{% endtest %}