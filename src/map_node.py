from pygame import Surface, draw
from abc import ABC, abstractmethod
from enum import Enum
from typing import Self


Point = tuple[int, int]


class MapNodeType(Enum):
    STORY = 0
    BATTLE = 1
    BOSS = 2


class MapNode(ABC):
    def __init__(self, pos: Point, type: MapNodeType, data):
        self.pos = pos
        self.children = []
        self.type = type
        self.data = data
        self.was_visited = False
        self.is_navigable = False
        self.is_active = False

    def to(self, *args: list[Self]):
        self.children += args
        return self

    def navigate_to(self, child: Self):
        if child not in self.children:
            raise ValueError("Nó sendo visitado não é filho do anterior")

        self.is_active = False
        for c in self.children:
            c.is_navigable = False

        child.was_visited = True
        child.is_active = True
        child.is_navigable = False

        for c in child.children:
            c.is_navigable = True

    def begin(self):
        self.was_visited = True
        self.is_active = True
        for c in self.children:
            c.is_navigable = True
