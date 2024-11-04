import pygame
from deck import Deck


class Entity:
    """
    Classe que representa uma entidade qualquer no jogo

    Atributos:
        defense (int): Valor da defesa da entidade, que reduz o dano recebido
        is_alive (bool): Indica se a entidade está viva
        current_life (int): Quantidade de pontos de vida atuais da entidade
        max_hp (int): Quantidade máxima de pontos de vida da entidade
        deck (Deck): Conjunto de cartas associado à entidade
        sprite (pygame.image): Sprite reprsentativo da entidade
        name (str): Nome da entidade
        energy (int): Quantidade energia disponivel para aplicar cartas
    """
    def __init__(self, max_hp: int, deck: Deck, name: str,
                  energy: int,x_pos:int,y_pos:int):
        self.defense = 0
        self.is_alive = True
        self.current_life = max_hp
        self.max_hp = max_hp
        self.deck = deck
        self.name = name

        img = pygame.image.load(f'./assests/{self.name}.png')
        self.sprite = pygame.transform.scale(img,(img.get_width()*2,img.get_height()*2))

        self.energy = energy
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.sprite.get_rect()
        self.rect.center = (self.x_pos,self.y_pos)
    def draw_entity(self,screen:pygame.display):
        screen.blit(self.sprite,self.rect)


class Enemy(Entity):
    """
    Classe que representa um inimigo no jogo - herda classe 'Entity'

    Atributos:
        drop_xp (int): Quantidade de experiência que o inimigo dropa na morte
    """
    def __init__(self, drop_xp: int,max_hp: int, deck: Deck, name: str,
                  energy: int,x_pos:int,y_pos:int):
        super().__init__(max_hp,deck,name,energy,x_pos,y_pos)
        self.drop_xp = drop_xp


class Ulisses(Entity):
    """
    Classe que representa o personagem principal - herdando da classe 'Entity'.

    Atributos:
        level (int): Nível atual do personagem
        xp (int): Experiência acumulada do personagem
        coins (int): Quantidade de moedas que o personagem possui
    """
    def __init__(self):
        super().__init__(max_hp=80,deck=Deck(),name="Ulisses",energy=3,x_pos = 80,y_pos = 400)
        self.level = 0
        self.xp = 0
        self.coins = 0
        
