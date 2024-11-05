from pygame import Surface, draw
from abc import ABC, abstractmethod
from enum import Enum
from typing import Self


Point = tuple[int, int]


class Scroller:
    pass


class MapNodeType(Enum):
    BATTLE = 0
    STORY = 1
    BOSS = 2


class MapNode(ABC):
    def __init__(self, pos: Point, type: MapNodeType, data):
        self.pos = pos
        self.children = []
        self.type = type
        self.data = data
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

