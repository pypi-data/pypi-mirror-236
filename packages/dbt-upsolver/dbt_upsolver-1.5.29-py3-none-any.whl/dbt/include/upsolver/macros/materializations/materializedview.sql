{% materialization materializedview, adapter='upsolver' %}
  {%- set identifier = model['alias'] -%}
  {%- set model_config = model['config'] -%}
  {% set sync = adapter.get(model_config, 'sync', False) %}
  {% set options = adapter.get(model_config, 'options', {}) %}
  {% set enriched_options = adapter.enrich_options(options, 'materialized_view', 'target_options') %}
  {% set enriched_editable_options = adapter.filter_options(enriched_options, 'editable') %}

  {%- set old_relation = adapter.get_relation(identifier=identifier,
                                              schema=schema,
                                              database=database) -%}
  {%- set target_relation = api.Relation.create(identifier=identifier,
                                                schema=schema,
                                                database=database,
                                                type="materializedview") -%}

  {{ run_hooks(pre_hooks, inside_transaction=False) }}
  {{ run_hooks(pre_hooks, inside_transaction=True) }}

    {% if old_relation %}
      {% call statement('main') -%}
        ALTER MATERIALIZED VIEW {{target_relation}}
          {{ render_options(enriched_editable_options, 'alter') }}
      {%- endcall %}
    {% else %}
      {% call statement('main') -%}
        CREATE
        {% if sync %}
          SYNC
        {% endif %}
        MATERIALIZED VIEW  {{target_relation}} AS
        {{ sql }}
        {{ render_options(enriched_options, 'create') }}
      {%- endcall %}
    {% endif %}

  {% do persist_docs(target_relation, model) %}

  {{ run_hooks(post_hooks, inside_transaction=False) }}
  {{ run_hooks(post_hooks, inside_transaction=True) }}

  {{ return({'relations': [target_relation]}) }}
{% endmaterialization %}
