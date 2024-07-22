import os

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from datetime import datetime, timedelta
import pandas as pd

from src.extract.extract import download_10k, extract_10K
from src.io_utils import save_to_datalake

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
    'tenk-extraction-dag',
    default_args=default_args,
    description='An ETL DAG to extract data from an API, transform it, and save as CSV',
    schedule_interval=timedelta(days=1),
    catchup=False
)


# Download 10K filings
def download_10K_filings(execution_date, **kwargs):
    data = download_10k(execution_date)
    kwargs['ti'].xcom_push(key='extracted_data', value=data)


# Load 10K filings in datalake
def load_10K_filings(execution_date, **kwargs):
    downloaded_data = kwargs['ti'].xcom_pull(key='extracted_data', task_ids='download_10K_filings')
    data = extract_10K(downloaded_data)
    df = pd.DataFrame.from_dict(data)
    date_str = execution_date.strftime('%Y%m%d')
    key = f'tenk_extraction/{date_str}/'
    save_to_datalake(df, key=key)


# Create the tasks
download_task = PythonOperator(
    task_id='download_10K_filings',
    python_callable=download_10K_filings,
    provide_context=True,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_10K_filings',
    python_callable=load_10K_filings,
    provide_context=True,
    dag=dag,
)

trigger_companies_dag = TriggerDagRunOperator(
    task_id='trigger_company_info_extraction_dag',
    trigger_dag_id='company-info-extraction-dag',  # The DAG ID to trigger
    dag=dag,
)

# Define the task dependencies
download_task >> load_task >> trigger_companies_dag
