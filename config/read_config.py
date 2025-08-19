import json
import os

def config_json():
    # Pega o diretório onde está este arquivo (config/)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    caminho_arquivo = os.path.join(base_dir, "config.json")

    with open(caminho_arquivo, mode="r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    return dados