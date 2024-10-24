from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime
import random

# Определяем параметры DAG'а
default_args = {
    'start_date': datetime(2024, 10, 24),
    'catchup': False,  # Отключаем выполнение DAG'а в прошлом
}

# Функция для PythonOperator, которая генерирует случайное число и возводит его в квадрат
def generate_and_square():
    random_number = random.randint(1, 100)
    squared_number = random_number ** 2
    print(f"Исходное число: {random_number}, Результат: {squared_number}")

# Ваше местоположение для запроса
location = 'moscow'

# Создаем новый DAG
with DAG('combined_dag', default_args=default_args, schedule_interval=None) as dag:

    # Задача 1: BashOperator для генерации случайного числа и вывода его в консоль
    bash_task = BashOperator(
        task_id='generate_random_bash',
        bash_command='echo $(( RANDOM ))'
    )

    # Задача 2: PythonOperator для генерации случайного числа, возведения его в квадрат и вывода
    python_task = PythonOperator(
        task_id='generate_and_square_python',
        python_callable=generate_and_square
    )

    # Задача 3: SimpleHttpOperator для запроса погоды по указанному местоположению
    http_task = SimpleHttpOperator(
        task_id='get_weather_http',
        method='GET',
        endpoint=f'https://goweather.herokuapp.com/weather/{location}',
        headers={"Content-Type": "application/json"},
        log_response=True
    )

    # Задаем последовательный порядок выполнения операторов
    bash_task >> python_task >> http_task
