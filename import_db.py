from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd
import os

chunksize = 1000

def insert_data_to_db(df, table_name, schema_name, chunksize=1000):
    from sqlalchemy import create_engine
    from dotenv import load_dotenv
    import os

    load_dotenv()

    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')  
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

    database_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(database_url)

    try:
        df.to_sql(
            table_name,
            engine,
            schema=schema_name,
            if_exists="append",
            index=False,
            chunksize=chunksize  # envia 1000 linhas por vez
        )
        print(f"✅ Dados inseridos com sucesso na tabela {schema_name}.{table_name}!")
    except Exception as e:
        print(f"❌ Erro ao inserir dados: {e}")