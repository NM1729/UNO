#UNO Game
#Nidhin Mohan
#22/06/19

import unocards

class Unocard2(unocards.Unocard):

    #Returns whether the card can be played or not
    def is_valid(self, currentcard):
        return self.rank == currentcard.rank or self.colour == currentcard.colour or self.colour == 'w'

    #Returns whether the card is a special card or not
    def is_special(self):
        return self.colour == 'w' or self.rank in ('S', 'R', '+2')
    def special_action(self, currentcard, deck, currentplayer, hands):

        #Wild Card
        if self.colour == 'w':

            #+4 Card
            if self.rank == '+4':
                print("Next player must draw 4 cards.\n")
                deck.deal([hands[((hands.index(currentplayer)+1)%2)]], per_hand=4)
                print(hands[((hands.index(currentplayer)+1)%2)])
            currentcard.colour = input("Now change the colour(r,b,g,y):").lower()
            while currentcard.colour not in ('r','b','g','y'):
                currentcard.colour = input("Change the colour again(r,b,g,y):").lower()
            print(currentcard.colour)

        #+2 Card
        if self.rank == '+2':
            print("Next player must draw 2 cards.\n")
            deck.deal([hands[((hands.index(currentplayer)+1)%2)]], per_hand=2)
            print(hands[((hands.index(currentplayer)+1)%2)])

        #Stop or Reverse Card(for only two players)
        if self.rank == 'R' or self.rank == 'S':
            currentplayer = hands[(hands.index(currentplayer)+1)%2]
            print(currentplayer)
        return currentplayer
        

class Unohand2(unocards.Unohand):

    #Initialise hand
    def __init__(self, name):
        super(Unohand2, self).__init__()
        self.name = name

    #Print hand
    def __str__(self):
        rep = ""
        rep += self.name + ":\t" + super(Unohand2, self).__str__()
        return rep

class Unodeck2(unocards.Unodeck):

    #Fill up the deck
    def fill(self):
        for colour in Unocard2.COLOUR:
            if colour == 'w':
                for rank in Unocard2.WILDRANK:
                    quadruplecard = Unocard2(rank, colour)
                    self.add(quadruplecard)
                    self.add(quadruplecard)
                    self.add(quadruplecard)
                    self.add(quadruplecard)
            else:
                for rank in Unocard2.RANK:
                    doublecard = Unocard2(rank, colour)
                    self.add(doublecard)
                    self.add(doublecard)
                else:
                    rank = '0'
                    self.add(Unocard2(rank,colour))

class Unoplayer(Unohand2):

    #Players plays a card from his hand
    def next_move(self, cardname, currentcard, currentplayer, deck, hands):
        valid_card = ""
        for card in self.cards:
            if cardname == str(card):
                if card.is_valid(currentcard):
                    valid_card = card
                    currentplayer.cards.remove(valid_card)
                if valid_card != "":
                    if valid_card.is_special():
                        print("The card is special.\n")
                        currentplayer = valid_card.special_action(currentcard, deck, currentplayer, hands)
        if valid_card == "":
            currentcard = None
        else:
            print("This card is valid.\n")
            if valid_card.colour != 'w':    
                currentcard = valid_card
            else:
                currentcard.rank = '#'
        return currentcard, valid_card, currentplayer

    #Player takes a card from the deck
    def deal_from_deck(self, deck, currentcard, currentplayer, hands):
        valid_card = currentcard
        top_card = deck.cards[0]
        deck.give(top_card, currentplayer)
        if top_card.is_valid(currentcard):
            valid_card = top_card
            currentplayer.cards.remove(top_card)
            if valid_card != "":
                if valid_card.is_special():
                    print("The card is special.\n")
                    currentplayer = valid_card.special_action(currentcard, deck, currentplayer, hands)
            if valid_card == "":
                currentcard = None
            else:
                print("This card is valid.\n")
                if valid_card.colour != 'w':    
                    currentcard = valid_card
                else:
                    currentcard.rank = '#'
        return currentcard, valid_card, currentplayer, deck
        

class Unogame(object):

    #Starts the game, shuffles the deck and deals the cards
    def __init__(self, hands):
        self.deck = Unodeck2()
        self.discard = Unodeck2()
        self.hands = hands
        self.deck.fill()
        self.deck.shuffle()
        self.deck.deal(self.hands, per_hand = 7)
        self.player = hands[0]
        self.dealer = hands[1]
        top_card = self.deck.cards[0]
        if top_card.colour == 'w':
            top_card = self.deck.cards[1]
        self.currentcard = top_card
        self.deck.give(top_card, self.discard)

    #Move of the current player
    def player_move(self, currentplayer):
        valid_card = ""
        choice = ""
        uno = False
        prevcurrentcard = self.currentcard
        self.currentplayer = currentplayer
        print(self.currentplayer.name + "'s turn.\n")
        while choice not in ('1','2'):
            choice = input("Choose a card from your hand(1) or the deck(2) or call out Uno(3):\n")
            if choice == '3':
                if len(self.currentplayer.cards) > 2:
                    print("You don't need to call out uno now.\n")
                elif uno == True:
                    print("Shut up!")
                else:
                    print("UNO!!!!!")
                    uno = True
        if choice == '1':
            if len(self.currentplayer.cards) == 2 and uno == False:
                print("\nYou didn't call out Uno!")
                print("\nYou have been penalised 4 cards.")
                self.deck.deal([self.currentplayer], per_hand=4)
            cardname = input("Choose a card:\n")
            self.currentcard, valid_card, self.currentplayer = self.currentplayer.next_move(cardname, self.currentcard, self.currentplayer, self.deck, self.hands)
            
            while self.currentcard == None:
                self.currentcard = prevcurrentcard
                cardname = input("Choose another card.\n") 
                self.currentcard, valid_card, self.currentplayer = self.currentplayer.next_move(cardname, self.currentcard, self.currentplayer, self.deck, self.hands)
        elif choice == '2':
            self.currentcard, valid_card, self.currentplayer, self.deck = self.currentplayer.deal_from_deck(self.deck, self.currentcard, self.currentplayer, self.hands)

        if(valid_card != prevcurrentcard):
            self.discard.add(valid_card)
        print(self.currentcard)
        print("\n")
        print(self.player)
        print(self.dealer)

    #Switches turns
    def switch_turns(self):
        self.currentplayer = self.hands[(self.hands.index(self.currentplayer)+1)%2]
        return self.currentplayer

    #Fills deck if it becomes less than 8 cards
    def fill_deck(self):
            self.deck.deal([discard],per_hand=8)
            self.deck = self.discard
            self.deck.shuffle()

    #The game
    def play(self):
        print(self.player)
        print(self.dealer)
        print(self.currentcard)
        gameover = False
        currentplayer = self.player
        while gameover == False:
            self.player_move(currentplayer)
            if self.currentplayer.cards == []:
                gameover = True
                if self.currentplayer == self.player:
                    print("You won!")
                else:
                    print("You lost!")
            currentplayer = self.switch_turns()
            if len(self.deck.cards) < 9:
                self.fill_deck()
def main():

    #Receives the name of the player
    player_name = input("Enter your name: ")
    player = Unoplayer(player_name)
    dealer = Unoplayer("Dealer")
    hands = [player,dealer]

    game = Unogame(hands)
    game.play()

main()

input("\n\nPress enter key to exit.\n\n")
    
