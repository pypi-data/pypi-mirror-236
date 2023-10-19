{% materialization connection, adapter='upsolver' %}
  {%- set identifier = model['alias'] -%}
  {%- set model_config = model['config'] -%}
  {% set connection_type = adapter.require(model_config, 'connection_type') %}
  {% set connection_options = adapter.require(model_config, 'connection_options') %}
  {% set enriched_options = adapter.enrich_options(connection_options, connection_type, 'connection_options') %}
  {% set enriched_editable_options = adapter.filter_options(enriched_options, 'editable') %}


  {%- set old_relation = adapter.get_relation(identifier=identifier,
                                              schema=schema,
                                              database=database) -%}
  {%- set target_relation = api.Relation.create(identifier=identifier,
                                                schema=schema,
                                                database=database,
                                                type="connection") -%}

  {{ run_hooks(pre_hooks, inside_transaction=False) }}
  {{ run_hooks(pre_hooks, inside_transaction=True) }}

  {% if old_relation %}
    {% call statement('main') %}
      ALTER {{ connection_type }} CONNECTION {{target_relation.identifier}}
        {{ render_options(enriched_editable_options, 'alter') }}
    {%- endcall %}
  {% else %}
    {% call statement('main') -%}
      CREATE {{ connection_type }} CONNECTION {{target_relation.identifier}}
        {{ render_options(enriched_options, 'create') }}
    {%- endcall %}
  {% endif %}

  {% do persist_docs(target_relation, model) %}

  {{ run_hooks(post_hooks, inside_transaction=False) }}
  {{ run_hooks(post_hooks, inside_transaction=True) }}

  {{ return({'relations': [target_relation]}) }}
{% endmaterialization %}
