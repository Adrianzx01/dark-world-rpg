import pygame
from PIL import Image, ImageSequence

class GifAnimator:
    def __init__(self, caminho_gif, largura_desejada=200):
        self.frames = []
        self.frame_index = 0
        self.last_update_time = pygame.time.get_ticks()
        self.velocidade = 100 

        try:
            pil_image = Image.open(caminho_gif)
            
            if 'duration' in pil_image.info:
                self.velocidade = pil_image.info['duration']
                if self.velocidade < 20: self.velocidade = 100

            print(f"DEBUG Animator: Carregando GIF {caminho_gif} com {pil_image.n_frames} frames a {self.velocidade}ms.")

            for frame in ImageSequence.Iterator(pil_image):
                frame_rgba = frame.convert('RGBA')
                frame_data = frame_rgba.tobytes()
                frame_size = frame_rgba.size
                
                pygame_frame = pygame.image.fromstring(frame_data, frame_size, 'RGBA')
                
                proporcao = largura_desejada / pygame_frame.get_width()
                altura_desejada = int(pygame_frame.get_height() * proporcao)
                scaled_frame = pygame.transform.smoothscale(pygame_frame, (largura_desejada, altura_desejada))
                
                self.frames.append(scaled_frame)
                
            pil_image.close() 
            
        except Exception as e:
            print(f"ERRO Animator: Falha ao processar GIF {caminho_gif}. Motivo: {e}")
            self.frames = [] 

    def get_current_frame(self):
        """Retorna o frame atual para ser desenhado"""
        if not self.frames: return None
        return self.frames[self.frame_index]

    def update(self):
        """Lógica para trocar o frame baseado no tempo (velocidade)"""
        if len(self.frames) <= 1: return 

        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_update_time > self.velocidade:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.last_update_time = current_time