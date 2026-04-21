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
    global estado_jogo, progressao, vilao_viva
    tela.fill((30, 0, 0)) 
    
    if vilao:
        txt_luta = FONTE_PRINCIPAL.render(f"DESAFIO: VS {vilao.nome}", True, BRANCO)
        tela.blit(txt_luta, (LARGURA//2 - txt_luta.get_width()//2, 20))
        # --- BARRA DE VIDA DO VILÃO ---
        largura_barra = 200
        altura_barra = 15
        x_barra = LARGURA//2 - largura_barra//2
        y_barra = 80 
        
        # Fundo da barra (Vermelho escuro/Preto)
        pygame.draw.rect(tela, (50, 0, 0), (x_barra, y_barra, largura_barra, altura_barra))
        
        # Barra de vida atual (Verde)
        # Cálculo: (HP Atual / HP Máximo) * Largura Total
        porcentagem_vida = vilao.hp / vilao.max_hp
        pygame.draw.rect(tela, (0, 255, 0), (x_barra, y_barra, largura_barra * porcentagem_vida, altura_barra))
        
        # Borda da barra
        pygame.draw.rect(tela, BRANCO, (x_barra, y_barra, largura_barra, altura_barra), 2)
        
        # Texto do HP
        txt_hp = FONTE_PEQUENA.render(f"{vilao.hp} / {vilao.max_hp}", True, BRANCO)
        tela.blit(txt_hp, (x_barra + largura_barra//2 - txt_hp.get_width()//2, y_barra - 20))

        # Checa vitória
        if vilao.hp <= 0:
            txt_vitoria = FONTE_PRINCIPAL.render("VITÓRIA!", True, DOURADO)
            tela.blit(txt_vitoria, (LARGURA//2 - txt_vitoria.get_width()//2, LARGURA//2))
            
            # Se apertar ESPAÇO, vai para o próximo nível
            aviso_v = FONTE_PEQUENA.render("Pressione ESPAÇO para o Próximo Desafio", True, BRANCO)
            tela.blit(aviso_v, (LARGURA//2 - aviso_v.get_width()//2, LARGURA//2 + 50))
            
            for evento in eventos:
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    progressao.proximo_nivel()
                    # Atualiza a variável local para o novo vilão (Sukuna!)
                    vilao_viva = progressao.obter_vilão_atual()
        
        # Carrega se for a primeira vez
        if not vilao.animador or len(vilao.animador.frames) == 0:
             vilao.carregar_imagem(250)
        
        vilao.update_animation() 
        frame_vilao = vilao.get_frame_for_drawing()
        if frame_vilao:
            pos_v = LARGURA//2 - frame_vilao.get_width()//2
            tela.blit(frame_vilao, (pos_v, 100))

    # Exibir sua equipe
    y_equipe = 420
    for i, p in enumerate(equipe):
        txt_p = FONTE_PEQUENA.render(f"{i+1}. {p.nome} (HP: {p.hp})", True, BRANCO)
        tela.blit(txt_p, (50, y_equipe + (i * 30)))
# --- INTERFACE DE ATAQUE ---
    txt_instrucao = FONTE_PEQUENA.render("Aperte o número do herói para atacar:", True, BRANCO)
    tela.blit(txt_instrucao, (50, 380))

    for evento in eventos:
        if evento.type == pygame.KEYDOWN:
            # Se apertar 1, o primeiro herói ataca, se 2 o segundo...
            indices_teclas = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]
            
            for i, tecla in enumerate(indices_teclas):
                if evento.key == tecla and i < len(equipe):
                    heroi = equipe[i]
                    # Calcular dano 
                    dano = 50 
                    vilao.hp -= dano
                    print(f"{heroi.nome} atacou! Dano: {dano}")
                    
                    # Garante que o HP não fique negativo
                    if vilao.hp < 0:
                        vilao.hp = 0
    # Botão de fugir
    voltar = FONTE_PEQUENA.render("Pressione [M] para Fugir", True, (180, 180, 180))
    tela.blit(voltar, (LARGURA - 220, 560))

    # Captura de teclado para a batalha
    for evento in eventos:
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_m:
                estado_jogo = "MENU" 

def jogo():
    global estado_jogo, inventario, progressao, vilao_viva
    clock = pygame.time.Clock()
    personagens_db = carregar_personagens()
    gacha = GachaSystem(personagens_db)
    progressao = ProgressionSystem()
    
    vilao_viva = progressao.obter_vilão_atual()

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