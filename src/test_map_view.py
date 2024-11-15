import pygame
from map import odyssey_map, MapScreen


SCALE = 2


pygame.init()
screen = pygame.display.set_mode((1280, 720))
win = pygame.Surface((1280 / SCALE, 720 / SCALE))
clock = pygame.time.Clock()
running = True


map_screen = MapScreen(win, odyssey_map)
mouse_events = [
    pygame.MOUSEBUTTONDOWN,
    pygame.MOUSEBUTTONUP,
    pygame.MOUSEMOTION,
]


while running:
    for event in pygame.event.get():
        if event.type in mouse_events:
            pos = event.dict["pos"]
            event.dict["pos"] = (pos[0] / SCALE, pos[1] / SCALE)

        map_screen.handle_event(event)

        if event.type == pygame.QUIT:
            running = False
            continue

    new_node = map_screen.get()
    if new_node != None:
        print(new_node)

    win.fill("black")
    map_screen.render()

    scaled_win = pygame.transform.scale_by(win, SCALE)
    screen.blit(scaled_win, (0, 0))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
