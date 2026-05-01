import pygame
import sys
import os

# Ajuste de caminho para os módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from systems.loader import carregar_personagens
from systems.gacha import GachaSystem
from systems.progression import ProgressionSystem

# Inicialização Global
pygame.init()
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Dark World RPG")

# Cores e Fontes
PRETO = (20, 20, 20)
BRANCO = (255, 255, 255)
DOURADO = (255, 215, 0)
CINZA = (150, 150, 150)
FONTE_PRINCIPAL = pygame.font.SysFont("Arial", 32, bold=True)
FONTE_PEQUENA = pygame.font.SysFont("Arial", 20)

# Variáveis de Estado Globais
inventario = []
equipe_atual = []
progressao = None
vilao_viva = None
estado_jogo = "MENU" # Estados: MENU, GACHA, EQUIPE, BATALHA
personagem_sorteado = None
carregar_nova_imagem = False
cursor_inventario = 0
animacao_ataque_ativa = None
tempo_animacao_ataque = 0

# --- FUNÇÕES DE TELA ---

def desenhar_menu(eventos):
    global estado_jogo
    tela.fill(PRETO)
    
    titulo = FONTE_PRINCIPAL.render("DARK WORLD RPG", True, DOURADO)
    tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 100))
    
    # Instruções do Menu
    txt1 = FONTE_PEQUENA.render("Pressione [G] para entrar no Gacha", True, BRANCO)
    txt2 = FONTE_PEQUENA.render("Pressione [E] para ver Equipe/Inventário", True, BRANCO)
    tela.blit(txt1, (LARGURA//2 - txt1.get_width()//2, 300))
    tela.blit(txt2, (LARGURA//2 - txt2.get_width()//2, 350))

    for evento in eventos:
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_g:
                estado_jogo = "GACHA"
            if evento.key == pygame.K_e:
                estado_jogo = "EQUIPE"

def desenhar_gacha(eventos, gacha):
    global estado_jogo, personagem_sorteado, carregar_nova_imagem, inventario
    tela.fill(PRETO)
    
    txt_voltar = FONTE_PEQUENA.render("Pressione [M] para Voltar ao Menu", True, CINZA)
    tela.blit(txt_voltar, (20, 20))
    
    titulo = FONTE_PRINCIPAL.render("SISTEMA DE SUMMON", True, BRANCO)
    tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 50))

    # Eventos do Gacha
    for evento in eventos:
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_m:
                estado_jogo = "MENU"
            if evento.key == pygame.K_SPACE:
                personagem_sorteado = gacha.sumonar()
                carregar_nova_imagem = True
                # Adiciona ao inventário
                inventario.append(personagem_sorteado)
                print(f"Adicionado ao inventário: {personagem_sorteado.nome}. Total: {len(inventario)}")

    # Desenho do Personagem Sorteado
    if personagem_sorteado:
        if carregar_nova_imagem:
            personagem_sorteado.carregar_imagem(250)
            carregar_nova_imagem = False
        
        personagem_sorteado.update_animation()
        frame = personagem_sorteado.get_frame_for_drawing()
        
        if frame:
            pos_x = LARGURA//2 - frame.get_width()//2
            tela.blit(frame, (pos_x, 150))
            y_texto = 150 + frame.get_height() + 20
        else:
            y_texto = 300

        nome = FONTE_PRINCIPAL.render(f"{personagem_sorteado.nome}", True, BRANCO)
        raro = FONTE_PRINCIPAL.render(f"GRAU: {personagem_sorteado.raridade}", True, DOURADO)
        tela.blit(nome, (LARGURA//2 - nome.get_width()//2, y_texto))
        tela.blit(raro, (LARGURA//2 - raro.get_width()//2, y_texto + 40))

    instr = FONTE_PEQUENA.render("Pressione ESPAÇO para Sumonar", True, CINZA)
    tela.blit(instr, (LARGURA//2 - instr.get_width()//2, 530))

def desenhar_equipe(eventos):
    global estado_jogo, inventario, equipe_atual, cursor_inventario
    tela.fill(PRETO)
    
    titulo = FONTE_PRINCIPAL.render("ESCOLHA SUA EQUIPE (MÁX 4)", True, DOURADO)
    tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 30))

    instr = FONTE_PEQUENA.render("[Setas] Navegar | [Espaço] Selecionar/Remover | [B] Lutar", True, CINZA)
    tela.blit(instr, (LARGURA//2 - instr.get_width()//2, 80))  

    # Listar personagens do inventário
    y_lista = 130
    for i, p in enumerate(inventario):
        cor = BRANCO
        prefixo = "[ ]"
        
        # Destaca onde o cursor está
        if i == cursor_inventario:
            cor = DOURADO
            prefixo = "> [ ]"
            
        # Marca se o personagem já está na equipe
        if p in equipe_atual:
            prefixo = prefixo.replace("[ ]", "[X]")
            cor = (0, 255, 0) # Verde se selecionado

        txt = FONTE_PEQUENA.render(f"{prefixo} {p.nome} ({p.raridade})", True, cor)
        tela.blit(txt, (50, y_lista))
        y_lista += 30

    # Exibir Equipe Atual 
    txt_equipe = FONTE_PRINCIPAL.render(f"EQUIPE: {len(equipe_atual)}/4", True, BRANCO)
    tela.blit(txt_equipe, (500, 130))
    
    for i, p in enumerate(equipe_atual):
        txt_p = FONTE_PEQUENA.render(f"{i+1}. {p.nome}", True, DOURADO)
        tela.blit(txt_p, (500, 180 + (i * 30)))

    # Lógica de Eventos
    for evento in eventos:
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_m:
                estado_jogo = "MENU"
            
            # Navegação
            if evento.key == pygame.K_UP:
                cursor_inventario = max(0, cursor_inventario - 1)
            if evento.key == pygame.K_DOWN:
                cursor_inventario = min(len(inventario) - 1, cursor_inventario + 1)
            
            # Seleção
            if evento.key == pygame.K_SPACE:
                p_escolhido = inventario[cursor_inventario]
                if p_escolhido in equipe_atual:
                    equipe_atual.remove(p_escolhido)
                elif len(equipe_atual) < 4:
                    equipe_atual.append(p_escolhido)
            
            # Ir para Batalha
            if evento.key == pygame.K_b and len(equipe_atual) > 0:
                estado_jogo = "BATALHA"

def desenhar_batalha(eventos, equipe, vilao):
    global estado_jogo, progressao, vilao_viva, animacao_ataque_ativa, tempo_animacao_ataque
    
    # 1. Fundo
    tela.fill((20, 20, 25))

    if vilao:
        # --- DESENHAR VILÃO E VIDA ---
        txt_luta = FONTE_PRINCIPAL.render(f"DESAFIO: VS {vilao.nome}", True, BRANCO)
        tela.blit(txt_luta, (LARGURA//2 - txt_luta.get_width()//2, 20))

        vilao.update_animation()
        frame_v = vilao.get_frame_for_drawing()
        if frame_v:
            tela.blit(frame_v, (LARGURA//2 - frame_v.get_width()//2, 100))

        # Barra de Vida do Vilão
        pygame.draw.rect(tela, (50, 0, 0), (LARGURA//2 - 100, 80, 200, 15))
        porcentagem_v = max(0, vilao.hp / vilao.max_hp)
        pygame.draw.rect(tela, (0, 255, 0), (LARGURA//2 - 100, 80, 200 * porcentagem_v, 15))
        pygame.draw.rect(tela, BRANCO, (LARGURA//2 - 100, 80, 200, 15), 2)

        # --- DESENHAR EQUIPE (HP E ENERGIA) ---
        for i, p in enumerate(equipe):
            y_pos = 400 + (i * 60)
            txt_p = FONTE_PEQUENA.render(f"{p.nome} (HP: {p.hp})", True, BRANCO)
            tela.blit(txt_p, (50, y_pos))
            
            # Barra de Energia Amaldiçoada (CE)
            pygame.draw.rect(tela, (30, 30, 40), (50, y_pos + 25, 150, 8))
            porcentagem_ce = p.energia / p.max_energia
            pygame.draw.rect(tela, (0, 150, 255), (50, y_pos + 25, 150 * porcentagem_ce, 8))

        # --- MENU DE GOLPES (Focado no Heroi 1 - Gojo) ---
        heroi_ativo = equipe[0]
        painel = pygame.Rect(300, 390, 470, 180)
        pygame.draw.rect(tela, (10, 10, 15), painel, border_radius=10)
        pygame.draw.rect(tela, DOURADO, painel, 2, border_radius=10)

        for idx, golpe in enumerate(heroi_ativo.golpes):
            cor = BRANCO if heroi_ativo.energia >= golpe['custo'] else (100, 100, 100)
            txt_g = FONTE_PEQUENA.render(f"{idx+1}. {golpe['nome']} ({golpe['custo']} CE)", True, cor)
            tela.blit(txt_g, (320, 420 + (idx * 30)))

        # --- LÓGICA DE EVENTOS ---
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_m: estado_jogo = "MENU"
                
                if vilao.hp <= 0 and evento.key == pygame.K_SPACE:
                    progressao.proximo_nivel()
                    vilao_viva = progressao.obter_vilão_atual()
                    if vilao_viva:
                        vilao_viva.carregar_imagem(250)
                
                elif vilao.hp > 0:
                    teclas = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]
                    for idx, tecla in enumerate(teclas):
                        if evento.key == tecla and idx < len(heroi_ativo.golpes):
                            golpe = heroi_ativo.golpes[idx]
                            if heroi_ativo.energia >= golpe['custo']:
                                # Atacar
                                heroi_ativo.energia -= golpe['custo']
                                vilao.hp -= golpe['dano']
                                heroi_ativo.recuperar_energia()
                                
                                # Ativar Animação
                                if 'animacao' in golpe:
                                    from systems.animator import GifAnimator
                                    path = os.path.join(os.getcwd(), golpe['animacao'])
                                    animacao_ataque_ativa = GifAnimator(path, 450)
                                    tempo_animacao_ataque = 300 # 5 segundos

        # --- DESENHAR ANIMAÇÃO DE ATAQUE ---
        if animacao_ataque_ativa and tempo_animacao_ataque > 0:
            animacao_ataque_ativa.update()
            f_skill = animacao_ataque_ativa.get_current_frame()
            if f_skill:
                tela.blit(f_skill, (LARGURA//2 - f_skill.get_width()//2, 100))
            tempo_animacao_ataque -= 1
        else:
            animacao_ataque_ativa = None

        # --- VITÓRIA ---
        if vilao.hp <= 0:
            txt_v = FONTE_PRINCIPAL.render("VITÓRIA!", True, DOURADO)
            tela.blit(txt_v, (LARGURA//2 - txt_v.get_width()//2, 250))
            txt_s = FONTE_PEQUENA.render("Pressione ESPAÇO para o próximo", True, BRANCO)
            tela.blit(txt_s, (LARGURA//2 - txt_s.get_width()//2, 320))

def jogo():
    global estado_jogo, inventario, progressao, vilao_viva
    clock = pygame.time.Clock()
    personagens_db = carregar_personagens()
    gacha = GachaSystem(personagens_db)
    progressao = ProgressionSystem()
    
    vilao_viva = progressao.obter_vilão_atual()
    if vilao_viva:
        vilao_viva.carregar_imagem(250)

    rostando = True
    while rostando:
        # 1. PEGAR EVENTOS UMA ÚNICA VEZ
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                rostando = False

        # 2. GERENCIAR TELAS 
        if estado_jogo == "MENU":
            desenhar_menu(eventos)
        elif estado_jogo == "GACHA":
            desenhar_gacha(eventos, gacha)
        elif estado_jogo == "EQUIPE":
            desenhar_equipe(eventos)
        elif estado_jogo == "BATALHA":
            desenhar_batalha(eventos, equipe_atual, vilao_viva)

        # 3. ATUALIZAR A TELA 
        pygame.display.flip()
        clock.tick(60) 

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    jogo()