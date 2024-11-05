# Example file showing a basic pygame "game loop"
import pygame
import entities
from deck import Deck
from world_level import CombatLevel
# pygame setup
pygame.init()

SCREEN_DIMENSIONS = (800,700)

screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
clock = pygame.time.Clock()
running = True

ulisses = entities.Ulisses()

cl = CombatLevel(screen=screen,background_name='test_bg',stages=(['Fairy'],['King']))

index = True
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    colors = ['purple','yellow']
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            index = not(index)
            cl.next_game_state()
            

    # fill the screen with a color to wipe away anything from last frame
    color = colors[int(index)]
    cl.draw_level()
    ulisses.draw_entity(screen)
    pygame.draw.rect(screen, color, pygame.Rect(440, 300, 150, 150))
    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()