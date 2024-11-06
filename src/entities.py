import pygame
from deck import Deck
import json

with open(file='./assets/enemies.json',mode='r') as enemy_config:
    default_entity_configurations = json.load(enemy_config)

class Entity:
    """
    Classe que representa uma entidade qualquer no jogo, dentre as possibilidades estabelecidas.

    Atributos
    ----------
        defense: int
            Valor da defesa da entidade, que reduz o dano recebido.
        is_alive : bool
            Indica se a entidade está viva.
        current_life : int
            Quantidade de pontos de vida atuais da entidade
        max_hp : int
            Quantidade máxima de pontos de vida da entidade
        deck : Deck
            Conjunto de cartas associado à entidade
        sprite : pygame.image
            Sprite reprsentativo da entidade
        name : str
            Nome da entidade
        energy : int
            Quantidade energia disponivel para aplicar cartas
    """
    def __init__(self,name:str,x_pos:int,y_pos:int):
        try:
            entity_info = default_entity_configurations['entities'][name]
            self.defense = 0
            self.is_alive = True
            self.current_life = entity_info['max_hp']
            self.max_hp = entity_info['max_hp']
            self.deck = Deck(draw_pile=entity_info['draw_pile'])
            self.name = name

            img = pygame.image.load(f'./assets/{self.name}.png')
            self.sprite = pygame.transform.scale(img,(150,150)) # fixa as dimensões de todas as entidades em quadrados de 150x150

            self.energy = entity_info['energy']
            self.x_pos = x_pos
            self.y_pos = y_pos
            self.rect = self.sprite.get_rect()
            self.deck.set_owner(self) # definimos o dono do deck como a porpria entidade
        except FileNotFoundError as error:
            print(f"{error}: assest of name {self.name} was not found in folder 'assets'")

    def draw_entity(self,screen:pygame.display):
        """
       Função que desenha uma entidade qualquer do jogo, por meio do método screen.blit.

        Parâmetros 
        ----------
        screen : pygame.display
            Display do jogo
        """
        self.rect.center = (self.x_pos,self.y_pos)
        screen.blit(self.sprite,self.rect)
        self.draw_health_bar(screen)

    def draw_health_bar(self,screen:pygame.display):
        entity_left_corner_x_pos = self.x_pos-75
        entity_left_corner_y_pos = self.y_pos-75


        health_bar_size = 100 * (self.current_life/self.max_hp)

        # deslocamento nas posições x e y para dar margem ao sprite
        health_bar_bg_rect = pygame.Rect(entity_left_corner_x_pos+25,entity_left_corner_y_pos-15,100,20)
        health_bar_rect = pygame.Rect(entity_left_corner_x_pos+25,entity_left_corner_y_pos-15,health_bar_size,20)

        pygame.draw.rect(screen,'grey',health_bar_bg_rect)
        pygame.draw.rect(screen,'red',health_bar_rect)


class Enemy(Entity):
    """
    Classe que representa um inimigo no jogo - herda classe 'Entity'

    Atributos
    ---------
        drop_xp : int
            Quantidade de experiência que o inimigo dropa na morte
    """
    def __init__(self, name:str):
        entity_info = default_entity_configurations['entities'][name]
        super().__init__(name=name,
                         x_pos=700,
                         y_pos=375)
        self.drop_xp = entity_info['drop_xp']


class Ulisses(Entity):
    """
    Classe que representa o personagem principal - herdando da classe 'Entity'.

    Atributos
    ---------
        level : int
            Nível atual do personagem
        xp : int
            Experiência acumulada do personagem
        coins : int
            Quantidade de moedas que o personagem possui
    """
    def __init__(self):
        super().__init__(name="Ulisses",x_pos = 80,y_pos = 375)
        self.level = 0
        self.xp = 0
        self.coins = 0
        
