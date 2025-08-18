import dropbox
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

TOKEN = os.getenv('TOKEN_DROPBOX')

dbx = dropbox.Dropbox(TOKEN)

# Lista arquivos na pasta raiz
for entry in dbx.files_list_folder("/eleicoes_bases").entries:
    print(entry.name)