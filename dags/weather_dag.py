from datetime import datetime, timedelta
from airflow.decorators import dag, task
from pathlib import Path
import sys, os
from dotenv import load_dotenv

sys.path.insert(0, '/opt/airflow/src')

from src.extract_data import extract_weather_data
from src.load_data import load_weather_data
from src.transform_data import data_transformations

env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(env_path)

API_KEY = os.getenv('API_KEY')
url = f'https://api.openweathermap.org/data/2.5/weather?q=Sao Paulo,BR&units=metric&appid={API_KEY}'

@dag(
    dag_id='youtube_weather_pipeline',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5),
    },
    description='Pipeline de ETL - Clima de SP',
    schedule='@hourly', # A cada 1 hora, minuto, hora, dia do mês, mês, dia da semana
    start_date=datetime(2026, 4, 24),
    catchup=False,
    tags=['weather', 'etl']
)
    

def weather_pipeline():
    @task()
    def extract():
        extract_weather_data(url)

    @task()
    def transform():
        df = data_transformations()
        df.to_parquet('/opt/airflow/data/weather_data.parquet', index=False)

    @task()
    def load():
        import pandas as pd
        df = pd.read_parquet('/opt/airflow/data/weather_data.parquet')
        load_weather_data('sp_weather', df)
    
    extract() >> transform() >> load()

weather_pipeline()