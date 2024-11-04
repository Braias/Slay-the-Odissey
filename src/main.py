# Example file showing a basic pygame "game loop"
import pygame
import entities
from cards import Deck

class GameAnimationHandler():
    def draw_entities(self,*args:entities):
        for entity in args:
            screen.blit(entity.sprite,entity.rect)



# pygame setup
pygame.init()

screen = pygame.display.set_mode((800, 540))
clock = pygame.time.Clock()
running = True

bg = pygame.image.load('./assests/test_bg.jpeg')
enemies = []
ulisses = entities.Ulisses()

handler = GameAnimationHandler()

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
            

    # fill the screen with a color to wipe away anything from last frame
    screen.blit(bg, (0, 0))
    color = colors[int(index)]
    handler.draw_entities(ulisses)
    pygame.draw.rect(screen, color, pygame.Rect(450, 300, 150, 150))
    pygame.draw.rect(screen, color, pygame.Rect(620, 300, 150, 150))

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()