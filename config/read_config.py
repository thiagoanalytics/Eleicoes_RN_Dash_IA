import json


def config_json():
    caminho_arquivo = "config/config.json"
    # Usa o gerenciador de contexto `with` para abrir o arquivo
    with open(caminho_arquivo, mode='r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)

    return dados