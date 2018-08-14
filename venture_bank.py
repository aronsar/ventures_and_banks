# Rule clarification: if you play 5 ventures and 2 banks, the 5 ventures 
# are worth 5 money, the first bank is worth 6 money, and the second bank 
# is worth 7 money, for a total of 18 money. This is because treasures are 
# played *one at a time*. So when the first bank is played, there are a 
# total of *6* treasures in play, whereas when the second bank is played,
# there are a total of *7* treasures in play. This is reflected in the sim.

import random
from copy import deepcopy

deck_size = 25
num_simulations = 10000
venture_bank_combinations = [[10,0], [10,1], [10,2], [10,3], [10,4], [10,5], [10,6], [10,7], [10, 8], [10, 9], [10, 10]]

# FIXME: these variables should really not be global, I just suck at Python
total_money = 0
treasures_played_so_far = 0
money_so_far = 0

class Deck:
  def __init__(self, num_ventures, num_banks):
    self.cards = []
    self.cards += num_ventures * [Card('venture')]
    self.cards += num_banks * [Card('bank')]
    num_other = deck_size - num_ventures - num_banks
    #num_other = 5
    self.cards += num_other * [Card('other')]
    
  def shuffle(self):
    random.shuffle(self.cards)
    return self
      
  def draw(self, num_cards):
    cards_drawn = []
    for _ in range(num_cards):
      try:
        cards_drawn.append(self.cards.pop(0))
      except IndexError: # deck has run out of cards
        return [Card('deck_empty')]
        
    return cards_drawn
    
  def venture_played(self):
    global treasures_played_so_far, money_so_far
    treasures_played_so_far += 1
    money_so_far += 1
    card_drawn = self.draw(1)[0]
    
    # keep drawing cards as long as there are cards in the deck and
    # the card you draw is not a treasure
    while not card_drawn.deck_empty() and not card_drawn.is_treasure():
      card_drawn = self.draw(1)[0]
      
    if card_drawn == Card('venture'):
      self.venture_played()
      
    elif card_drawn == Card('bank'):
      self.bank_played()
      
  def bank_played(self):
    global treasures_played_so_far, money_so_far
    treasures_played_so_far += 1
    money_so_far += treasures_played_so_far
    
  def clean_up(self):
    global total_money
    total_money += money_so_far
    
class Hand:
  def __init__(self, cards):
    self.cards = cards
    
  def has_ventures(self):
    has_ventures = False
    for card in self.cards:
      if card.type == 'venture':
        has_ventures = True
    return has_ventures
    
  def has_banks(self):
    has_banks = False
    for card in self.cards:
      if card.type == 'bank':
        has_banks = True
    return has_banks
    
  def play_venture(self, deck):
    deck.venture_played()
    self.cards.remove(Card('venture'))
    
  def play_bank(self, deck):
    deck.bank_played()
    self.cards.remove(Card('bank'))

class Card:
  def __init__(self, type):
    self.type = type
  
  def __eq__(self, other):
    return self.type == other.type
  
  def is_treasure(self):
    if self.type == 'venture' or self.type == 'bank':
      return True
    else:
      return False
  
  def deck_empty(self):
    if self.type == 'deck_empty':
      return True
    else:
      return False
      
def main():
  global total_money, treasures_played_so_far, money_so_far
  
  print("Deck size is: %d" % deck_size)
  print("Number of simulations: %d" % num_simulations)
  
  #import pdb; pdb.set_trace()
  for [num_ventures, num_banks] in venture_bank_combinations:
    total_money = 0
    unshuffled_deck = Deck(num_ventures, num_banks)
    for _ in range(num_simulations):
      deck = deepcopy(unshuffled_deck.shuffle())
      hand = Hand(deck.draw(5))
      
      treasures_played_so_far = 0
      money_so_far = 0
      
      while hand.has_ventures():
        hand.play_venture(deck)
      
      while hand.has_banks():
        hand.play_bank(deck)
      
      deck.clean_up()
    print("%d ventures and %d banks expect %.2f money in a turn." % \
          (num_ventures, num_banks, total_money / num_simulations))

if __name__ == '__main__':
  main()