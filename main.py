from src.extract_data import extract_weather_data
from src.load_data import load_weather_data
from src.transform_data import data_transformations

import os
from pathlib import Path
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(env_path)

# CORREÇÃO 1: Letras maiúsculas para bater com o arquivo .env
API_KEY = os.getenv('API_KEY')

# CORREÇÃO 2: Trava de segurança para garantir que a chave foi lida
if not API_KEY:
    logging.error("❌ ERRO: A API_KEY não foi encontrada! Verifique seu arquivo .env")
    exit() # Para o programa aqui mesmo

url = f'https://api.openweathermap.org/data/2.5/weather?q=Sao Paulo,BR&units=metric&appid={API_KEY}'
table_name = 'sp_weather'

def pipeline():
    try:
        logging.info("ETAPA 1: EXTRACT")
        # Capturamos o retorno da extração
        dados_extraidos = extract_weather_data(url)
        
        # CORREÇÃO 3: Se a extração falhar, abortamos antes de ir para a Etapa 2
        if not dados_extraidos:
            logging.error("❌ A extração de dados falhou. Abortando o pipeline.")
            return

        logging.info("ETAPA 2: TRANSFORM")
        df = data_transformations()
        
        logging.info("ETAPA 3: LOAD")
        load_weather_data(table_name, df)
        
        print("\n" + "="*60)
        print("✅ Pipeline concluído com sucesso!")
        print("="*60)
        
    except Exception as e:
        logging.error(f"❌ ERRO no Pipeline: {e}")
        import traceback
        traceback.print_exc()
    
pipeline()