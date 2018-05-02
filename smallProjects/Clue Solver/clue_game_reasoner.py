"""
Make sure to fill in the following information before submitting your
assignment. Your grade may be affected if you leave it blank!
For usernames, make sure to use your Whitman usernames (i.e. exleyas). 
File name: clue_game_reasoner.py
Author username(s): ashleygw
Date: March 28 2018
"""
'''clue_game_reasoner.py - project skeleton for a propositional reasoner
for the game of Clue.  Unimplemented portions have the comment "TO
BE IMPLEMENTED AS AN EXERCISE".  The reasoner does not include
knowledge of how many cards each player holds.
Originally by Todd Neller
Ported to Python by Dave Musicant
Ported to Python3 by Andy Exley

Copyright (C) 2008 Dave Musicant
Copyright (C) 2018 Andy Exley

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Information about the GNU General Public License is available online at:
  http://www.gnu.org/licenses/
To receive a copy of the GNU General Public License, write to the Free
Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
02111-1307, USA.'''

import SATSolver
import itertools

# Initialize important variables

CASE_FILE = "cf"
POSSIBLE_PLAYERS = ["sc", "mu", "wh", "gr", "pe", "pl"]
POSSIBLE_CARD_LOCATIONS = POSSIBLE_PLAYERS + [CASE_FILE]
SUSPECTS = ["mu", "pl", "gr", "pe", "sc", "wh"]
WEAPONS = ["kn", "ca", "re", "ro", "pi", "wr"]
ROOMS = ["ha", "lo", "di", "ki", "ba", "co", "bi", "li", "st"]
CARDS = SUSPECTS + WEAPONS + ROOMS

class ClueGameReasoner:
    '''This class represents a clue game reasoner, a tool that can be used
    to track the information during a game of clue and deduce information
    about the game. (Hopefully help you win!)
    '''

    def __init__(self, player_order, card_nums = None):
        '''init for a particular clue game.
            player_order is a list of strings of players in the order that they
            are sitting around the table. Note: This may not include all the suspects,
            as there may be fewer than 6 players in any given game.

            card_nums is a list of numbers of cards in players' hands. It is 
            possible that different players have different numbers of cards! 
        '''
        self.players = player_order
        self.clauses = []
    
        # Each card is in at least one place (including case file).
        for c in CARDS:
            clause = []
            for p in POSSIBLE_CARD_LOCATIONS:
                clause.append(get_pair_num_from_names(p,c))
            self.clauses.append(clause)

        # TO BE IMPLEMENTED AS AN EXERCISE:

        # A card cannot be in two places.
        for c in CARDS:
            clause = []
            for p in POSSIBLE_CARD_LOCATIONS:
                #Add negative of player hand to clause
                clause.append(-get_pair_num_from_names(p,c))
            # Builds all combinations of two players per card (is negative)
            notOrList = list(itertools.permutations(clause, 2))
            # for n1,n2 in notOrList:
            #     print([n1,n2])
            for n1,n2 in notOrList:
                self.clauses.append([n1,n2])

        # At least one card of each category is in the case file.
        clause = []
        for c in WEAPONS:
            clause.append(get_pair_num_from_names("cf",c))
        self.clauses.append(clause)
        clause = []
        for c in ROOMS:
            clause.append(get_pair_num_from_names("cf",c))
        self.clauses.append(clause)
        clause = []
        for c in SUSPECTS:
            clause.append(get_pair_num_from_names("cf",c))
        self.clauses.append(clause)
        # No two cards in each category can both be in the case file.
        for l in [WEAPONS,SUSPECTS,ROOMS]:
            clause = []
            for c in l:
                clause.append(-get_pair_num_from_names("cf",c))
            notOrList = list(itertools.permutations(clause, 2))
            for n1,n2 in notOrList:
                #print([n1,n2])
                self.clauses.append([n1,n2])


    def add_hand(self, player_name, hand_cards):
        '''Add the information about the given player's hand to the KB'''
        # TO BE IMPLEMENTED AS AN EXERCISE
        for c in hand_cards:
            self.clauses.append([get_pair_num_from_names(player_name, c)])

    def suggest(self, suggester, c1, c2, c3, refuter, cardshown = None):
        '''Add information about a given suggestion to the KB'''
        # TO BE IMPLEMENTED AS AN EXERCISE
        i = (self.players.index(suggester) + 1) % len(self.players)
        while True:
            if self.players[i] == suggester:
                return
            if self.players[i] != refuter:
                for c in [c1,c2,c3]:
                    self.clauses.append([-get_pair_num_from_names(self.players[i],c)])
            else:
                if cardshown:
                    self.clauses.append([get_pair_num_from_names(refuter, cardshown)])
                self.clauses.append([get_pair_num_from_names(refuter,c) for c in [c1,c2,c3]])
                return
            
            i = (i + 1) % len(self.players)

    def accuse(self, accuser, c1, c2, c3, iscorrect):
        '''Add information about a given accusation to the KB'''
        # TO BE IMPLEMENTED AS AN EXERCISE
        if not iscorrect:
            self.clauses.append([-get_pair_num_from_names("cf",c) for c in [c1,c2,c3]])
        else:
            for c in [c1,c2,c3]:
                self.clauses.append([get_pair_num_from_names("cf",c)])

    def print_notepad(self):
        for player in self.players:
            print('\t'+ player, end='')
        print('\t'+ CASE_FILE)
        for card in CARDS:
            print(card,'\t',end='')
            for player in self.players:
                print(query_string(query(player, card, self.clauses)),'\t',end='')
            print(query_string(query(CASE_FILE, card, self.clauses)))

