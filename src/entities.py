from pathlib import Path
import pygame
from deck import Deck
import json

game_dir = Path(__file__).parent.parent
entities_json_path = game_dir / "assets" / "entities.json"

with open(file=entities_json_path,mode='r') as enemy_config:
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
        max_energy : int
            Quantidade energia maximo para aplicar cartas
        current_energy : int
            Quantidade energia disponivel para aplicar cartas
    """
    def __init__(self,name:str,x_pos:int,y_pos:int):
        try:
            entity_info = default_entity_configurations['entities'][name]
            self.defense = 0
            self.is_alive = True
            self.current_life = entity_info['max_hp']
            self.max_hp = entity_info['max_hp']
            self.deck = Deck(draw_pile_ids=entity_info['draw_pile']) 
            self.name = name

            img_path = game_dir / "assets" / f"{self.name}.png"
            img = pygame.image.load(img_path)
            self.sprite = pygame.transform.scale(img,(150,150)) # fixa as dimensões de todas as entidades em quadrados de 150x150

            self.max_energy = entity_info['max_energy']
            self.current_energy = entity_info['max_energy']
            self.x_pos = x_pos
            self.y_pos = y_pos
            self.rect = self.sprite.get_rect()
            self.deck.set_owner(self) # definimos o dono do deck como a porpria entidade
        except FileNotFoundError as error:
            print(f"{error}: assest of name {self.name} was not found in folder 'assets'")
    def __str__(self):
        return f"name:{self.name}\ndeck:{self.deck.__str__()}\nenergy:{self.current_energy}/{self.max_energy}"
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
        self.draw_status_bar(screen)

    def draw_status_bar(self,screen:pygame.display):

        entity_left_corner_x_pos = self.x_pos-75
        entity_left_corner_y_pos = self.y_pos-75

        text_font = pygame.font.SysFont('Arial',18)
        hp_text_img = text_font.render(f'{self.current_life}/{self.max_hp}',True,'white')
        defnse_text_img = text_font.render(f'{self.defense}',True,'white')
        health_bar_size = 100 * (self.current_life/self.max_hp)
        # deslocamento nas posições x e y para dar margem ao sprite
        defense_status_rect = pygame.Rect(entity_left_corner_x_pos+110,entity_left_corner_y_pos-15,30,20)
        health_bar_bg_rect = pygame.Rect(entity_left_corner_x_pos+10,entity_left_corner_y_pos-15,100,20)
        health_bar_rect = pygame.Rect(entity_left_corner_x_pos+10,entity_left_corner_y_pos-15,health_bar_size,20)

        pygame.draw.rect(screen,'grey',health_bar_bg_rect)
        pygame.draw.rect(screen,'red',health_bar_rect)
        pygame.draw.rect(screen,'blue',defense_status_rect)

        screen.blit(hp_text_img,(entity_left_corner_x_pos+10,entity_left_corner_y_pos-15))
        screen.blit(defnse_text_img,(entity_left_corner_x_pos+110,entity_left_corner_y_pos-15))


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

    def enemy_attack_animation(self):
        self.x_pos -= 100
        #TODO achar um jeito de voltar pra posição inicial de forma mais suave

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
        health_regain : int
            Quantidade de vida ganha ao terminar um combate
    """
    def __init__(self):
        super().__init__(name="Ulisses",x_pos = 80,y_pos = 375)
        self.level = 0
        self.xp = 0
        self.coins = 0
        self.health_regain = 8

    def ulisses_attack_animation(self):
        self.x_pos += 100
        #TODO achar um jeito de voltar pra posiçao inicial de forma mais suave