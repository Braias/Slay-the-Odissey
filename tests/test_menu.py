import unittest
import sys
from pathlib import Path
from pygame import Vector2, init
from pygame.font import Font, get_default_font


game_dir = Path(__file__).parent.parent
sys.path.append(f"{game_dir}/src")

from menu_button import Button


class TestMenuButton(unittest.TestCase):
    def setUp(self):
        init()
        self.font = Font(get_default_font(), 10)
        self.btn = Button((125, 125), (50, 50), "Hello world!", self.font)
        # (100, 100) is the center of the button
        # Here, the button is going from (100, 100) to (150, 150)

    def test_mouse_outside_button_should_not_be_hovering(self):
        positions = [
            (90, 90),   # Top left
            (90, 120),  # Left
            (90, 160),  # Bottom left
            (120, 160), # Bottom
            (160, 160), # Bottom right
            (160, 120), # Right
            (160, 90),  # Top right
            (120, 90),  # Top
        ]
        for pos in positions:
            self.btn.on_mouse_motion(Vector2(pos))
            self.assertFalse(self.btn.is_hovering)

    def test_mouse_inside_button_should_be_hovering(self):
        positions = [
            (125, 125), # Center
            (110, 110),
            (110, 140),
            (140, 140),
            (140, 110),
        ]
        for pos in positions:
            self.btn.on_mouse_motion(Vector2(pos))
            self.assertTrue(self.btn.is_hovering)

    def test_mouse_over_edges_should_not_be_hovering(self):
        positions = [
            (100, 100), # Top left
            (100, 125), # Left
            (100, 150), # Bottom left
            (125, 150), # Bottom
            (150, 150), # Bottom right
            (150, 125), # Right
            (150, 100),  # Top right
            (125, 100),  # Top
        ]
        for pos in positions:
            self.btn.on_mouse_motion(Vector2(pos))
            self.assertFalse(self.btn.is_hovering)

    def test_hovering_should_be_false_by_default(self):
        self.assertFalse(self.btn.is_hovering)

    def test_moving_in_out_should_change_hovering_state(self):
        self.btn.on_mouse_motion(Vector2(0, 0))
        self.assertFalse(self.btn.is_hovering)
        self.btn.on_mouse_motion(Vector2(120, 120))
        self.assertTrue(self.btn.is_hovering)
        self.btn.on_mouse_motion(Vector2(160, 160))
        self.assertFalse(self.btn.is_hovering)

    def test_negative_mouse_position_should_not_bug(self):
        btn = Button((-10, -10), (20, 20), "Hello world!", self.font)

        btn.on_mouse_motion(Vector2(-10, -10))
        self.assertTrue(btn.is_hovering)
        btn.on_mouse_motion(Vector2(-1, -1))
        self.assertTrue(btn.is_hovering)
        btn.on_mouse_motion(Vector2(10, 10))
        self.assertFalse(btn.is_hovering)
        btn.on_mouse_motion(Vector2(-25, 0))
        self.assertFalse(btn.is_hovering)


if __name__ == "__main__":
    unittest.main()
