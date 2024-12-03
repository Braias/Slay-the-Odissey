import unittest
import sys
from pathlib import Path


game_dir = Path(__file__).parent.parent
sys.path.append(f"{game_dir}/src")

from map_node import MapNode, MapNodeType


class TestMapNode(unittest.TestCase):
    def setUp(self):
        any_pos = (0,0) # A posição na tela é irrelevante aqui
        any_screen = None # Mesma coisa

        self.v1 = MapNode(any_pos, MapNodeType.STORY, any_screen)
        self.v2 = MapNode(any_pos, MapNodeType.STORY, any_screen)
        self.v3 = MapNode(any_pos, MapNodeType.STORY, any_screen)
        self.v4 = MapNode(any_pos, MapNodeType.STORY, any_screen)
        self.v5 = MapNode(any_pos, MapNodeType.STORY, any_screen)
        self.v6 = MapNode(any_pos, MapNodeType.STORY, any_screen)     
        self.v7 = MapNode(any_pos, MapNodeType.STORY, any_screen)     
        self.v8 = MapNode(any_pos, MapNodeType.BOSS, any_screen)     

        self.v1.add_children(self.v2)
        self.v2.add_children(self.v3, self.v5)
        self.v3.add_children(self.v6)
        self.v6.add_children(self.v5)
        self.v5.add_children(self.v4, self.v7)
        self.v7.add_children(self.v8)

        # Representação gráfica do mapa criado acima:
        #
        #      v7 → v8
        #      ↑
        # v4 ← v5 ← v6
        #      ↑     ↑
        #      v2 → v3
        #      ↑
        #      v1

    def test_invalid_navigation_should_raise_ValueError(self):
        with self.assertRaises(ValueError):
            self.v1.navigate_to(self.v3)

        with self.assertRaises(ValueError):
            self.v2.navigate_to(self.v7)

    def test_navigating_backwards_should_raise_ValueError(self):
        with self.assertRaises(ValueError):
            self.v2.navigate_to(self.v1)

        with self.assertRaises(ValueError):
            self.v4.navigate_to(self.v5)

    def test_adding_parallel_edge_should_raise_ValueError(self):
        with self.assertRaises(ValueError):
            self.v2.add_children(self.v3)

        with self.assertRaises(ValueError):
            self.v5.add_children(self.v7)

    def test_navigating_should_mark_as_visited(self):
        self.v1.navigate_to(self.v2)
        self.v2.navigate_to(self.v3)
        self.v3.navigate_to(self.v6)

        self.assertTrue(self.v2.was_visited)
        self.assertTrue(self.v3.was_visited)

    def test_activating_should_mark_as_visited(self):
        self.v1.activate()

        self.assertTrue(self.v1.was_visited)

    def test_activating_should_mark_as_active(self):
        self.v1.activate()

        self.assertTrue(self.v1.is_active)

    def test_navigating_should_change_active_node(self):
        self.v1.activate()
        self.v1.navigate_to(self.v2)
        self.v2.navigate_to(self.v5)

        self.assertFalse(self.v1.is_active)
        self.assertFalse(self.v2.is_active)
        self.assertTrue(self.v5.is_active)

    def test_active_node_children_should_be_navigable(self):
        self.v1.activate()
        self.v1.navigate_to(self.v2)
        self.v2.navigate_to(self.v5)

        self.assertTrue(self.v4.is_navigable)
        self.assertTrue(self.v7.is_navigable)

    def test_non_active_node_children_should_not_be_navigable(self):
        self.v1.activate()
        self.v1.navigate_to(self.v2)
        self.v2.navigate_to(self.v5)

        self.assertFalse(self.v6.is_navigable)
        self.assertFalse(self.v2.is_navigable)
        self.assertFalse(self.v8.is_navigable)


if __name__ == "__main__":
    unittest.main()
