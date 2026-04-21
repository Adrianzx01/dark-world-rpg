import json
import os
from models.character import Character

class ProgressionSystem:
    def __init__(self):
        self.viloes_dados = self.carregar_viloes()
        self.indice_atual = 0
        self.vilao_instanciado = None # Guarda o vilão atual aqui

    def carregar_viloes(self):
        caminho = os.path.join('data', 'villains.json')
        with open(caminho, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            return sorted(dados, key=lambda v: v['hp'])

    def obter_vilão_atual(self):
        if self.indice_atual < len(self.viloes_dados):
           
            if not hasattr(self, 'vilao_instanciado') or self.vilao_instanciado is None:
                self.vilao_instanciado = Character(self.viloes_dados[self.indice_atual])
            return self.vilao_instanciado
        return None

    def proximo_nivel(self):
        self.indice_atual += 1
        self.vilao_instanciado = None 