import pygame
class Entity():
    def __init__(self,life:int,deck:dict,
                 sprite:pygame.image,name:str,xp:int,coins:int,
                 actions:int):
        self.life = life
        self.defense = 0
        self.is_alive = True
        self.deck = deck
        self.sprite = sprite
        self.hand = []
        self.name = name
        self.xp = xp
        self.coins = coins
        self.actions = actions


