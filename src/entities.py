import pygame
from cards import Deck


class Entity():
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
    def __init__(self, max_hp: int, deck: Deck, sprite: pygame.image, name: str, energy: int):
        self.defense = 0
        self.is_alive = True
        self.current_life = max_hp
        self.max_hp = max_hp
        self.deck = deck
        self.sprite = sprite
        self.name = name
        self.energy = energy


class Enemy(Entity):
    """
    Classe que representa um inimigo no jogo - herda classe 'Entity'

    Atributos:
        drop_xp (int): Quantidade de experiência que o inimigo dropa na morte
    """
    def __init__(self, drop_xp: int):
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
        self.level = 0
        self.xp = 0
        self.coins = 0