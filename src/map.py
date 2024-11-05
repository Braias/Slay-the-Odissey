""" Módulo responsável pelas mecânicas do mapa do jogo """


from abc import ABC, abstractmethod
from pygame import Surface, draw, display, math
from typing import Self, Callable
from enum import Enum


Point = tuple[int, int]


# INFO
# como escalonar a pixel art???
# se basear no tamanho da tela é ruim


MAP_WIDTH = 400
MAP_HEIGHT = 600
SCROLL_SPEED = 2
MARGIN = 20

COLOR_MAP = (200, 200, 150)


class MapNodeType(Enum):
    BATTLE = 0
    STORY = 1
    BOSS = 2


class MapNode(ABC):
    def __init__(self, pos: Point, type: MapNodeType, perform: Callable):
        self.pos = pos
        self.children = []
        self.type = type
        self.perform = perform
        self.reset_flags()

    def reset_flags(self):
        self.was_visited = False
        self.is_available = False
        self.is_hovered = False
        self.is_active = False

    def to(self, *args: list[Self]):
        self.children += args
        return self

    def render(self, surface: Surface):
        color = (100, 100, 100)
        if self.was_visited or self.is_available:
            color = (0, 0, 0)

        size = 10 if self.is_available else 6

        if self.type == MapNodeType.BATTLE:
            draw.circle(surface, color, self.pos, size)
        elif self.type == MapNodeType.STORY:
            draw.rect(surface, color, (
                self.pos[0] - size, self.pos[1] - size,
                size << 1, size << 1
            ))
        elif self.type == MapNodeType.BOSS:
            draw.circle(surface, color, self.pos, size * 3)

        if self.is_hovered: # overlay
            draw.circle(surface, (140, 140, 100), self.pos, size + 16, width = 4)

    def visit(self):
        self.was_visited = True
        self.is_active = True
        self.is_hovered = False
        self.is_available = False

        for child in self.children:
            child.is_available = True

        self.perform()


class MapView(Surface): # TODO: implicações de herdar Surface
    def __init__(self, target: Surface, root: MapNode):
        self.size = (MAP_WIDTH, MAP_HEIGHT)
        self.pos = (
            (target.get_width() - self.size[0]) >> 1,
            (target.get_height() - self.size[1]) >> 1
        )

        Surface.__init__(self, (MAP_WIDTH, MAP_HEIGHT))
        self.target = target
        
        self.root = root
        self.nodes = set([root])
        self.hovered_node = None
        self._add_children(root)

        self.current_node = root
        root.visit()

        self.scrolling = False
        self.scroll_initial_y = 0

        self.scroll_interval = (target.get_height() - MAP_HEIGHT - MARGIN, MARGIN)
        self.focus_on(root)

    def mouse_motion(self, mouse_pos: Point):
        if self.scrolling:
            self.pos = (
                self.pos[0],
                math.clamp(
                    mouse_pos[1] - self.scroll_initial_y,
                    self.scroll_interval[0],
                    self.scroll_interval[1],
                )
            )

        for node in self.nodes:
            diff = (node.pos[0] - mouse_pos[0] + self.pos[0]) ** 2 + \
                   (node.pos[1] - mouse_pos[1] + self.pos[1]) ** 2

            if (diff < 400) and node.is_available:
                node.is_hovered = True
                self.hovered_node = node
                return

        # Aqui o mouse não está sobre nenhum nó
        
        if self.hovered_node != None:
            self.hovered_node.is_hovered = False

        self.hovered_node = None

    def mouse_down(self, mouse_pos: Point):
        if self.hovered_node != None and self.hovered_node.is_available:
            self.current_node.is_active = False
            self.current_node.is_available = False

            for child in self.current_node.children:
                child.is_available = False

            self.hovered_node.visit()
            self.current_node = self.hovered_node
        else:
            self.scrolling = True
            self.scroll_initial_y = mouse_pos[1] - self.pos[1]

    def mouse_up(self, mouse_pos: Point):
        self.scrolling = False
        
    def render(self):
        rect = self.get_bounding_rect()
        draw.rect(self, COLOR_MAP, rect)

        self._render_edges(self.root)

        for node in self.nodes:
            node.render(self)

        self.target.blit(self, (self.pos[0], self.pos[1]))

    def focus_on(self, node: MapNode):
        self.pos = (
            self.pos[0],
            math.clamp(
                (self.target.get_height() * 3/4) - node.pos[1],
                self.scroll_interval[0],
                self.scroll_interval[1],
            )
        )

    def _add_children(self, node: MapNode):
        self.nodes.update(node.children)
        for child in node.children:
            self._add_children(child)

    def _render_edges(self, origin: MapNode):
        for child in origin.children:
            if (child.was_visited or child.is_available) and origin.was_visited:
                draw.line(self, (100, 100, 60), origin.pos, child.pos, 4)
            else:
                draw.line(self, (150, 150, 110), origin.pos, child.pos, 4)

            self._render_edges(child)


# ------------------------------------


def initial_dialogue(): pass


def nf(): print("Visited")
def boss(): print("BOSS")


node = MapNode((230, 400), MapNodeType.STORY, nf)

odyssey_map = MapNode((200, 540), MapNodeType.BATTLE, initial_dialogue).to(
    MapNode((170, 460), MapNodeType.STORY, nf).to(
        MapNode((150, 360), MapNodeType.BATTLE, nf),
        node.to(
            MapNode((180, 290), MapNodeType.BATTLE, nf).to(
                MapNode((220, 170), MapNodeType.BOSS, boss)
            )
        )
    ),
    MapNode((210, 490), MapNodeType.BATTLE, nf).to(
        MapNode((260, 440), MapNodeType.STORY, nf).to(
            node
        )
    )
)
