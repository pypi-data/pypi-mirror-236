{% macro upsolver__get_catalog(information_schema, schemas)-%}

  {%- if (schemas | length) == 0 -%}
   {% set msg -%}
    There is no schemas
   {%endset-%}
   {% do exceptions.raise_compiler_error(msg) %}
  {%- endif -%}

  {%- set tables_sql -%}
    SELECT schema, name, created_by, comment, 'table' AS type
    FROM system.information_schema.tables;
  {%- endset -%}

  {%- set tables_result = run_query(tables_sql) -%}

  {% set columns_list = [] %}
  {% for row in tables_result %}
    {%- set columns_query -%}
      SELECT
        catalog as "table_database",
        schema as "table_schema",
        '{{row['name']}}' as "table_name",
        name as "column_name",
        data_type as "column_type",
        'table' as "table_type",
        '{{row['created_by']}}' as "table_owner",
        1 as "column_index",
        '{{row['comment']}}' as "column_comment"
      FROM system.information_schema.columns
      WHERE catalog='default_glue_catalog' AND   schema='{{row['schema']}}' AND "table"='{{row['name']}}'
    {%- endset -%}
    {% set columns = run_query(columns_query) %}
    {% do columns_list.append(columns) %}
  {% endfor %}
  {{ return(adapter.merge_tables(columns_list)) }}

{% endmacro %}