def get_pair_num_from_names(player,card):
    '''
        Returns the integer that corresponds to the proposition that
         the given card is in the given player's hand

        Preconditions:
            player is a string representation of a valid player or case file
            card is a string representation of a valid card
    '''
    assert isinstance(player, str), 'player argument should be a string'
    assert isinstance(card, str), 'card argument should be a string'
    assert player in POSSIBLE_CARD_LOCATIONS, 'Given player ' +player+ ' is not a valid location'
    assert card in CARDS, 'Given card ' + card + ' is not a valid card'

    return get_pair_num_from_positions(POSSIBLE_CARD_LOCATIONS.index(player),
                                   CARDS.index(card))

def get_pair_num_from_positions(player,card):
    '''Helper function to generate proposition literals.'''
    return player * len(CARDS) + card + 1

def query(player,card,clauses):
    return SATSolver.testLiteral(get_pair_num_from_names(player,card),clauses)

def query_string(returnCode):
    if returnCode == True:
        return 'Y'
    elif returnCode == False:
        return 'N'
    else:
        return '-'

def play_clue_game1():
    # the game begins! add players to the game
    cgr = ClueGameReasoner(["sc", "mu", "wh", "gr", "pe", "pl"])

    # Add information about our hand: We are Miss Scarlet,
    # and we have the cards Mrs White, Library, Study
    cgr.add_hand("sc",["wh", "li", "st"])

    # We go first, we suggest that it was Miss Scarlet, 
    # with the Rope in the Lounge. Colonel Mustard refutes us 
    # by showing us the Miss Scarlet card.
    cgr.suggest("sc", "sc", "ro", "lo", "mu", "sc")

    # Mustard takes his turn. He suggests that it was Mrs. Peacock,
    # in the Dining Room with the Lead Pipe.
    # Mrs. White and Mr. Green cannot refute, but Mrs. Peacock does.
    cgr.suggest("mu", "pe", "pi", "di", "pe", None)

    # Mrs. White takes her turn
    cgr.suggest("wh", "mu", "re", "ba", "pe", None)

    # and so on...
    cgr.suggest("gr", "wh", "kn", "ba", "pl", None)
    cgr.suggest("pe", "gr", "ca", "di", "wh", None)
    cgr.suggest("pl", "wh", "wr", "st", "sc", "wh")
    cgr.suggest("sc", "pl", "ro", "co", "mu", "pl")
    cgr.suggest("mu", "pe", "ro", "ba", "wh", None)
    cgr.suggest("wh", "mu", "ca", "st", "gr", None)
    cgr.suggest("gr", "pe", "kn", "di", "pe", None)
    cgr.suggest("pe", "mu", "pi", "di", "pl", None)
    cgr.suggest("pl", "gr", "kn", "co", "wh", None)
    cgr.suggest("sc", "pe", "kn", "lo", "mu", "lo")
    cgr.suggest("mu", "pe", "kn", "di", "wh", None)
    cgr.suggest("wh", "pe", "wr", "ha", "gr", None)
    cgr.suggest("gr", "wh", "pi", "co", "pl", None)
    cgr.suggest("pe", "sc", "pi", "ha", "mu", None)
    cgr.suggest("pl", "pe", "pi", "ba", None, None)
    cgr.suggest("sc", "wh", "pi", "ha", "pe", "ha")

    # aha! we have discovered that the lead pipe is the correct weapon
    # if you print the notepad here, you should see that we know that
    # it is in the case file. But it looks like the jig is up and 
    # everyone else has figured this out as well...

    cgr.suggest("wh", "pe", "pi", "ha", "pe", None)
    cgr.suggest("pe", "pe", "pi", "ha", None, None)
    cgr.suggest("sc", "gr", "pi", "st", "wh", "gr")
    cgr.suggest("mu", "pe", "pi", "ba", "pl", None)
    cgr.suggest("wh", "pe", "pi", "st", "sc", "st")
    cgr.suggest("gr", "wh", "pi", "st", "sc", "wh")
    cgr.suggest("pe", "wh", "pi", "st", "sc", "wh")

    # At this point, we are still unsure of whether it happened
    # in the kitchen, or the billiard room. printing our notepad
    # here should reflect that we know all the other information
    cgr.suggest("pl", "pe", "pi", "ki", "gr", None)

    # Aha! Mr. Green must have the Kitchen card in his hand
    print('Before accusation: should show a single solution.')
    cgr.print_notepad()
    print()
    cgr.accuse("sc", "pe", "pi", "bi", True)
    print('After accusation: if consistent, output should remain unchanged.')
    cgr.print_notepad()

