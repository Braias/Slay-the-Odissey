from pathlib import Path
import pygame
from deck import Deck
import json
from enum import Enum

game_dir = Path(__file__).parent.parent
entities_json_path = game_dir / "assets" / "entities.json"

with open(file=entities_json_path,mode='r') as enemy_config:
    default_entity_configurations = json.load(enemy_config)

class Entity():
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
            self.current_life = entity_info['max_hp']
            self.max_hp = entity_info['max_hp']
            self.deck = Deck(draw_pile_ids=entity_info['draw_pile']) 
            self.name = name

            self.damage_multiplier = 1
            self.absorption_multiplier = 1

            self.applied_offensive_effects = [] # lista de efeitos negativos aplicados por inimigos
            self.applied_defensive_effects = [] # lista de efeitos positivos aplicados por si mesmo

            img_path = game_dir / "assets" / f"{self.name}.png"
            img = pygame.image.load(img_path)
            self.sprite = pygame.transform.scale(img,(100 * .7,100 * .7)) # fixa as dimensões de todas as entidades em quadrados de 150x150

            self.max_energy = entity_info['max_energy']
            self.current_energy = entity_info['max_energy']
            self.x_pos = x_pos
            self.y_pos = y_pos
            self.rect = self.sprite.get_rect()
            self.deck.set_owner(self) # definimos o dono do deck como a porpria entidade

            self.origin_x = x_pos
            self.animation_state = AnimationState.REST
            self.animation_start_time = None
        except FileNotFoundError as error:
            print(f"{error}: asset of name {self.name} was not found in folder 'assets'")
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
        if self.check_is_alive():
            # Coordenadas Base e dimensoes para retangulos - deslocados para canto esquero do personagem
            x, y = self.x_pos - 62, self.y_pos - 35
            background_width = 65

            # Rendereizando fonte e calculando tamanho de cada barra
            hp_text_img = pygame.font.Font("assets/pixel_font.ttf", 9).render(f'{self.current_life}/{self.max_hp}', True, 'white')
            health_bar_size = background_width * (self.current_life / self.max_hp)
            defense_bar_size = background_width * (self.current_defense / self.max_defense)

            self.__draw_status_rectangle(screen, background_width, 10, health_bar_size,  x + 25, y - 13, 'red', 'grey')
            self.__draw_status_rectangle(screen, background_width,  5, defense_bar_size, x + 25, y, 'blue', 'gray')

            # Desenhar texto indicador de vida atual
            screen.blit(hp_text_img, (x + 27, y - 12))

    def check_is_alive(self):
        return self.current_life > 0
    
    def death_animate(self):
        img_path = game_dir / "assets" / "death" / f"RIP.png"
        img = pygame.image.load(img_path)
        self.sprite = pygame.transform.scale(img,(75, 75)) 

    def engage_hit(self):
        self.animation_state = AnimationState.SHAKE
        self.animation_start_time = pygame.time.get_ticks()

    def engage_attack(self):
        self.animation_state = AnimationState.ATTACK
        self.animation_start_time = pygame.time.get_ticks()

    def attack_animate(self,invert_direction:bool):
        duration_ms = 400
        x_displacement = 10
        direction = (-1) ** (int(invert_direction))

        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.animation_start_time
        if self.animation_state == AnimationState.ATTACK:
            if elapsed_time < duration_ms//2:
                self.x_pos += x_displacement*direction
            else: 
                self.animation_state = AnimationState.RETREAT

        elif self.animation_state == AnimationState.RETREAT:
            if elapsed_time < duration_ms:
                self.x_pos -= x_displacement*direction
            else:
                self.animation_state = AnimationState.REST
                self.x_pos = self.origin_x

    def hit_animate(self):
        if self.animation_state == AnimationState.SHAKE:
            duration_ms = 150
            x_displacement = 8

            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.animation_start_time
            if elapsed_time < duration_ms:
                if self.x_pos <= self.origin_x:
                    self.x_pos = self.origin_x + x_displacement
                elif self.x_pos > self.origin_x:
                    self.x_pos = self.origin_x - x_displacement
            else:
                self.x_pos = self.origin_x
                self.animation_state = AnimationState.REST

    def apply_offensive_effects(self):
        for status_effect in self.applied_offensive_effects:
            status_effect.apply_effect(affected=self)
            if status_effect.duration == 0:
                self.applied_offensive_effects.remove(status_effect)
    def apply_defensive_effects(self):
        for status_effect in self.applied_defensive_effects:
            status_effect.apply_effect(affected=self)
            if status_effect.duration == 0:
                self.applied_defensive_effects.remove(status_effect)
    def clear_multipliers(self):
        self.absorption_multiplier = 1
        self.damage_multiplier = 1

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
        super().__init__(name=name, x_pos=400, y_pos=185)
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
        health_regain : int
            Quantidade de vida ganha ao terminar um combate
    """
    def __init__(self):
        super().__init__(name="Ulisses",x_pos = 100,y_pos = 185)
        self.level = 0
        self.xp = 0
        self.coins = 0
        self.deck.shuffle_and_allocate()
        
    def draw_status_bar(self,screen:pygame.display):
        super().draw_status_bar(screen)
        energy_text_img = pygame.font.Font("assets/pixel_font.ttf", 18).render(f'{self.current_energy}', True, 'white')
        pygame.draw.circle(screen,pygame.Color('#3dad62'),(35,250),15)
        screen.blit(energy_text_img,(30,242))

    def insufficient_energy_animate(self):
        pass

class AnimationState(Enum):
    REST = 0 
    ATTACK = 1
    RETREAT = 2
    SHAKE = 3

