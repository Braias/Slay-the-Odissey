from abc import ABC, abstractmethod
from pathlib import Path
import pygame
import status_effects as se
import pygame.mixer as pm

pm.init()

death_sound = pm.Sound("sounds/death_sound.wav")

class InsufficientEnergyError(Exception):
    def __init__(self, message="A energia atual não é suficiente para essa carta"):
        super().__init__(message)

class WrongTargetError(Exception):
    def __init__(self, message="A carta escolhida não pode ser aplicada no alvo selecionado"):
        super().__init__(message)

class Card(ABC):
    """
    Classe para todas as cartas a serem utilizadas nas batalhas do jogo

    Atributos
    ----------
    name : str
        Título específico da carta.
    cost : int
        Custo energético da carta perante ao seu uso.
    type : str
        Tipo da Carta dentre os definidos: "Attack", "Defense", etc.
    """
    
    def __init__(self, name: str, cost: int, type: str):
        self._name = name
        self._cost = cost 
        self._type = type 
        
        game_dir = Path(__file__).parent.parent
        img_path = game_dir / "assets" / f"{name}.png"
        img = pygame.image.load(img_path)
        
        self.sprite = pygame.transform.scale(img,(75,75))
        self.rect = self.sprite.get_rect()
        self.x_pos = 50
        self.y_pos = 310
        self.rect.center = (self.x_pos,self.y_pos)
    
    def check_energy(self,owner) -> bool:
        return self._cost <= owner.current_energy

    @abstractmethod
    def check_target(self,owner, target) -> bool: ...

    @abstractmethod
    def apply_card(self, owner, target):
        """
        Aplica as funcionalidades da carta no alvo escolhido e cobra o custo da carta.
        """ 
        owner.current_energy -= self._cost
        owner.deck.discard_card(self)
        owner.deck.selected_card = None

    def validate_application(self,owner,target) -> bool:
        return (self.check_energy(owner) and self.check_target(owner,target) and target.check_is_alive())

class AttackCard(Card):
    """
    Classe Filha de Card, referente às cartas de Ataque, que diminuem HP do alvo.

    Atributos
    ----------
    name : str
        Título específico da carta.
    cost : int
        Custo energético da carta perante ao seu uso.
    damage : int
        Valor de dimuição do HP do alvo.
    type : str, optional
        Tipo da Carta dentre os definidos: "Attack", "Defense", etc, por default "attack"
    """
    def __init__(self, name, cost, damage: int, type:str):
        super().__init__(name, cost, type)
        self._damage = damage

    def check_target(self, owner, target) -> bool:
        """
        Checa a aplicabilidade da carta no alvo escolhido.

        Parametros
        ----------

        """
        return not owner == target

    def apply_card(self, owner, target):
        """
        Aplica as funcionalidades da carta no alvo escolhido e cobra o custo da carta. Aqui, diminui o HP do alvo escolhido. 
        """
        if self.validate_application(owner,target):
            if target.current_defense < self._damage:
                # Subtrai a diferença entre o dano e a defesa da vida atual do alvo
                damage = int((self._damage*owner.damage_multiplier)/target.absorption_multiplier)
                new_target_hp = target.current_life - (damage - target.current_defense)
                if new_target_hp <= 0:
                    target.current_life = 0
                    death_sound.play()
                else:
                    target.current_life = new_target_hp
                target.current_defense = 0 
            else:
                target.current_defense -= self._damage
            super().apply_card(owner,target)
            owner.engage_attack()
            target.engage_hit()

class DefenseCard(Card):
    def __init__(self, name, cost, defense: int, type:str):
        super().__init__(name, cost, type)
        self._defense = defense
     
    def check_target(self, target, owner) -> bool:
        """
        Checa a aplicabilidade da carta no alvo escolhido.

        Parametros 
        ----------

        """
        return(owner == target)

    def apply_card(self,owner,target):
        """
        Aplica as funcionalidades da carta no alvo escolhido e cobra o custo da carta. Aqui, aumenta a defesa do usuário. 
        """
        if self.validate_application(owner,target):
            new_defense = target.current_defense + self._defense
            if new_defense > target.max_defense:
                target.current_defense = target.max_defense
            else:
                target.current_defense = new_defense
            super().apply_card(owner,target)

        
class EffectCard(Card,ABC):
    def __init__(self, name:str, cost:int, type:str, status_effect_id:int, **kwargs):
        super().__init__(name, cost, type)
        self.status_effect_info = kwargs
        self.status_effect_id = status_effect_id

    def check_target(owner, target):
        super().check_target(target)
    
    def apply_card(self, owner, target):
        super().apply_card(owner,target)

    def instantiate_status_effect(self,status_effect_id:int,**kwargs) -> se.StatusEffect:
        chosen_effect_type = se.EffectTypes(status_effect_id)
        try:
            duration = kwargs['duration']
            if chosen_effect_type == se.EffectTypes.POISON:
                damage = kwargs['damage']
                return se.Poison(duration,damage)
            elif chosen_effect_type == se.EffectTypes.ABSORPTION:
                pass
            elif chosen_effect_type == se.EffectTypes.REGEN:
                heal = kwargs['heal']
                return se.Regen(duration,heal)
            elif chosen_effect_type == se.EffectTypes.STRENGTH:
                dmg_buff = kwargs['damage_percent_buff']
                return se.Strength(duration,dmg_buff)    
        except KeyError as error:
            print(f'{error}:inadequate parameters passed for {chosen_effect_type} card - {kwargs}')

class OffensiveEffectCard(EffectCard):
    def __init__(self, name:str, cost:int, type:str, status_effect_id:int,**kwargs):
        super().__init__(name, cost, type, status_effect_id,**kwargs)

    def check_target(self,owner, target):
        return not(owner == target)
    
    def apply_card(self, owner, target):
        if self.validate_application(owner,target):
            status_effect = self.instantiate_status_effect(self.status_effect_id,
                                                            **self.status_effect_info)
            owner.engage_attack()
            status_effect.apply_effect(target)
            target.applied_offensive_effects.append(status_effect)
            super().apply_card(owner, target)


class DefensiveEffectCard(EffectCard):
    def __init__(self, name:str, cost:int, type:str, status_effect_id:int,**kwargs):
        super().__init__(name, cost, type, status_effect_id,**kwargs)

    def check_target(self,owner, target):
        return (owner == target)
    
    def apply_card(self, owner, target):
        if self.validate_application(owner,target):
            status_effect = self.instantiate_status_effect(self.status_effect_id,
                                                            **self.status_effect_info)
            status_effect.apply_effect(target)
            target.applied_defensive_effects.append(status_effect)
            super().apply_card(owner, target)
