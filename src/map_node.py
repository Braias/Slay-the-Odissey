from pygame import Surface, draw, math
from enum import Enum
from typing import Self


Point = tuple[int, int]


class MapNodeType(Enum):
    FIREPLACE = 0
    STORY = 1
    BATTLE = 2
    BOSS = 3


class MapNode:
    def __init__(self, pos: Point, type: MapNodeType, screen):
        self.pos = math.Vector2(pos)
        self.children = []
        self.type = type
        self.screen = screen # A tela a ser exibida quando o nó for escolhido
        self.was_visited = False # O jogador já visitou esse nó?
        self.is_navigable = False # O jogador pode escolher ir para esse nó?
        self.is_active = False # Esse é o nó em que o jogador se encontra?

    # Na prática, cria arestas direcionadas do nó atual aos passados em `args`
    def add_child(self, *args: list[Self]):
        self.children += args

    # Atualiza as propriedades dos nós para refletir a ação do jogador ter
    # "navegado" para `child`. Ou seja, `child` se torna o novo nó ativo e o
    # nó atual tem seu estado resetado.
    def navigate_to(self, child: Self):
        if child not in self.children:
            raise ValueError("Nó sendo visitado não é filho do anterior")

        child.activate()

        # Reseta o estado "ativo" do nó atual, mas mantendo `was_visited`
        self.is_active = False
        for c in self.children:
            c.is_navigable = False

    # Torna o nó ativo, AKA, o nó em que o jogador está, e atualiza o grafo de
    # acordo.
    def activate(self):
        self.was_visited = True
        self.is_active = True
        for c in self.children:
            c.is_navigable = True
