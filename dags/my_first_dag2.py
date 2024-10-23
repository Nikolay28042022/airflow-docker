from datetime import datetime
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator

def print_hello():
    print ('Привет, Николай!')

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 10, 23),
}

dag = DAG(
    'my_first_dag2',
    description='Hello Nikolay DAG',
    default_args=default_args,
    schedule_interval='0 12 * * *',
    catchup=False
)

hello_operator = PythonOperator(
    task_id='hello_task2',
    python_callable=print_hello,
    dag=dag
)