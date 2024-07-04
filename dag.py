from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from main import run

import requests
import json
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

## TAREAS

default_args={
    'owner': 'frantraversaro_coderhouse',
    'retries': 5,
    'retry_delay': timedelta(minutes=2) # 2 min de espera antes de cualquier re intento
}

api_dag = DAG(
        dag_id="create_daily_10k",
        default_args= default_args,
        description="DAG para consumir API y vaciar datos en Redshift",
        start_date=datetime(2024,7,3,10),
        schedule_interval='@daily'
    )

task1 = BashOperator(task_id='primera_tarea',
    bash_command='echo Iniciando...'
)

task2 = PythonOperator(
    task_id='download_data',
    python_callable=run,
    dag=api_dag,
)

task3 = BashOperator(
    task_id= 'tercera_tarea',
    bash_command='echo Proceso completado...'
)
task1 >> task2 >> task3