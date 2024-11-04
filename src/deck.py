import random

class Deck:
    def __init__(self,draw_pile=[]):
        self.hand = []
        self.draw_pile = draw_pile
        self.discard_pile = []
        self.exhaust_pile =[]

    def shuffle_and_allocate(self):     
        # Checamos quantas caratas estão disponíveis
        cards_to_draw = len(self.draw_pile) 
        # Caso não temos cartas suficentes para formar uma mão adcionamos do deck de descarte
        if cards_to_draw < 5: 
            self.draw_pile+=self.discard_pile
        random.shuffle(self.draw_pile)
        hand = self.draw_pile[:5]
        return hand