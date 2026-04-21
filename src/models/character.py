import os
from systems.animator import GifAnimator

class Character:
    def __init__(self, data):
        self.nome = data.get('nome', 'Desconhecido')
        self.raridade = data.get('raridade', 'N/A') 
        self.hp = data.get('hp', 100)
        self.max_hp = self.hp
        self.energia = data.get('energia', 50)
        self.golpes = data.get('golpes', [])
        self.imagem_path = data.get('imagem_combate', '')
        self.animador = None
        self.superficie_imagem = None

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