def play_clue_game2():
    '''This game recorded by Brooke Taylor and played by Sean Miller,
    George Ashley, Ben Limpich, Melissa Kohl and Andy Exley. Thanks to all!
    '''
    cgr = ClueGameReasoner(["sc","mu","wh","gr","pe","pl"])
    cgr.add_hand("wh",["kn","ro","ki"])

    # all suggestions
    cgr.suggest("mu", "mu", "di", "pi", "pe", None)
    cgr.suggest("wh", "pl", "ca", "ba", "pe", "ba")
    cgr.suggest("gr", "pe", "ba", "ro", "pe", None)
    cgr.suggest("pe", "ki", "sc", "re", "wh", "ki")
    cgr.suggest("sc", "wh", "st", "ro", "mu", None)
    cgr.suggest("mu", "lo", "pl", "kn", "wh", "kn")
    cgr.suggest("wh", "li", "re", "pl", "gr", "re")
    cgr.suggest("pe", "st", "sc", "wr", "mu", None)
    cgr.suggest("pl", "bi", "gr", "wr", "sc", None)
    cgr.suggest("mu", "co", "pe", "ca", "gr", None)
    cgr.suggest("pe", "lo", "mu", "ro", "pl", None)
    cgr.suggest("pl", "co", "mu", "wr", "gr", None)
    cgr.suggest("sc", "ha", "ro", "pe", "wh", "ro")
    cgr.suggest("mu", "pe", "pi", "ba", "pe", None)
    cgr.suggest("wh", "sc", "pi", "ha", "pe", "sc")
    cgr.suggest("pe", "pl", "wr", "co", "pl", None)
    cgr.suggest("pl", "ba", "mu", "wr", "pe", None)
    cgr.suggest("sc", "st", "pi", "pe", "mu", None)
    cgr.suggest("wh", "ca", "st", "gr", "sc", "ca")
    cgr.suggest("gr", "sc", "ki", "wr", "pe", None)
    cgr.suggest("pe", "ki", "mu", "wr", "wh", "ki")
    cgr.suggest("mu", "st", "gr", "wr", "sc", None)
    cgr.suggest("wh", "gr", "ha", "wr", "sc", "ha")
    cgr.suggest("pe", "pe", "st", "wr", "mu", None)
    cgr.suggest("pl", "ki", "gr", "wr", "sc", None)
    cgr.suggest("sc", "li", "wr", "pe", "pl", None)
    cgr.suggest("wh", "di", "pe", "wr", None, None)

    cgr.print_notepad()
    # final accusation
    cgr.accuse("wh", "di", "pe", "wr", True)

