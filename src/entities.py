import pygame
from cards import Deck


class Entity():
    def __init__(self, max_hp: int, deck: Deck, sprite: pygame.image, name: str, energy: int):
        self.defense = 0
        self.is_alive = True
        self.current_life = max_hp
        self.max_hp = max_hp
        self.deck = deck
        self.sprite = sprite
        self.name = name
        self.energy = energy


class Enemy():
    def __init__(self, drop_xp: int):
        self.drop_xp = drop_xp


class Ulisses():
    def __init__(self):
        self.level = 0
        self.xp = 0
        self.coins = 0