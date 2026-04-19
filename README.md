# Dark World RPG 🌑

**Dark World RPG** é um motor de jogo estilo Gacha e RPG de turnos desenvolvido em Python. Inspirado em mecânicas de jogos clássicos como Pokémon e sistemas de Gacha RPG, o projeto permite colecionar personagens, gerenciar suas habilidades e enfrentar desafios em um sistema de combate estratégico.

Embora tenha iniciado com o universo de **Jujutsu Kaisen** por escolha pessoal, o projeto foi arquitetado para ser um **multiverso aberto**, permitindo a inclusão de qualquer personagem ou criação autoral através de uma estrutura simples de banco de dados JSON.

---

## 🚀 Funcionalidades Atuais

- **Sistema de Gacha:** Sorteio de personagens baseado em probabilidades de raridade (R, SR, SSR).
- **Animação Dinâmica:** Suporte para GIFs animados através do processamento de frames com a biblioteca Pillow.
- **Banco de Dados Descentralizado:** Personagens, atributos e golpes são lidos de arquivos `.json`, facilitando a expansão sem mexer no código principal.
- **Interface Gráfica:** Desenvolvido com Pygame-CE para uma experiência visual fluida em janela independente.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** [Python 3.14+](https://www.python.org/)
* **Engine Gráfica:** [Pygame-CE](https://pygam-ce.org/)
* **Processamento de Imagem:** [Pillow (PIL)](https://python-pillow.org/)
* **Persistência de Dados:** JSON

## 📂 Estrutura do Projeto

```text
DarkWorldRPG/
├── assets/             # Imagens, GIFs e sons
├── data/               # Arquivos JSON (Personagens e Vilões)
├── src/
│   ├── models/         # Classes base (Character, Skills)
│   ├── systems/        # Lógica de Gacha, Animação e Combate
├── main.py             # Ponto de entrada do aplicativo
└── .gitignore          # Filtro de arquivos para o Git
```
## 🎮 Como Executar 

1. Clone este repositório:
```bash
git clone [https://github.com/Adrianzx01/dark-world-rpg.git](https://github.com/Adrianzx01/dark-world-rpg.git)
```
2. Instale as dependências necessárias:
```bash
pip install pygame-ce Pillow
```
3. Inicie o aplicativo:
```bash
python main.py
```
Desenvolvido por Adrian como um projeto pessoal.

