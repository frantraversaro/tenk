import logging

import pandas as pd
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from src.extract.extract import get_companies_details
from src.io_utils import load_from_datalake, save_to_datalake

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

# Define the DAG
dag = DAG(
    'company_info_extraction_dag',
    default_args=default_args,
    description='A DAG to read data from 10K extraction and get company info',
    schedule_interval=None,  # Only trigger manually or via another DAG
    catchup=False,  # Disable backfill
)


# Reads 10K filings from datalake
def read_10k_filings(execution_date, **kwargs):
    date_str = execution_date.strftime('%Y%m%d')
    key = f'tenk_extraction/{date_str}/'
    df = load_from_datalake(key=key)
    logging.info(f'Loaded {len(df)} entries')
    data = df.to_dict(orient='records')
    kwargs['ti'].xcom_push(key='tenk_filing_data', value=data)


# Downloads and parses the companies details for companies in the 10K filings
def download_companies_details(**kwargs):
    data = kwargs['ti'].xcom_pull(key='tenk_filing_data', task_ids='read_10k_filings')
    df = pd.DataFrame.from_dict(data)
    company_details = get_companies_details(df)
    kwargs['ti'].xcom_push(key='companies_data', value=company_details)


# Save companies details in datalake
def load_companies_details(execution_date, **kwargs):
    data = kwargs['ti'].xcom_pull(key='companies_data', task_ids='download_companies_details')
    df = pd.DataFrame.from_dict(data)
    date_str = execution_date.strftime('%Y%m%d')
    key = f'companies_details/{date_str}/'
    save_to_datalake(df, key=key)


# Create the tasks
read_10k_filings = PythonOperator(
    task_id='read_10k_filings',
    python_callable=read_10k_filings,
    provide_context=True,
    dag=dag,
)

download_companies_details = PythonOperator(
    task_id='download_companies_details',
    python_callable=download_companies_details,
    provide_context=True,
    dag=dag,
)

load_companies_details = PythonOperator(
    task_id='load_companies_details',
    python_callable=load_companies_details,
    provide_context=True,
    dag=dag,
)

trigger_companies_dag = TriggerDagRunOperator(
    task_id='trigger_upload_companies_to_redshift_dag',
    trigger_dag_id='load_companies_table_to_redshift_dag',  # The DAG ID to trigger
    dag=dag,
)

trigger_10K_dag = TriggerDagRunOperator(
    task_id='trigger_upload_filings_to_redshift_dag',
    trigger_dag_id='load_filings_table_to_redshift_dag',  # The DAG ID to trigger
    dag=dag,
)

# Define the task dependencies
read_10k_filings >> download_companies_details >> load_companies_details >> [trigger_companies_dag, trigger_10K_dag]
