#Unocards module
#Nidhin Mohan
#22/06/2019

class Unocard(object):
    
    RANK = ['0','1','2','3','4','5','6','7','8','9','+2','R','S']
    COLOUR = ['r','b','g','y','w']
    WILDRANK = ['','+4']
    def __init__(self, rank, colour):
        self.rank = rank
        self.colour = colour

    def __str__(self):
        rep = self.rank + self.colour
        return rep

class Unohand(object):
    
    def __init__(self):
        self.cards = []
        
    def __str__(self):
        if self.cards:
            rep=""
            for card in self.cards:
                rep += str(card) + "\t"
        else:
            rep="<empty>"
        return rep

    def add(self, card):
        self.cards.append(card)

    def clear(self):
        self.cards = []

    def give(self, card, other_hand):
        self.cards.remove(card)
        other_hand.add(card)

class Unodeck(Unohand):

    def fill(self):
        for colour in COLOUR:
            if colour == 'w':
                for rank in ('', '+4'):
                    quadruplecard = Unocard(rank, colour)
                    self.add(quadruplecard)*4
            else:
                for rank in ('1','2','3','4','5','6','7','8','9','S','R','+2'):
                    doublecard = Unocard(rank, colour)
                    self.add(doublecard)*2
                else:
                    rank = '0'
                    self.add(Unocard(rank,colour))
                

    def shuffle(self):
        import random
        random.shuffle(self.cards)

    def deal(self, hands, per_hand=1):
        for i in range(per_hand):
            for hand in hands:
                if self.cards:
                    top_card = self.cards[0]
                    self.give(top_card, hand)

if __name__=="__main__":
        print("This is a module for playing cards.")
        input("\n\nPress the enter key to exit.")
        
