from abc import ABC,abstractmethod
from enum import Enum

class EffectTypes(Enum):
    POISON = 0
    REGEN = 1
    ABSORPTION = 2
    STRENGTH = 3

class StatusEffect(ABC):
    """_summary_

    Args
    ----
        ABC (_type_): _description_

    Atributos
    ---------
        type (EffectTypes): enumerador que indica tipo 
    """
    def __init__(self,duration:int):
        self.duration = duration

    @abstractmethod
    def apply_effect(self):
        self.duration -= 1

class Poison(StatusEffect):
    def __init__(self, duration:int, damage:int):
        super().__init__(duration)
        self.damage = damage
    def apply_effect(self,affected):
        affected.engage_hit()
        new_health = affected.current_life - self.damage
        if new_health <= 0:
            affected.current_life = 0
        else:
            affected.current_life = new_health
        self.damage -= 1
        super().apply_effect()

class Regen(StatusEffect):
    def __init__(self, duration:int, heal:int):
        super().__init__(duration)
        self.heal = heal
    def apply_effect(self,affected):
        new_health = affected.current_life + self.heal
        if new_health >= affected.max_hp:
            affected.current_life = affected.max_hp
        else:
            affected.current_life = new_health
        super().apply_effect()
