from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import random

# Определяем параметры DAG'а
default_args = {
    'start_date': datetime(2024, 10, 24),
    'catchup': False,  # Отключаем выполнение DAG'а в прошлом
}

# Функция, которая генерирует случайное число, возводит его в квадрат и выводит в консоль
def generate_and_square():
    random_number = random.randint(1, 100)  # Генерация случайного числа от 1 до 100
    squared_number = random_number ** 2  # Возведение в квадрат
    print(f"Исходное число: {random_number}, Результат: {squared_number}")

# Создаем новый DAG
with DAG('random_number_dag2', default_args=default_args, schedule_interval=None) as dag:

    # Оператор, который использует Python для выполнения функции
    generate_random_number = PythonOperator(
        task_id='generate_random_number2',
        python_callable=generate_and_square  # Указываем функцию, которую PythonOperator должен вызвать
    )

    generate_random_number
