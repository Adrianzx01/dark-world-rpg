import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from systems.loader import carregar_personagens
from systems.gacha import GachaSystem

pygame.init()

# Configurações da Janela
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Mundo Sombrio: Jujutsu Gacha")

# Cores
PRETO = (20, 20, 20)
BRANCO = (255, 255, 255)
DOURADO = (255, 215, 0)

def jogo():
    clock = pygame.time.Clock()
    
    # Carrega os dados e o sistema de sorteio
    personagens = carregar_personagens()
    gacha = GachaSystem(personagens)
    
    personagem_sorteado = None
    rostando = True

    # Fonte para o texto
    fonte = pygame.font.SysFont("Arial", 32, bold=True)

    carregar_nova_imagem = False

    while rostando:
        # 1. Escutar Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rostando = False
            
            # Quando apertar ESPAÇO, faz o sumon
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    personagem_sorteado = gacha.sumonar()
                    carregar_nova_imagem = True

        # 2. Desenhar
        tela.fill(PRETO)
        
        # Título
        txt_titulo = fonte.render("MUNDO SOMBRIO: GACHA", True, BRANCO)
        tela.blit(txt_titulo, (LARGURA//2 - txt_titulo.get_width()//2, 30))

        # Instrução
        txt_instr = fonte.render("Pressione ESPAÇO para Sumonar", True, (150, 150, 150))
        tela.blit(txt_instr, (LARGURA//2 - txt_instr.get_width()//2, 500))

        # Mostrar Resultado do Gacha
        # Lógica de Carregamento e DESENHO ANIMADO
        if personagem_sorteado:
            # 1. Carrega o GIF na primeira vez
            if carregar_nova_imagem:
                personagem_sorteado.carregar_imagem(250) 
                carregar_nova_imagem = False

            # 2. Atualiza a animação
            if hasattr(personagem_sorteado, 'update_animation'):
                personagem_sorteado.update_animation()

            # 3. Pega o frame atual
            frame_atual = personagem_sorteado.get_frame_for_drawing()

            # 4. Desenha se o frame existir
            if frame_atual:
                pos_x = LARGURA//2 - frame_atual.get_width()//2
                pos_y = 150 
                tela.blit(frame_atual, (pos_x, pos_y))
                
                txt_y_offset = pos_y + frame_atual.get_height() + 20
            else:
                # Caso a imagem falhe, define um offset padrão para o texto não sumir
                txt_y_offset = 300

            # 5. Desenha os textos usando o novo offset
            txt_nome = fonte.render(f"FEITICEIRO: {personagem_sorteado.nome}", True, BRANCO)
            tela.blit(txt_nome, (LARGURA//2 - txt_nome.get_width()//2, txt_y_offset))
            
            txt_raro = fonte.render(f"GRAU: {personagem_sorteado.raridade}", True, DOURADO)
            tela.blit(txt_raro, (LARGURA//2 - txt_raro.get_width()//2, txt_y_offset + 40))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    jogo()