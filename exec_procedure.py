from sqlalchemy import create_engine, text
import os

from dotenv import load_dotenv


def exec_procedure(procedure):
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
    
    procedure_name = procedure
    print(f"🔄 Executando procedure: {procedure_name}")

    # Executar a procedure
    with engine.connect() as conn:
        conn.execute(text(f"CALL {procedure_name}()"))
        conn.commit()

    print(f"✅ Procedure {procedure_name} executada com sucesso!")

