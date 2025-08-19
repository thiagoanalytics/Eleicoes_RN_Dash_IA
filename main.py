import pandas as pd
from config.read_config import config_json
from get_data_dropbox import dataframe_bens
from get_data_dropbox import dataframe_candidados
from get_data_dropbox import dataframe_despesas
from get_data_dropbox import dataframe_receitas
from get_data_dropbox import dataframe_votos
from import_db import insert_data_to_db

config = config_json()
database_list = []
# Percorre cada item da lista "database"
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


def main():
    # Obter dados dos bens
    bens_candidatos = dataframe_bens()
    
    # Obter dados dos candidatos
    candidatos = dataframe_candidados()
    
    # Obter dados das despesas
    despesas_candidatos = dataframe_despesas()
    
    # Obter dados das receitas
    receitas_candidatos = dataframe_receitas()

    # Obter dados dos votos
    votos_candidatos = dataframe_votos()

    #Enviar os dados para o banco o banco dados
    insert_data_to_db(bens_candidatos,bens_list["table"],bens_list["schema"])
    insert_data_to_db(candidatos,candidatos_list["table"],candidatos_list["schema"])
    insert_data_to_db(despesas_candidatos,despesas_list["table"],despesas_list["schema"])
    insert_data_to_db(receitas_candidatos,receitas_list["table"],receitas_list["schema"])
    insert_data_to_db(votos_candidatos,votos_list["table"],votos_list["schema"])

if __name__ == "__main__":

    main()
        