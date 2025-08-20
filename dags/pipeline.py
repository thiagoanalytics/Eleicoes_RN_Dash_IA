from prefect import flow, task
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.read_config import config_json
from get_data_dropbox import (
    dataframe_bens,
    dataframe_candidados,
    dataframe_despesas,
    dataframe_receitas,
    dataframe_votos
)
from import_db import insert_data_to_db
from exec_procedure import exec_procedure

load_dotenv()  # carrega variáveis do .env

print(os.environ.get("PREFECT_API_URL"))  # teste

# ===== Carregar configurações =====
config = config_json()
database_list = []
for db_config in config["database"]:
    arquivo_key = db_config["arquivo"]   # chave do arquivo no JSON "arquivos"
    nome_arquivo = config["arquivos"][arquivo_key]  # nome do CSV
    schema = db_config["schema"]
    table = db_config["table"]

    database_list.append({
        "nome_arquivo": nome_arquivo,
        "schema": schema,
        "table": table
    })

candidatos_list = database_list[0]
bens_list = database_list[1]
despesas_list = database_list[2]
votos_list = database_list[3]
receitas_list = database_list[4]

proc_historico_bens_candidatos = "historico.atualiza_bens_candidatos"


# ===== Tarefas =====
@task
def extrair_bens():
    return dataframe_bens()

@task
def extrair_candidatos():
    return dataframe_candidados()

@task
def extrair_despesas():
    return dataframe_despesas()

@task
def extrair_receitas():
    return dataframe_receitas()

@task
def extrair_votos():
    return dataframe_votos()


@task
def carregar(df, schema, table):
    insert_data_to_db(df, table, schema)
    print(f"📤 Dados carregados em {schema}.{table}")

@task
def exec_SP(procedure):
    exec_procedure(procedure)
    

# ===== Flow principal =====
@flow
def pipeline_eleicoes():
    # Extração
    bens = extrair_bens()
    candidatos = extrair_candidatos()
    despesas = extrair_despesas()
    receitas = extrair_receitas()
    votos = extrair_votos()

    # Carga no banco
    carregar(bens, bens_list["schema"], bens_list["table"])
    carregar(candidatos, candidatos_list["schema"], candidatos_list["table"])
    carregar(despesas, despesas_list["schema"], despesas_list["table"])
    carregar(receitas, receitas_list["schema"], receitas_list["table"])
    carregar(votos, votos_list["schema"], votos_list["table"])

    # Executar Procedures
    exec_SP(proc_historico_bens_candidatos)

if __name__ == "__main__":
    pipeline_eleicoes()