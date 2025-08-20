from prefect import flow, task
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.read_config import config_json
from get_data_dropbox import read_dropbox_file
from import_db import insert_data_to_db
from exec_procedure import exec_procedure

load_dotenv()  # carrega variáveis do .env
config = config_json()
print(os.environ.get("PREFECT_API_URL"))  # teste

# ===== Carregar nome dos arquivos a serem extraídos ======
pasta_dropbox = config["dropbox_folder"]
arquivo_candidatos = config["arquivos"]["candidatos"]
arquivo_bens = config["arquivos"]["bens"]
arquivo_despesas = config["arquivos"]["despesas"]
arquivo_votos = config["arquivos"]["votos"]
arquivo_receitas = config["arquivos"]["receitas"]

# ===== Carregar configurações do banco de dados =====
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

# ===== Carregar configurações das procedures =====
proc_historico_bens_candidatos = "historico.atualiza_bens_candidatos"


# ===== Tarefas =====
@task
def extrair_bens():
    return read_dropbox_file(pasta_dropbox,arquivo_bens)

@task
def extrair_candidatos():
    return read_dropbox_file(pasta_dropbox,arquivo_candidatos)

@task
def extrair_despesas():
    return read_dropbox_file(pasta_dropbox,arquivo_despesas)

@task
def extrair_receitas():
    return read_dropbox_file(pasta_dropbox,arquivo_receitas)

@task
def extrair_votos():
    return read_dropbox_file(pasta_dropbox,arquivo_votos)


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