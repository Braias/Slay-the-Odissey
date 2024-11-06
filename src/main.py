# Example file showing a basic pygame "game loop"
import pygame
import entities
from deck import Deck
from world_level import CombatLevel
pygame.init()

SCREEN_DIMENSIONS = (800,700)

screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
clock = pygame.time.Clock()
running = True

ulisses = entities.Ulisses()

cl = CombatLevel(screen=screen,background_name='test_bg',stages=(['Ogre'],['King']))

index = True
while running:
    colors = ['purple','yellow']
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            index = not(index)
            ulisses.current_life -= 10
    color = colors[int(index)]
    cl.draw_level()
    ulisses.draw_entity(screen)
    pygame.draw.rect(screen, color, pygame.Rect(440, 300, 150, 150))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()