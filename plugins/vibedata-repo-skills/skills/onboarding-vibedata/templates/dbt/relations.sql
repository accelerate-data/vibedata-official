{# Selected single-database DuckDB only: stored views must survive a renamed copy. #}
{% macro ref() -%}
    {{ return(builtins.ref(*varargs, **kwargs).include(database=False)) }}
{%- endmacro %}

{% macro source() -%}
    {{ return(builtins.source(*varargs, **kwargs).include(database=False)) }}
{%- endmacro %}
