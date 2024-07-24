import logging

import pandas as pd
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

from src.io_utils import load_from_datalake
from src.load.load import load_filings, load_companies

# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Upload 10K filings to redshift
filings_dag = DAG(
    'load_filings_table_to_redshift_dag',
    default_args=default_args,
    description='A DAG to load extracted data to redshift',
    schedule_interval=None,  # Only trigger manually or via another DAG
    catchup=False,  # Disable backfill
)


def upload_10k_filings_to_redshift(execution_date, **kwargs):
    process_date = execution_date.strftime('%Y%m%d')
    key = f'tenk_extraction/{process_date}/'
    df = load_from_datalake(key=key)
    logging.info(f'Loaded {len(df)} entries')
    load_filings(df)


upload_10k_filings_to_redshift_task = PythonOperator(
    task_id='upload_10k_filings_to_redshift',
    python_callable=upload_10k_filings_to_redshift,
    provide_context=True,
    dag=filings_dag,
)


# Upload Companies details to redshift

companies_dag = DAG(
    'load_companies_table_to_redshift_dag',
    default_args=default_args,
    description='A DAG to load extracted data to redshift',
    schedule_interval=None,  # Only trigger manually or via another DAG
    catchup=False,  # Disable backfill
)

def upload_companies_details_to_redshift(execution_date, **kwargs):
    process_date = execution_date.strftime('%Y%m%d')
    key = f'companies_details/{process_date}/'
    df = load_from_datalake(key=key)
    logging.info(f'Loaded {len(df)} entries')
    load_companies(df, process_date)


# Create the tasks
upload_companies_details_to_redshift_task = PythonOperator(
    task_id='upload_companies_details_to_redshift',
    python_callable=upload_companies_details_to_redshift,
    provide_context=True,
    dag=companies_dag,
)
