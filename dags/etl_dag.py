from airflow import DAG
from airflow.decorators import task
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import logging
from airflow.hooks.base import BaseHook

# Настройка логирования
logger = logging.getLogger(__name__)

# Определение DAG
with DAG(
    'etl_dag',
    start_date=datetime(2024, 10, 25),
    schedule_interval='@once',
    catchup=False,
    tags=['etl']
) as dag:

    @task
    def extract_booking():
        logger.info("Начало извлечения booking.csv")
        booking_df = pd.read_csv('/opt/airflow/data/booking.csv')
        logger.info(f"Извлечено {len(booking_df)} записей из booking.csv")
        return booking_df

    @task
    def extract_client():
        logger.info("Начало извлечения client.csv")
        client_df = pd.read_csv('/opt/airflow/data/client.csv')
        logger.info(f"Извлечено {len(client_df)} записей из client.csv")
        return client_df

    @task
    def extract_hotel():
        logger.info("Начало извлечения hotel.csv")
        hotel_df = pd.read_csv('/opt/airflow/data/hotel.csv')
        logger.info(f"Извлечено {len(hotel_df)} записей из hotel.csv")
        return hotel_df

    @task
    def transform_data(booking_df: pd.DataFrame, client_df: pd.DataFrame, hotel_df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Начало трансформации данных")

        # Объединение booking и client по 'client_id'
        merged_df = pd.merge(booking_df, client_df, on='client_id')
        logger.info(f"После первого объединения: {merged_df.shape[0]} записей, {merged_df.shape[1]} колонок")

        # Объединение с hotel по 'hotel_id'
        merged_df = pd.merge(merged_df, hotel_df, on='hotel_id')
        logger.info(f"После второго объединения: {merged_df.shape[0]} записей, {merged_df.shape[1]} колонок")

        # Приведение дат к формату 'YYYY-MM-DD'
        if 'date' in merged_df.columns:
            merged_df['date'] = pd.to_datetime(merged_df['date']).dt.strftime('%Y-%m-%d')
            logger.info("Дата приведена к формату 'YYYY-MM-DD'")
        else:
            logger.warning("Колонка 'date' отсутствует в данных")

        # Удаление невалидных колонок, если они существуют
        columns_to_drop = ['invalid_column1', 'invalid_column2']
        merged_df = merged_df.drop(columns=columns_to_drop, errors='ignore')
        logger.info(f"Удалены колонки: {columns_to_drop}")

        logger.info("Трансформация данных завершена")
        return merged_df



    @task
    def load_data(transformed_df: pd.DataFrame):
        logger.info("Начало загрузки данных в базу данных")
        connection = BaseHook.get_connection('my_postgres_connection')
        engine = create_engine(f'postgresql://{connection.login}:{connection.password}@{connection.host}:{connection.port}/{connection.schema}')
        try:
            transformed_df.to_sql('final_table', engine, if_exists='replace', index=False)
            logger.info(f"Данные успешно загружены в таблицу 'final_table' в базе данных '{connection.schema}'")
        except Exception as e:
            logger.error(f"Ошибка при загрузке данных: {e}")
            raise

    # Определение последовательности задач
    booking_data = extract_booking()
    client_data = extract_client()
    hotel_data = extract_hotel()

    transformed_data = transform_data(booking_data, client_data, hotel_data)
    load_data_task = load_data(transformed_data)