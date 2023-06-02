from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime
import pandas as pd
import requests

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2021, 1, 1)
}

dag = DAG(
    'api_to_csv_dag',
    default_args=default_args,
    schedule_interval="@once",
)

def load_data():
    response = requests.get('https://api.publicapis.org/entries')
    data = response.json()['entries']
    df = pd.DataFrame(data)
    df.to_csv('/tmp/data.csv', header=False, index=False)
    return '/tmp/data.csv'

first_step_load = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

def print_data(**context):
    file_path = context['task_instance'].xcom_pull(task_ids='load_data')
    df = pd.read_csv(file_path, header=None)
    print(df)

second_step_print = PythonOperator(
    task_id='print_data',
    python_callable=print_data,
    provide_context=True,
    dag=dag,
)

first_step_load >> second_step_print