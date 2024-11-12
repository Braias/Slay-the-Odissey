import unittest
import unittest.mock
import sys
from pathlib import Path

game_dir = Path(__file__).parent.parent

sys.path.append(f"{game_dir}/src")

import cards

class TestCard(unittest.TestCase):
    def setUp(self):
        self.owner = unittest.mock.MagicMock()
        self.target = unittest.mock.MagicMock()
        
        self.owner.current_energy = 0
        self.target.defense = 2
        self.target.current_life = 10

    @unittest.mock.patch("builtins.print")
    def test_check_energy_enemy_logic(self, mock_print):
        self.owner.__class__.__name__ = "Enemy"
        
        test_energy_card = cards.AttackCard("Tapa", "Estapeia o inimigo", cost=1, damage=2)
        test_energy_card.check_energy(self.owner)
        
        # Iserir aqui a lógica de tratamento do erro pro inimigo
        mock_print.assert_called_once_with("Ei, inimigo")

    @unittest.mock.patch("builtins.print")
    def test_check_energy_player_logic(self, mock_print):
        self.owner.__class__.__name__ = "Player"
        
        test_energy_card = cards.AttackCard("Tapa", "Estapeia o inimigo", cost=1, damage=2)
        test_energy_card.check_energy(self.owner)
        
        # Iserir aqui a lógica de tratamento do erro pro ulisses
        mock_print.assert_called_once_with("Ei, Ulisses")
        
    
    @unittest.mock.patch("builtins.print")
    def test_wrong_target_selected_for_attack(self, mock_print):
        
        test_wrong_target_selected_for_attack_card = cards.AttackCard("Tapa", "Estapeia o inimigo", cost=1, damage=2)
        test_wrong_target_selected_for_attack_card.check_target(self.owner, self.owner)
        
        mock_print.assert_called_once_with("Essa carta não pode ser aplicada em si mesmo")
    
    @unittest.mock.patch("builtins.print")
    def test_wrong_target_selected_for_defense(self, mock_print):
        
        test_wrong_target_selected_for_defense_card = cards.DefenseCard("Escudo", "Equipa um escudo", cost=1, defense=2)
        test_wrong_target_selected_for_defense_card.check_target(self.owner, self.target)
        
        mock_print.assert_called_once_with("Essa carta não pode ser aplicada em um inimigo")
    
    def test_damage_bigger_than_defense(self):
        
        test_damage_bigger_than_defense_card = cards.AttackCard("Tapa", "Estapeia o inimigo", cost=1, damage=3)
        
        test_damage_bigger_than_defense_card.apply_card(self.owner, self.target)
    
        self.assertEqual(self.target.current_life, 9) 
        
    def test_damage_smaller_than_defense(self):
        test_damage_smaller_than_defense_card = cards.AttackCard("Tapa", "Estapeia o inimigo", cost=1, damage=1)
        
        test_damage_smaller_than_defense_card.apply_card(self.owner, self.target)
    
        self.assertEqual(self.target.defense, 1) 
    
    def test_damage_bigger_than_hp_of_target(self):
        pass
    
    def test_damage_smaller_than_hp_of_target(self):
        pass

if __name__ == "__main__":
    unittest.main()

    