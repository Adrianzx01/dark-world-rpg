import random

class GachaSystem:
    def __init__(self, personagens):
        self.personagens = personagens
        self.chances = {
            "SSR": 5,   # 5%
            "SR": 25,   # 25%
            "R": 70     # 70%
        }

    def sumonar(self):
        sorteio_raridade = random.randint(1, 100)
        
        if sorteio_raridade <= self.chances["SSR"]:
            raridade_escolhida = "SSR"
        elif sorteio_raridade <= self.chances["SSR"] + self.chances["SR"]:
            raridade_escolhida = "SR"
        else:
            raridade_escolhida = "R"
            
        possiveis = [p for p in self.personagens if p.raridade == raridade_escolhida]
        
        if not possiveis:
            return random.choice(self.personagens)
            
        return random.choice(possiveis)