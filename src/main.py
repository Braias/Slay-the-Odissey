import pygame
from screen import Screen
import math





# Temporário ---------------------

from map import MapScreen
from map_node import MapNode, MapNodeType

class TestScreen(Screen):
    def __init__(self, surface: pygame.Surface):
        self.surface = surface

    def handle_event(self, event: pygame.event.Event):
        pass

    def update(self):
        pass

    def draw(self):
        pygame.draw.rect(self.surface, (255,100,0), (100, 100, 100, 100))

def init(surface: pygame.Surface):
    root = MapNode((220, 450), MapNodeType.STORY, None)
    root.add_child(MapNode((210, 350), MapNodeType.BATTLE, TestScreen(surface)))

    return MapScreen(surface, root)

# fim Temporário ---------------------





pygame.init()

SCREEN_DIMENSIONS = (1000,700) # Valores temporários
SCALE = 2

window_surface = pygame.display.set_mode(SCREEN_DIMENSIONS)
downscaled_surface = pygame.Surface(
    (SCREEN_DIMENSIONS[0] / SCALE, SCREEN_DIMENSIONS[1] / SCALE)
)
clock = pygame.time.Clock()
running = True

current_screen = init(downscaled_surface)

transition_progress = math.pi / 2 # Para ter uma transição no início do jogo
transition_surface = pygame.Surface(downscaled_surface.get_size())
transition_surface.fill((0,0,0))
transition_to = None


while running:
    # Roda apenas enquanto a transição estiver em progresso
    if transition_progress < math.pi:
        # Não atualiza nem processa os eventos; apenas desenha a tela atual
        current_screen.draw()

        transition_progress += 0.1

        # Troca `current_screen` na metade da transição, quando a tela estiver
        # toda preta, para o jogador não perceber
        if transition_progress > math.pi / 2 and transition_to != None:
            current_screen = transition_to
            transition_to = None

        # "Desenha" a transição sobre a surface principal.
        # `255 * (sin(t) ** 2)` faz uma transição suave de 0 -> 255 -> 0
        transition_surface.set_alpha(255 * (math.sin(transition_progress) ** 2))
        downscaled_surface.blit(transition_surface, (0,0))

    else:
        for event in pygame.event.get():
            # Pré-processa os eventos do mouse para que as telas não tenham
            # que lidar com `SCALE`
            if event.type == pygame.MOUSEBUTTONDOWN \
                or event.type == pygame.MOUSEBUTTONUP \
                or event.type == pygame.MOUSEMOTION:

                downscaled_pos = pygame.Vector2(event.dict["pos"])
                event.dict["pos"] = downscaled_pos / SCALE

            elif event.type == pygame.QUIT:
                running = False

            current_screen.handle_event(event)

        next_screen = current_screen.update()
        current_screen.draw()

        # Se a função `update()` retornou algo, começa a transição e armazena
        # a tela retornada para fazer a substituição depois
        if next_screen != None:
            transition_to = next_screen
            transition_progress = 0

    scaled_surface = pygame.transform.scale_by(downscaled_surface, SCALE)
    window_surface.blit(scaled_surface, (0,0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
