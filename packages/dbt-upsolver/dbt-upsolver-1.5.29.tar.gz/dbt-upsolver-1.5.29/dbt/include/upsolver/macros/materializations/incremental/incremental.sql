{% materialization incremental, adapter='upsolver' %}

  {%- set identifier = model['alias'] -%}
  {%- set model_config = model['config'] -%}
  {%- set incremental_strategy = adapter.get(model_config, 'incremental_strategy', False) -%}
  {%- set sync = adapter.get(model_config, 'sync', False) -%}
  {%- set options = adapter.get(model_config, 'options', {}) -%}
  {%- set source = adapter.get(model_config, 'source') -%}
  {%- set target_type = adapter.get(model_config, 'target_type', 'datalake').lower() -%}
  {%- set target_connection = adapter.get(model_config, 'target_connection', '').lower() -%}
  {%- set target_location = adapter.get(model_config, 'target_location', '').lower() -%}
  {%- set target_prefix = adapter.get(model_config, 'target_prefix', '').lower() -%}
  {%- set delete_condition = adapter.get(model_config, 'delete_condition', False) -%}
  {%- set partition_by = adapter.get(model_config, 'partition_by', []) -%}
  {%- set primary_key = adapter.get(model_config, 'primary_key', []) -%}
  {%- set map_columns_by_name = adapter.get(model_config, 'map_columns_by_name', False) -%}
  {%- set job_identifier = identifier + '_job' %}
  {%- set model_constraints = adapter.render_raw_model_constraints(raw_constraints=model['constraints']) -%}
  {%- set column_constraints = adapter.render_raw_columns_constraints(raw_columns=model['columns']) -%}

  {{ get_validate_constraints(model_constraints, column_constraints, incremental_strategy, target_type) }}

  {%- set old_relation = adapter.get_relation(identifier=job_identifier,
                                              schema=schema,
                                              database=database) -%}
  {%- set target_relation = api.Relation.create(identifier=job_identifier,
                                                schema=schema,
                                                database=database,
                                                type='incremental') -%}


  {{ run_hooks(pre_hooks, inside_transaction=False) }}
  {{ run_hooks(pre_hooks, inside_transaction=True) }}
  {{ log("model[config]: " ~ model['config'] ) }}
  {{ log("model['columns']): " ~ model['columns'] ) }}
  {{ log("model['constraints']: " ~ model['constraints'] ) }}

  {% if target_type  == 'datalake' %}
    {%- set table_relation = api.Relation.create(identifier=identifier,
                                                 schema=schema,
                                                 database=database,
                                                 type='table') -%}
    {%- set into_relation = table_relation -%}
    {%- call statement('create_table_if_not_exists') -%}
      {{ get_create_table_if_not_exists_sql(table_relation, partition_by, primary_key, options) }}
    {%- endcall -%}
  {%- elif  target_type  == 's3'-%}
    {%- set into_relation = database + ' location=' + "'" + target_location + "'" -%}
  {%- elif  target_type  == 'elasticsearch'-%}
    {%- set into_relation = database + ' prefix=' + "'" + target_prefix + "'" -%}
  {%- else -%}
    {%- set into_relation = database + '.' + schema + '.' + identifier -%}
  {%- endif %}
  {%- if old_relation -%}
    {%- call statement('main') -%}
      {{ get_alter_job_sql(job_identifier, options, incremental_strategy, source) }}
    {%- endcall %}
    {{ get_add_expectations_if_not_exists_sql(job_identifier, rendered_constraints = column_constraints + model_constraints) }}
  {%- else -%}
    {%- call statement('main') -%}
      {%- if incremental_strategy == 'merge' -%}
        {{ get_create_merge_job_sql(job_identifier, into_relation, sync,
                                    options, primary_key, delete_condition,
                                    target_type) }}
      {%- elif incremental_strategy == 'insert' -%}
        {{ get_create_insert_job_sql(job_identifier,
                                    into_relation, sync, options,
                                    map_columns_by_name, target_type) }}

      {%- else  -%}
        {{ get_create_copy_job_sql(job_identifier, sql,
                                   into_relation, sync, options, source,
                                   target_type, model_constraints, column_constraints) }}

      {%- endif -%}
    {%- endcall -%}
  {%- endif -%}

  {%- do persist_docs(target_relation, model) -%}
  {%- do persist_docs(table_relation, model) -%}

  {{ run_hooks(post_hooks, inside_transaction=False) }}
  {{ run_hooks(post_hooks, inside_transaction=True) }}

  {%- if target_type  == 'datalake' -%}
    {{ return({'relations': [target_relation, table_relation]}) }}
  {%- else  -%}
    {{ return({'relations': [target_relation]}) }}
  {%- endif -%}
{%- endmaterialization -%}
