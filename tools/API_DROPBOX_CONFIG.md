
# Dropbox API Integration

Este projeto ensina como criar um aplicativo no Dropbox, gerar tokens de acesso usando o fluxo PKCE e refresh token, e acessar arquivos diretamente do Dropbox via Python.

---

## 1️⃣ Criar um App no Dropbox

1. Acesse o [Dropbox App Console](https://www.dropbox.com/developers/apps).
2. Clique em **Create App**.
3. Selecione:
   - **Scoped access**
   - Tipo de app:
     - **Full Dropbox** (acesso total)
     - **App folder** (apenas uma pasta específica)
4. Dê um **nome ao app** e clique em **Create App**.

---

## 2️⃣ Obter App Key e App Secret

1. Vá para a aba **Settings** do seu app.
2. Em **OAuth 2**, localize:
   - **App Key** → para usar no código.
   - **App Secret** → para usar no código.
3. Guarde-os com segurança.

---

## 3️⃣ Configure o APP Key em um arquivo .env



## 4️⃣ Executar o script de geração de tokens

1. Execute no terminal o script localizado na pasta **tools**:

```bash
python dropbox_pkce.py
```

2. Faça login e autorize o app no navegador.
3. Copie o **authorization code** da URL de redirecionamento e cole no terminal.
4. O script retornará:
   - **Access Token** (curta duração)
   - **Refresh Token** (longa duração, não expira até ser revogado)

---

## 5️⃣ Usar o Refresh Token para acessar arquivos

Crie um arquivo Python (`read_dropbox.py`) com:

```python
import requests
import dropbox
from dotenv import load_dotenv
import os

load_dotenv()

APP_KEY = os.getenv("APP_KEY")
APP_SECRET = os.getenv("APP_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

def get_access_token():
    url = "https://api.dropbox.com/oauth2/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "client_id": APP_KEY,
        "client_secret": APP_SECRET
    }
    r = requests.post(url, data=data)
    r.raise_for_status()
    return r.json()["access_token"]

ACCESS_TOKEN = get_access_token()
dbx = dropbox.Dropbox(ACCESS_TOKEN)

# Listar arquivos na pasta /eleicoes_bases
for entry in dbx.files_list_folder("/pasta").entries:
    print(entry.name)
```
**Obs: Configure o REFRESH_TOKEN, APP_KEY e APP_SECRET no arquivo .env**
> Com isso, você pode **acessar arquivos do Dropbox sem precisar autorizar toda vez**, usando o refresh token gerado.

