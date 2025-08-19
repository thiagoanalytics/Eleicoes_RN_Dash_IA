import secrets
import base64
import hashlib
import requests
import webbrowser
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
# ==========================
# CONFIGURAÇÕES DO APP
# ==========================
APP_KEY = os.getenv('APP_KEY') # coloque aqui a App Key do seu app
REDIRECT_URI = "https://localhost"  # URI de redirecionamento (pode ser localhost se for desktop)

# ==========================
# 1️⃣ Gerar code_verifier e code_challenge
# ==========================
code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(64)).rstrip(b'=').decode('utf-8')

code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).rstrip(b'=').decode('utf-8')

print("Code Verifier:", code_verifier)
print("Code Challenge:", code_challenge)

# ==========================
# 2️⃣ Gerar URL de autorização
# ==========================
auth_url = (
    f"https://www.dropbox.com/oauth2/authorize"
    f"?client_id={APP_KEY}"
    f"&response_type=code"
    f"&code_challenge={code_challenge}"
    f"&code_challenge_method=S256"
    f"&token_access_type=offline"
)

print("\nAbra esta URL no navegador e autorize o app:")
print(auth_url)

# opcional: abrir automaticamente
webbrowser.open(auth_url)

# ==========================
# 3️⃣ Inserir authorization code retornado
# ==========================
auth_code = input("\nCole aqui o code que apareceu na URL de redirecionamento: ")

# ==========================
# 4️⃣ Trocar authorization code por refresh token
# ==========================
token_url = "https://api.dropboxapi.com/oauth2/token"

data = {
    "code": auth_code,
    "grant_type": "authorization_code",
    "client_id": APP_KEY,
    "code_verifier": code_verifier,
    "redirect_uri": REDIRECT_URI
}

response = requests.post(token_url, data=data)
response.raise_for_status()

tokens = response.json()
print("\n✅ Tokens gerados com sucesso:")
print("Access Token:", tokens.get("access_token"))
print("Refresh Token:", tokens.get("refresh_token"))
print("Expires in (s):", tokens.get("expires_in"))
