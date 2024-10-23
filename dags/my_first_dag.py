from datetime import datetime
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator

def print_hello():
    return 'Hello world from first Airflow DAG!'

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 10, 23),
}

dag = DAG(
    'my_first_dag',
    description='Hello World DAG',
    default_args=default_args,
    schedule_interval='0 12 * * *',
    catchup=False
)

hello_operator = PythonOperator(
    task_id='hello_task',
    python_callable=print_hello,
    dag=dag
)
