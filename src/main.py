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
    entities_on_screen = [ulisses]+cl.instantiated_enemies
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            current_mouse_pos = pygame.mouse.get_pos()
            if ulisses.rect.collidepoint(current_mouse_pos):
                ulisses.deck.shuffle_and_allocate()
                print(ulisses.deck)
    cl.draw_level()
    ulisses.draw_entity(screen)
    ulisses.deck.draw_hand_on_screen(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()