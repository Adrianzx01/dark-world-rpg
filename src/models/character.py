import os
from systems.animator import GifAnimator

class Character:
    def __init__(self, data):
        # Dados Básicos
        self.nome = data.get('nome', 'Desconhecido')
        self.raridade = data.get('raridade', 'N/A')
        
        # Atributos de Vida
        self.hp = data.get('hp', 100)
        self.max_hp = data.get('max_hp', self.hp)
        
        # Atributos de Energia Amaldiçoada
        self.energia = data.get('energia', 50)
        self.max_energia = data.get('max_energia', self.energia)
        
        # Lista de Golpes (carregada do JSON)
        self.golpes = data.get('golpes', [])
        
        # Sistema de Animação
        self.imagem_path = data.get('imagem_combate', '')
        self.animador = None
        self.superficie_imagem = None
        
        # Sistema de Status (Stun)
        self.stun_turnos = 0

    def carregar_imagem(self, largura_desejada=200):
        if not self.imagem_path:
            return
        
        # Usa o caminho absoluto para evitar erros de diretório
        caminho_absoluto = os.path.join(os.getcwd(), self.imagem_path)
        self.animador = GifAnimator(caminho_absoluto, largura_desejada)

    def update_animation(self):
        if self.animador:
            self.animador.update()

    def get_frame_for_drawing(self):
        if self.animador:
            return self.animador.get_current_frame()
        return None

    def recuperar_energia(self):
        """Recupera energia após o ataque com base na raridade."""
        bonus = 0
        if self.raridade == "SSR":
            bonus = 100
        elif self.raridade == "SR":
            bonus = 50
            
        self.energia = min(self.max_energia, self.energia + bonus)
        print(f"DEBUG: {self.nome} ({self.raridade}) recuperou {bonus} de energia. Atual: {self.energia}")

    def esta_stunado(self):
        """Verifica se o personagem está impedido de agir."""
        return self.stun_turnos > 0

    def mostrar_status(self):
        """Imprime o status no terminal para debug."""
        print(f"--- {self.nome} ({self.raridade}) ---")
        print(f"HP: {self.hp}/{self.max_hp}")
        print(f"Energia: {self.energia}/{self.max_energia}")
        if self.esta_stunado():
            print(f"STATUS: STUNADO ({self.stun_turnos} turnos)")
        print("-" * 20)

    def esta_vivo(self):
        """Retorna True se o HP for maior que 0."""
        return self.hp > 0