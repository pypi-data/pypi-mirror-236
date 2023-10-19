{% macro get_create_table_if_not_exists_sql(target_relation, partition_by, primary_key, options) -%}

{%- set old_relation = adapter.get_relation(identifier=target_relation.identifier,
                                            schema=target_relation.schema,
                                            database=target_relation.database) -%}

  {%- set raw_columns = adapter.render_columns(raw_columns_from_config=partition_by+primary_key, raw_columns_from_columns=model['columns']) -%}
  {%- set columns_partitioned_by  = adapter.render_columns_names(partition_by) -%}
  {%- set columns_primary_key  = adapter.render_columns_names(primary_key) -%}
  {%- set enriched_options = adapter.enrich_options(options, 'datalake', 'target_options') -%}
  {%- set enriched_editable_options = adapter.filter_options(enriched_options, 'editable') -%}

  {%- if old_relation -%}
    ALTER TABLE {{target_relation}}
    {{ render_options(enriched_editable_options, 'alter') }}
  {%- else -%}
    CREATE TABLE {{ target_relation }}
    ({{ raw_columns }})
    {%- if partition_by %}
    PARTITIONED BY
      {{ columns_partitioned_by }}
    {%- endif -%}
    {%- if primary_key %}
    PRIMARY KEY
      {{ columns_primary_key }}
    {%- endif %}
    {{ render_options(enriched_options, 'create') }}
  {%- endif -%}

{%- endmacro %}
