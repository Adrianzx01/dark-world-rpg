import os
from systems.animator import GifAnimator

class Character:
    def __init__(self, data):
        self.id = data['id']
        self.nome = data['nome']
        self.raridade = data['raridade']
        self.imagem_path = data.get('imagem_combate', '')
        self.hp_max = data['hp']
        self.hp_atual = data['hp']
        self.energia_max = data['energia']
        self.energia_atual = data['energia']
        self.golpes = data['golpes']
        self.superficie_imagem = None
        self.animador = None

    def carregar_imagem(self, largura_desejada=200):
        if not self.imagem_path:
            return
        caminho_absoluto = os.path.join(os.getcwd(), self.imagem_path)
        self.animador = GifAnimator(caminho_absoluto, largura_desejada)

    def update_animation(self):
            if self.animador:
                self.animador.update()
        
    def get_frame_for_drawing(self):
            if self.animador:
                return self.animador.get_current_frame()
            return None
    def mostrar_status(self):
        print(f"--- {self.nome} ({self.raridade}) ---")
        print(f"HP: {self.hp_atual}/{self.hp_max}")
        print(f"Energia: {self.energia_atual}/{self.energia_max}")
        print("-" * 20)

    def esta_vivo(self):
        return self.hp_atual > 0