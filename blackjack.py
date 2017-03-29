# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
global player_hand, dealer_hand, game_deck


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

        
# define hand class
        
class Hand:
    def __init__(self):
        self.hand_list = []
        
    def __str__(self):
        self.hand_string = 'hand contains '
        for card in self.hand_list:
            self.hand_string = self.hand_string + card.get_suit() + card.get_rank() + " "
        return self.hand_string.rstrip(' ')
        
    def add_card(self, card):
        self.hand_list.append(card)
    
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        contains_ace = False
        value = 0
        for card in self.hand_list:
            if card.get_rank() == 'A':
                contains_ace = True
            value += VALUES[card.get_rank()]
        if value <= 11 and contains_ace == True:
            value += 10
        return value

    def draw(self, canvas, pos):
        for card in self.hand_list:
            card_loc = (CARD_SIZE[0] / 2 + CARD_SIZE[0] * RANKS.index(card.get_rank()), 
                        CARD_SIZE[1] / 2 + CARD_SIZE[1] * SUITS.index(card.get_suit()))
            canvas.draw_image(card_images, card_loc, 
                                  CARD_SIZE,
                                     [pos[0] + CARD_CENTER[0],
                                         pos[1] + CARD_CENTER[1]], 
                                             CARD_SIZE)
            pos[0] += CARD_SIZE[0] + 10
             
# define deck class 
class Deck:
    def __init__(self):
        self.deck_list = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck_list.append(Card(suit,rank))  
                
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck_list)

    def deal_card(self):
        return self.deck_list.pop(-1)
    
    def __str__(self):
        self.deck_str = "Deck contains "
        for card in self.deck_list:
            self.deck_str = self.deck_str + card.get_suit() + card.get_rank() + " " 
        return  self.deck_str
    
#define event handlers for buttons
def deal():
    global outcome, in_play, game_deck, player_hand, dealer_hand, score
    outcome = ''
    if in_play == True:
        score -= 1
        outcome = 'Player forfeit. Dealer wins. New Deal?' 
        in_play = False
    # your code goes here
    in_play = True
    game_deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()
    game_deck.shuffle()
    for i in range(2):
        if i < 2:
            player_hand.add_card(game_deck.deal_card())
            dealer_hand.add_card(game_deck.deal_card())
    print "Player " + str(player_hand)
    print "Dealer " + str(dealer_hand)
    print "Player has " + str(player_hand.get_value())
    print "Dealer has " + str(dealer_hand.get_value())

def hit():
    global outcome, in_play, game_deck, player_hand, dealer_hand, score
    # if the hand is in play, hit the player
    if in_play == True and player_hand.get_value() <= 21:
        player_hand.add_card(game_deck.deal_card())
        print "Player " + str(player_hand)
        print "Player has " + str(player_hand.get_value())
    if in_play == True and player_hand.get_value() > 21:
        in_play = False
        outcome = "You have busted! Dealer wins. New deal?"
        score -= 1
        print outcome
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global in_play, score, outcome
    dealer_busted = False
    if player_hand.get_value() > 21:
        outcome = "You have busted! Dealer wins. New deal?"
        print outcome
        
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    while in_play == True and dealer_hand.get_value() < 17:
        dealer_hand.add_card(game_deck.deal_card())
        print "Dealer " + str(dealer_hand)
        print "Dealer has " + str(dealer_hand.get_value())
    if dealer_hand.get_value() > 21 and in_play == True:
        print "Dealer busted!"
        dealer_busted = True
        outcome = "Dealer has busted" + ". You win! New deal?"
        score += 1
        print outcome
        
    # assign a message to outcome, update in_play and score
    if in_play == True and dealer_hand.get_value() >= player_hand.get_value() and dealer_busted == False:
        outcome = "Dealer: " + str(dealer_hand.get_value()) + " You: " +  str(player_hand.get_value()) + ". You lose. New Deal?"
        score -= 1
        print outcome
    if in_play == True and dealer_hand.get_value() < player_hand.get_value():
        in_play = False
        outcome = "Dealer: " + str(dealer_hand.get_value()) + " You: " +  str(player_hand.get_value()) + ". You win! New Deal?"
        score += 1
        print outcome
    in_play = False

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global player_hand
    player_hand.draw(canvas, [100, 400])
    dealer_hand.draw(canvas, [100, 110])
    canvas.draw_text(str(outcome), (25, 275), 32, 'Black')
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, 
                                  CARD_BACK_SIZE,
                                     [100 + CARD_BACK_SIZE[0] / 2 ,
                                         110 + CARD_BACK_SIZE[1] / 2], 
                                             CARD_BACK_SIZE)
    canvas.draw_text("Score: " + str(score), (450, 55), 32, 'Yellow')
    canvas.draw_text("Blackjack", (190, 335), 55, 'White')
    

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()


# remember to review the gradic rubric