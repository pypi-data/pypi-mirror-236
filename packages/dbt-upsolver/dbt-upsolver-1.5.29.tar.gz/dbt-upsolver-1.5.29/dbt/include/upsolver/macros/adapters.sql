{% macro upsolver__alter_column_type(relation,column_name,new_column_type) -%}
'''Changes column name or data type'''
/*
    1. Create a new column (w/ temp name and correct type)
    2. Copy data over to it
    3. Drop the existing column (cascade!)
    4. Rename the new column to existing column
*/
{% endmacro %}

{macro upsolver__check_schema_exists(information_schema,schema) -%}
'''Checks if schema name exists and returns number or times it shows up.'''
  {{ print('Checks if schema name exists') }}
{% endmacro %}

{% macro upsolver__drop_relation(relation) -%}
'''Deletes relatonship identifer between tables.'''
  {% call statement('drop_relation') -%}
    drop materialized view {{ relation }}
  {%- endcall %}
{% endmacro %}

{% macro upsolver__drop_schema(relation) -%}
'''drops a schema in a target database.'''
/*
  1. If database exists
  2. search all calls of schema, and change include value to False, cascade it to backtrack
*/
{% endmacro %}


{% macro upsolver__get_columns_in_relation(relation) -%}
  {% if relation.type == 'table'  %}
  {% call statement('get_columns_relation', fetch_result=True, auto_begin=False) -%}
      SELECT * FROM system.information_schema.columns
      where "catalog" = {{relation.database}}
      and "schema" = {{relation.schema}}
      and AND "table" = {{relation.identifier}}

  {% endcall %}
  {% endif %}

  {{ return(load_result('get_columns_relation').table) }}
{% endmacro %}


{% macro list_relation_without_caching(schema_relation, relation_type) -%}
  {% set source = relation_type +'s' %}
  {% call statement('list_relation_without_caching', fetch_result=True) -%}
    select
      '{{ schema_relation.database }}' as database,
      name,
      '{{ schema_relation.schema }}' as schema,
      {% if relation_type == 'job' %}
        'incremental' as type
      {% else %}
        '{{ relation_type }}' as type
      {% endif %}
    from system.information_schema."{{ source }}"
      {% if relation_type in ['table', 'view'] %}
        where schema = '{{ schema_relation.schema }}'
      {% endif %}
  {% endcall %}
  {{ return(load_result('list_relation_without_caching').table) }}
{% endmacro %}

{% macro upsolver__list_schemas(database) -%}
'''Returns a table of unique schemas.'''
  {% set database = adapter.trim_quotes(database) %}
  {% call statement('list_schemas', fetch_result=True, auto_begin=False) -%}
      select schema from system.information_schema.tables
      where catalog = '{{database}}'
      group by 1;
  {% endcall %}

  {{ return(load_result('list_schemas').table) }}
{% endmacro %}

{% macro upsolver__rename_relation(from_relation, to_relation) -%}
'''Renames a relation in the database.'''
/*
  1. Search for a specific relation name
  2. alter table by targeting specific name and passing in new name
*/
{% endmacro %}

{% macro upsolver__truncate_relation(relation) -%}
'''Removes all rows from a targeted set of tables.'''
/*
  1. grab all tables tied to the relation
  2. remove rows from relations
*/
{% endmacro %}

{% macro upsolver__current_timestamp() -%}
'''Returns current UTC time'''
{# docs show not to be implemented currently. #}
{% endmacro %}

{% macro upsolver__create_arbitrary_object(sql) -%}
    {{ sql }}
{%- endmacro %}

{% macro upsolver_list_tables(schema_relation) -%}
  {% call statement('upsolver_list_tables', fetch_result=True) -%}
    select
      '{{ schema_relation.database }}' as database,
      name,
      '{{ schema_relation.schema }}' as schema,
      {% if relation_type == 'job' %}
        'incremental' as type
      {% else %}
        '{{ relation_type }}' as type
      {% endif %}
    from system.information_schema."{{ source }}"
      {% if relation_type in ['table', 'view'] %}
        where schema = '{{ schema_relation.schema }}'
      {% endif %}
  {% endcall %}
  {{ return(load_result('list_relation_without_caching').table) }}
{% endmacro %}

{% macro get_add_constraints(row_constraints) %}
  {{ return(add_constraints(row_constraints)) }}
{% endmacro %}

{% macro add_constraints(row_constraints) %}
    {% for c in row_constraints -%}
      WITH {{ c['rendered_constraint'] }}
    {% endfor %}
{% endmacro %}

{% macro get_validate_constraints(model_constraints, column_constraints, incremental_strategy, target_type)  %}
  {{ return(validate_constraints(model_constraints, column_constraints, incremental_strategy, target_type)) }}
{% endmacro %}

{% macro validate_constraints(model_constraints, column_constraints, incremental_strategy, target_type)  %}
  {% if (model_constraints or column_constraints) and incremental_strategy  and  incremental_strategy != 'copy' %}
    {{ exceptions.raise_compiler_error("Constraints not available for incremental strategy " ~ incremental_strategy) }}
  {% endif %}
  {% if (model_constraints or column_constraints)  and  target_type  not in ['datalake', 'snowflake']  %}
    {{ exceptions.raise_compiler_error("Constraints not available for target " ~ target_type) }}
  {% endif %}
{% endmacro %}

{% macro upsolver__generate_schema_name(custom_schema_name, node) -%}

    {%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%}

        {{ default_schema }}

    {%- else -%}

        {{ custom_schema_name | trim }}

    {%- endif -%}

{%- endmacro %}
