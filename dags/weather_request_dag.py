from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from datetime import datetime

# Определяем параметры DAG'а
default_args = {
    'start_date': datetime(2024, 10, 24),
    'catchup': False,  # Отключаем выполнение DAG'а в прошлом
}

# Ваше местоположение
location = 'moscow'

# Создаем новый DAG
with DAG('weather_request_dag', default_args=default_args, schedule_interval=None) as dag:

    # Оператор для отправки HTTP-запроса
    get_weather = SimpleHttpOperator(
        task_id='get_weather',
        method='GET',
        endpoint=f'https://goweather.herokuapp.com/weather/{location}',  # Передаем полный URL
        headers={"Content-Type": "application/json"},
        log_response=True  # Логируем ответ для его отображения в логах
    )

    get_weather

