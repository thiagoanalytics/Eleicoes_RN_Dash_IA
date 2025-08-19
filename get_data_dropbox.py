import dropbox
from dotenv import load_dotenv
import os
from config.read_config import config_json
import pandas as pd
from io import BytesIO

config = config_json()
#Variavéis de configurações
pasta_dropbox = config["dropbox_folder"]
candidatos = config["arquivos"]["candidatos"]
bens = config["arquivos"]["bens"]
despesas = config["arquivos"]["despesas"]
votos = config["arquivos"]["votos"]
receitas = config["arquivos"]["receitas"]


load_dotenv()
APP_KEY = os.getenv("APP_KEY")
APP_SECRET = os.getenv("APP_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

dbx = dropbox.Dropbox(
    app_key=APP_KEY,
    app_secret=APP_SECRET,
    oauth2_refresh_token=REFRESH_TOKEN
)

def dataframe_candidados():
    # Ler o arquivo específico
    caminho_dropbox = f"{pasta_dropbox}/{candidatos}"
    metadata, res = dbx.files_download(caminho_dropbox)  # baixa o arquivo em memória
    df = pd.read_csv(BytesIO(res.content))  # cria DataFrame

    print(f"\n📄 Carregando arquivo: {candidatos}")
    return df

def dataframe_bens():
    # Ler o arquivo específico
    caminho_dropbox = f"{pasta_dropbox}/{bens}"
    metadata, res = dbx.files_download(caminho_dropbox)  # baixa o arquivo em memória
    df = pd.read_csv(BytesIO(res.content))  # cria DataFrame

    print(f"\n📄 Carregando arquivo: {bens}")
    return df

def dataframe_despesas():
    # Ler o arquivo específico
    caminho_dropbox = f"{pasta_dropbox}/{despesas}"
    metadata, res = dbx.files_download(caminho_dropbox)  # baixa o arquivo em memória
    df = pd.read_csv(BytesIO(res.content))  # cria DataFrame

    print(f"\n📄 Carregando arquivo: {despesas}")
    return df

def dataframe_votos():
    # Ler o arquivo específico
    caminho_dropbox = f"{pasta_dropbox}/{votos}"
    metadata, res = dbx.files_download(caminho_dropbox)  # baixa o arquivo em memória
    df = pd.read_csv(BytesIO(res.content))  # cria DataFrame

    print(f"\n📄 Carregando arquivo: {votos}")
    return df

def dataframe_receitas():
    # Ler o arquivo específico
    caminho_dropbox = f"{pasta_dropbox}/{receitas}"
    metadata, res = dbx.files_download(caminho_dropbox)  # baixa o arquivo em memória
    df = pd.read_csv(BytesIO(res.content))  # cria DataFrame

    print(f"\n📄 Carregando arquivo: {receitas}")
    return df
