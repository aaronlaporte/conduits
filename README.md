# Conduits

General-purpose data engineering toolkit for Nomadata client work. This repo hosts reusable connectors, ETL pipelines, and orchestration glue so engagements can reuse common building blocks.

## Repository layout

| Path | Description |
| --- | --- |
| `conduits/connectors/` | Source connectors and sinks (e.g., Statcast, Excel, filesystem). |
| `conduits/pipelines/` | Reusable pipelines built from the connectors. |
| `conduits/examples/` | CLI scripts demonstrating how to run the pipelines locally. |
| `conduits/orchestration/airflow/` | Example DAGs that invoke the pipelines at scale. |
| `conduits/artifacts/` | Sample inputs/outputs for quick smoke tests. |

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Pipelines

### Statcast ingestion

The MLB Statcast ingestion flow pulls data via `pybaseball`, applies domain transforms, and lands daily CSVs. To run locally:

```bash
python -m conduits.examples.run_statcast
```

### Weekly performance report

Summarizes Excel-based tracking logs for client-ready reports:

```bash
python -m conduits.examples.run_weekly_report
```

This writes a `reports/latest_week.json` file that downstream tools (Tableau, PDF renderers) can consume.

## Airflow deployment

Example DAGs live under `conduits/orchestration/airflow/dags/`. Drop them into an Airflow instance and point the pipelines at production buckets or warehouses.

## Roadmap

- Add more connectors (Google Sheets, REST APIs, Snowflake).
- Introduce dbt-compatible staging models.
- Harden tests and CI workflows.
