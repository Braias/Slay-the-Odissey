import pygame
import os
class WorldLevel:
    def __init__(self,screen:pygame.display,background_name:str,stages:tuple):
        self.background_img = pygame.image.load(f'./assests/{background_name}.png')
        self.game_state = 0
        self.stages = stages
        self.screen = screen
        
