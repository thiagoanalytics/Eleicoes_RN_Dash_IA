import dropbox
from dotenv import load_dotenv
import os
import pandas as pd
import tempfile

load_dotenv()
APP_KEY = os.getenv("APP_KEY")
APP_SECRET = os.getenv("APP_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

dbx = dropbox.Dropbox(
    app_key=APP_KEY,
    app_secret=APP_SECRET,
    oauth2_refresh_token=REFRESH_TOKEN
)

chunksize = 1000

def read_dropbox_file(pasta_dropbox,file_name):
    caminho_dropbox = f"{pasta_dropbox}/{file_name}"
    metadata, res = dbx.files_download(caminho_dropbox)

    print(f"\n📄 Carregando arquivo: {file_name}")

    # Cria um arquivo temporário no Windows
    tmp_path = os.path.join(tempfile.gettempdir(), f"{file_name}")

    # Escreve em chunks para evitar MemoryError
    with open(tmp_path, "wb") as f:
        for chunk in res.iter_content(chunk_size=8 * 1024):  # 8 KB
            if chunk:
                f.write(chunk)

    # Processa CSV em chunks do Pandas
    chunks = pd.read_csv(tmp_path, chunksize=chunksize)
    df = pd.concat(chunks, ignore_index=True)  # você ainda pode concatenar se couber na memória

    # Remove arquivo temporário
    os.remove(tmp_path)

    return df