def play_clue_game3():
    '''Same as clue game 2, but from ms. peacock's perspective'''
    cgr = ClueGameReasoner(["sc","mu","wh","gr","pe","pl"])
    cgr.add_hand("pe",["sc","mu","ba"])
    cgr.suggest("mu", "mu", "di", "pi", "pe", "mu")
    cgr.suggest("wh", "pl", "ca", "ba", "pe", "ba")
    cgr.suggest("gr", "pe", "ba", "ro", "pe", "ba")
    cgr.suggest("pe", "ki", "sc", "re", "wh", "ki")
    cgr.suggest("sc", "wh", "st", "ro", "mu", None)
    cgr.suggest("mu", "lo", "pl", "kn", "wh", None)
    cgr.suggest("wh", "li", "re", "pl", "gr", None)
    cgr.suggest("pe", "st", "sc", "wr", "mu", "st")
    cgr.suggest("pl", "bi", "gr", "wr", "sc", None)
    cgr.suggest("mu", "co", "pe", "ca", "gr", None)
    cgr.suggest("pe", "lo", "mu", "ro", "pl", "lo")
    cgr.suggest("pl", "co", "mu", "wr", "gr", None)
    cgr.suggest("sc", "ha", "ro", "pe", "wh", None)
    cgr.suggest("mu", "pe", "pi", "ba", "pe", "ba")
    cgr.suggest("wh", "sc", "pi", "ha", "pe", "sc")
    cgr.suggest("pe", "pl", "wr", "co", "pl", "pl")
    cgr.suggest("pl", "ba", "mu", "wr", "pe", "ba")
    cgr.suggest("sc", "st", "pi", "pe", "mu", None)
    cgr.suggest("wh", "ca", "st", "gr", "sc", None)
    cgr.suggest("gr", "sc", "ki", "wr", "pe", "sc")
    cgr.suggest("pe", "ki", "mu", "wr", "wh", "ki")
    cgr.suggest("mu", "st", "gr", "wr", "sc", None)
    cgr.suggest("wh", "gr", "ha", "wr", "sc", None)
    cgr.suggest("pe", "pe", "st", "wr", "mu", None)
    cgr.suggest("pl", "ki", "gr", "wr", "sc", None)
    cgr.suggest("sc", "li", "wr", "pe", "pl", None)

    # right before Mrs. White ends the game, I still
    # don't know what room it is in. :(
    cgr.print_notepad()
    cgr.suggest("wh", "di", "pe", "wr", None, None)
    cgr.accuse("wh", "di", "pe", "wr", True)

# Change which game gets called down here if you want to test 
# other games
if __name__ == '__main__':
    play_clue_game1()