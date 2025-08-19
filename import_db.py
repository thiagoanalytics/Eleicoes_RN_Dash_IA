from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd
import os


def insert_data_to_db(df,table_name,schema_name):
    # Carregar variáveis de ambiente do arquivo .env
    load_dotenv()

    # Configurar a conexão com o banco de dados
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')  
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

    #criar conexão com o sqlalchemy
    database_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(database_url)

    try:
        # Inserir os dados no banco usando os nomes das colunas do DataFrame
        df.to_sql(table_name, engine, schema=schema_name, if_exists="append", index=False)
        print(f"✅ Dados inseridos com sucesso na tabela {schema_name}.{table_name}!")
    except Exception as e:
        print(f"❌ Erro ao inserir dados: {e}")