import pygame


class Entity():
    def __init__(self, life: int, deck: Deck, sprite: pygame.image, name: str, energy: int):
        self.defense = 0
        self.is_alive = True
        self.life = life
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


class Deck():
    def __init__(self):
        self.hand = []
        self.draw_pile = []
        self.discard_pile = []

    def shuffle(self):
        # TODO

        return hand
