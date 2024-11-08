import unittest
import unittest.mock
import sys
from pathlib import Path

game_dir = Path(__file__).parent.parent
sys.path.append("game_dir/src")

import cards

class TestCard(unittest.TestCase):
    def setUp(self):
        self.owner = unittest.mock.MagicMock
        self.target = unittest.mock.MagicMock
        
        self.owner.current_energy = 0
        self.target.current_defense = 1
        self.target.current_life = 10

        
    def test_insufficient_energy_for_card(self):
        # test_energy_card = cards.AttackCard("Tapa", "Estapeia o inimigo", cost=1, damage = 2)
        
        # with self.assertRaises(cards.InsufficientEnergyError):
        #     cards.AttackCard.check_energy(test_energy_card, self.owner)
        pass
    
    def test_wrong_target_selected(self):
        pass
    
    def test_damage_bigger_than_defense(self):
        pass
    
    def test_damage_smaller_than_defense(self):
        pass
    
    def test_damage_bigger_than_hp_of_target(self):
        pass
    
    def test_damage_smaller_than_hp_of_target(self):
        pass

if __name__ == "__main__":
    unittest.main()

    