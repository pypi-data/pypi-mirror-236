{% macro get_add_expectations_if_not_exists_sql(job_identifier, rendered_constraints) -%}

  {%- for rendered_constraint in rendered_constraints %}
    {{ get_add_expectation_if_exists_sql(job_identifier, rendered_constraint) }}
  {%- endfor %}

{%- endmacro %}

{% macro get_add_expectation_if_exists_sql(job_identifier, rendered_constraint) -%}
  {%- set is_expectation_exists = adapter.is_expectation_exists(job_name = job_identifier, expectation_name = rendered_constraint['constraint_name']) -%}

  {% if not is_expectation_exists %}
    {% call statement('add_constraint') -%}
      ALTER JOB {{job_identifier}}
      ADD {{ rendered_constraint['rendered_constraint'] }}
    {% endcall %}
  {%- endif -%}

{%- endmacro %}

{% macro get_add_job_constraint_sql(job_identifier, rendered_constraint) -%}
  ALTER JOB {{job_identifier}}
  ADD {{ rendered_constraint['rendered_constraint'] }}
{%- endmacro %}

{% macro expectation_data(job_name, expectation_name) -%}
  {% call statement('get_expectation', fetch_result=True) -%}
    select * from system.monitoring.expectations
    where "job_name"='orders_raw_data_for_upsert_job'
    and "expectation_name"='{{expectation_name}}';
  {% endcall %}
  {{ return(load_result('get_expectation')) }}

{% endmacro %}
