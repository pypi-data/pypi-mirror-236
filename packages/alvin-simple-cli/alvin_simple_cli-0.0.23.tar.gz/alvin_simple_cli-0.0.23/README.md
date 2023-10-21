# alvin-new-cli

Install the Cli:
`pip install alvin-simple-cli`

Setup with your API key (_generate it in Alvin UI_):
`alvin setup --api-key MY_API_KEY`

## datafakehouse & Dbt Run

First we create a Datafakehouse. A datafakehouse is a virtual datawarehouse that only knows or cares about syntax and relations. Is does not contain any data or return any results.

We can create a Datafakehouse like this:
`alvin datafakehouse create-db-instance --sql-dialect BIGQUERY --format ENV`

Later on we will be able to run queries using `database_instance_id` and `database_token` as `user` and `password` when creating a database connection.

In DBT we can prepare or fill out our dbt `profiles.yml` with a new target as follows

```yaml
alvin-datafakehouse:
  # Pick up the ENV variables and use them for authentication
  user: "{{ env_var('ALVIN_DB_INSTANCE_ID') }}"
  password: "{{ env_var('ALVIN_DB_TOKEN') }}"

  # We should use the database and schema (project and dataset) as we do for production
  database: alvinai
  schema: production_schema
  host: db-wire-3ggwwp7l3q-ey.a.run.app
  # Of note the DBT type here is "snowflake" even if you are using a different database
  # Alvin Datafakehouse communicates over the snowflake connector
  type: snowflake
  warehouse: alvinai-bigquery-project
  account: alvin
  role: alvin_role
```

Next let us 
1. create a datafakehouse instance
2. set the needed data as ENV variables (the output of creating an instance)
3. run dbt with our alvin-test target

```bash
source <(alvin datafakehouse create-db-instance --sql-dialect BIGQUERY --format ENV) \
  && dbt run --target alvin-datafakehouse +my_model
````

Note - after successfully running this your env vars will be set in that shell session 
```bash
source <(alvin datafakehouse create-db-instance --sql-dialect BIGQUERY --format ENV)
```

