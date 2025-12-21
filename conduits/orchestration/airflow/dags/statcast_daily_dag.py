"""Example Airflow DAG for running the Statcast pipeline."""
from __future__ import annotations

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from conduits.pipelines.statcast_daily import StatcastDailyPipeline


def run_pipeline(**kwargs):
    execution_date = kwargs.get("execution_date", datetime.utcnow())
    start = (execution_date - timedelta(days=7)).strftime("%Y-%m-%d")
    end = (execution_date - timedelta(days=1)).strftime("%Y-%m-%d")
    pipe = StatcastDailyPipeline(start, end, "/opt/airflow/data/statcast")
    ctx = pipe.run(start_date=start, end_date=end)
    return ctx.metadata


def build_dag():
    with DAG(
        dag_id="statcast_daily",
        start_date=datetime(2024, 1, 1),
        schedule_interval="@daily",
        catchup=False,
        default_args={"owner": "conduits", "retries": 1, "retry_delay": timedelta(minutes=10)},
    ) as dag:
        PythonOperator(
            task_id="pull_statcast",
            python_callable=run_pipeline,
            provide_context=True,
        )
    return dag


dag = build_dag()
