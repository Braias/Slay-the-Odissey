from abc import ABC, abstractmethod
import entities

class Card(ABC):
    def __init__(self, name: str, 
                 description: str, 
                 cost: int,
                 type: str,
                 card_user: entities.Entity, 
                 target: entities.Entity):
        self._name = name
        self._description = description
        self._cost = cost
        self._type = type
        self._card_user = card_user
        self._target = target
    
    def check_energy(self):
        try:
            if self._card_user.energy < self._cost:
                raise ValueError
        except:
            if self._card_user.__class__ == entities.Enemy:
                # lógica para a ação de jogar dos inimigos (passar pra próxima carta caso não tenha energia)
                pass
            else:
                # lógica para ação do jogador (não conseguir selecionar a carta se não tiver energia)
                pass                           

    @property
    @abstractmethod
    def apply_card(): ...

class AttackCard(Card):
    def __init__(self, name, description, cost, target, card_user, damage: int, effect: str, type="attack"):
        super().__init__(name, description, cost, target, card_user, type)
        self._damage = damage
        self._effect = effect

    @property        
    def apply_card(self):
        self._card_user.energy -= self._cost
        self._target.current_life -= self._damage
