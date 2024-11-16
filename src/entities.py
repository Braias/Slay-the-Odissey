from pathlib import Path
import pygame
from deck import Deck
import json
from abc import ABC, abstractmethod
import copy

game_dir = Path(__file__).parent.parent
entities_json_path = game_dir / "assets" / "entities.json"

with open(file=entities_json_path,mode='r') as enemy_config:
    default_entity_configurations = json.load(enemy_config)

class Entity(ABC):
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
            self.max_defense = 50
            self.current_defense = 0
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
    
    def __draw_status_rectangle(self,screen:pygame.display,background_width:int,height:int,dyanamic_bar_size:int,
                                x:int,y:int, primary_color:str, bg_color:str):
        
        pygame.draw.rect(screen,bg_color, pygame.Rect(x, y, background_width, height))
        pygame.draw.rect(screen, primary_color, pygame.Rect(x, y, dyanamic_bar_size, height))

    def draw_status_bar(self, screen: pygame.display):
        # Coordenadas Base e dimensoes para retangulos - deslocados para canto esquero do personagem
        x, y = self.x_pos - 75, self.y_pos - 75
        background_width = 100

        # Rendereizando fonte e calculando tamanho de cada barra
        hp_text_img = pygame.font.SysFont('Arial', 18).render(f'{self.current_life}/{self.max_hp}', True, 'white')
        health_bar_size = background_width * (self.current_life / self.max_hp)
        defense_bar_size = background_width * (self.current_defense / self.max_defense)

        self.__draw_status_rectangle(screen, background_width, 20, health_bar_size,  x + 25, y - 23, 'red', 'grey')
        self.__draw_status_rectangle(screen, background_width,  5, defense_bar_size, x + 25, y, 'blue', 'gray')

        # Desenhar texto indicador de vida atual
        screen.blit(hp_text_img, (x + 25, y - 23))

    def hit_animate(self):
        #hit_duration = 
        pass
    def defense_animate(self):
        pass

    def death_animate(self):
            img_path = game_dir / "assets" / "death" / f"RIP.png"
            img = pygame.image.load(img_path)
            self.sprite = pygame.transform.scale(img,(150,150)) 
    @abstractmethod
    def attack_animate(self):...
    

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

    def attack_animate(self):
        pass
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
        self.speed = 50
        self.deck.shuffle_and_allocate()

    def attack_animate(self):
        self.x_pos += 100
        attacking = True
        backing = False
        attack_distance = 100
        original_x = copy.deepcopy(self.x_pos)
        while attacking:
            print("atacando")
            self.x_pos += self.speed
            if self.x_pos - original_x >= attack_distance:
                print("parei de atacar")
                attacking = False
                backing = True
        while backing:
            print("voltando")
            self.x_pos -= self.speed
            if self.x_pos - original_x <= 0:
                print("parei de voltar")
                backing = False
        




    def draw_status_bar(self,screen:pygame.display):
        super().draw_status_bar(screen)
        energy_text_img = pygame.font.SysFont('Arial', 34).render(f'{self.current_energy}', True, 'white')
        pygame.draw.circle(screen,pygame.Color('#3dad62'),(75,500),20)
        screen.blit(energy_text_img,(65,480))

    def insufficient_energy_animate(self):
        pass
