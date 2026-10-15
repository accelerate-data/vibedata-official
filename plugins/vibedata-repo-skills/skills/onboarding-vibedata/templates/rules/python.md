# Python and notebooks

Scope: {{confirmed_python_notebook_paths}}.
Preserve existing entrypoints, public interfaces, package manager and execution assumptions. Inspect imports/configuration as text; discovery does not import application modules or execute notebooks. Keep notebook outputs and secret contents out of context. Register actual tests and explicit coverage gaps; Python code needs no invented dbt selector or dlt pipeline. Use bounded temporary fixtures. For a new pytest configuration, set tmp_path_retention_count = 0 and tmp_path_retention_policy = "failed".
