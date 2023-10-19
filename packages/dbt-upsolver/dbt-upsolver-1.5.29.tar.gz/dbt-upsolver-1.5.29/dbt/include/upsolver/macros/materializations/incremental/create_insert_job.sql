{% macro get_create_insert_job_sql(job_identifier, into_relation, sync, options, map_columns_by_name, target_type) -%}

  {%- set enriched_options = adapter.enrich_options(options, target_type, 'transformation_options') -%}
  {%- if target_type == 'datalake' -%}
    {%- set target_type = '' -%}
  {%- endif -%}

  CREATE {{''}}
  {%- if sync -%}
    SYNC {{''}}
  {%- endif -%}
    JOB {{job_identifier}}
    {{ render_options(enriched_options, 'create') }}
  AS INSERT INTO {{target_type}} {{into_relation}}
  {%- if map_columns_by_name %}
    MAP_COLUMNS_BY_NAME
  {%- endif %}
  {{sql}}

{%- endmacro %}
