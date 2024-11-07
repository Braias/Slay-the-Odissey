import random
import cards
import json
import pygame

with open(file='./assets/cards.json',mode='r') as card_config:
    default_card_configurations = json.load(card_config)

class Deck:
    def __init__(self,draw_pile_ids=[]):
        self.hand = []
        self.draw_pile= self.build_draw_pile(draw_pile_ids)
        self.discard_pile = []
        self.exhaust_pile =[]
        self.owner = None
    def __str__(self):
        hand_names = []
        discard_pile_names = []
        for each_card in self.hand:
            hand_names.append(each_card._name)
        for each_card in self.discard_pile:
            discard_pile_names.append(each_card._name)
        return f"hand:{hand_names}\ndiscard pile:{discard_pile_names}"
    def shuffle_and_allocate(self):
        # limpar mao atual e mover para pilha de descarte
        self.discard_pile += self.hand 
        self.hand = []     
        # Checamos quantas cartas estão disponíveis
        cards_to_draw = len(self.draw_pile) 
        # Caso não temos cartas suficentes para formar uma mão adcionamos do deck de descarte
        if cards_to_draw < 5: 
            self.draw_pile+=self.discard_pile
            self.discard_pile = []
        # Embaralhamos o deck e removemos as primeiras 5 cartas
        random.shuffle(self.draw_pile)
        next_hand = self.draw_pile[:5]
        del(self.draw_pile[:5])
        # posicionamos as cartas no display e consturimos nossa mao
        for card_index,card in enumerate(next_hand):
            card.x_pos = 100+150*card_index
        self.hand = next_hand
    
    def build_draw_pile(self,draw_pile_ids:list):
        draw_pile = []
        for card_id in draw_pile_ids:
            card_info = default_card_configurations['cards'][card_id]
            card_type = card_info['type']
            if card_type == 'attack':
                draw_pile.append(cards.AttackCard(card_id,card_info['description'],
                                                  card_info['cost'],card_info['damage'],
                                                  card_type))
            elif card_type == 'defense':
                draw_pile.append(cards.DefenseCard(card_id,card_info['description'],
                                                   card_info['cost'],card_info['defense'],
                                                   card_type))
        return draw_pile
    def draw_hand_on_screen(self,screen:pygame.display):
        for card in self.hand:
            card.rect.center=(card.x_pos,card.y_pos)
            screen.blit(card.sprite,card.rect)
    def set_owner(self,owner):
        self.owner = owner
    def discard_card(self,card:cards):
        self.hand.remove(card)
        self.discard_pile.append(card)
