from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime
import random

# Определяем параметры DAG'а
default_args = {
    'start_date': datetime(2024, 10, 24),
    'catchup': False,  # Это отключает выполнение DAG'а в прошлом
}

# Создаем новый DAG
with DAG('random_number_dag', default_args=default_args, schedule_interval='@daily') as dag:

    # Оператор, который генерирует случайное число и выводит его в консоль
    generate_random_number = BashOperator(
        task_id='generate_random_number',
        bash_command='echo $(( RANDOM ))'  # Генерация случайного числа в bash
    )

    generate_random_number
