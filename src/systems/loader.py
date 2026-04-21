import json
import os
from models.character import Character

def carregar_personagens():
    caminho_arquivo = os.path.join('data', 'characters.json')
    
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            return [Character(d) for d in dados]
    except FileNotFoundError:
        print("Erro: O arquivo characters.json não foi encontrado!")
        return []