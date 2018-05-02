'''clue_reasoner.py - project skeleton for a propositional reasoner
for the game of Clue.  Unimplemented portions have the comment "TO
BE IMPLEMENTED AS AN EXERCISE".  The reasoner does not include
knowledge of how many cards each player holds.
Originally by Todd Neller
Ported to Python by Dave Musicant
Ported to Python3 by Andy Exley

Copyright (C) 2008 Dave Musicant
Copyright (C) 2016 Andy Exley

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

# Initialize important variables
case_file = "cf"
players = ["sc", "mu", "wh", "gr", "pe", "pl"]
extended_players = players + [case_file]
suspects = ["mu", "pl", "gr", "pe", "sc", "wh"]
weapons = ["kn", "ca", "re", "ro", "pi", "wr"]
rooms = ["ha", "lo", "di", "ki", "ba", "co", "bi", "li", "st"]
cards = suspects + weapons + rooms

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
    assert player in extended_players, 'Given player ' +player+ ' is not a valid location'
    assert card in cards, 'Given card ' + card + ' is not a valid card'

    return get_pair_num_from_positions(extended_players.index(player),
                                   cards.index(card))

def get_pair_num_from_positions(player,card):
    return player*len(cards) + card + 1

# TO BE IMPLEMENTED AS AN EXERCISE
def initial_clauses():
    clauses = []

    # Each card is in at least one place (including case file).
    for c in cards:
        clause = []
        for p in extended_players:
            clause.append(get_pair_num_from_names(p,c))
        clauses.append(clause)

    # A card cannot be in two places.

    # At least one card of each category is in the case file.

    # No two cards in each category can both be in the case file.

    return clauses

# TO BE IMPLEMENTED AS AN EXERCISE
def hand(player,hand_cards):
    return []


# TO BE IMPLEMENTED AS AN EXERCISE
def suggest(suggester,card1,card2,card3,refuter,cardShown):
    return []

# TO BE IMPLEMENTED AS AN EXERCISE
def accuse(accuser,card1,card2,card3,isCorrect):
    return []

def query(player,card,clauses):
    return SATSolver.testLiteral(get_pair_num_from_names(player,card),clauses)

def query_string(returnCode):
    if returnCode == True:
        return 'Y'
    elif returnCode == False:
        return 'N'
    else:
        return '-'

def print_notepad(clauses):
    for player in players:
        print('\t'+ player, end='')
    print('\t'+ case_file)
    for card in cards:
        print(card,'\t',end='')
        for player in players:
            print(query_string(query(player,card,clauses)),'\t',end='')
        print(query_string(query(case_file,card,clauses)))

def play_clue():
    # the game begins! add initial rules to the game
    clauses = initial_clauses()

    # if you are going to play your own instance of Clue, then you
    # would change the information from here going forward.

    # Add information about our hand: We are Miss Scarlet,
    # and we have the cards Mrs White, Library, Study
    clauses.extend(hand("sc",["wh", "li", "st"]))

    # We go first, we suggest that it was Miss Scarlet, 
    # with the Rope in the Lounge. Colonel Mustard refutes us 
    # by showing us the Miss Scarlet card.
    clauses.extend(suggest("sc", "sc", "ro", "lo", "mu", "sc"))

    # Mustard takes his turn
    clauses.extend(suggest("mu", "pe", "pi", "di", "pe", None))

    # White takes her turn
    clauses.extend(suggest("wh", "mu", "re", "ba", "pe", None))

    # and so on...
    clauses.extend(suggest("gr", "wh", "kn", "ba", "pl", None))
    clauses.extend(suggest("pe", "gr", "ca", "di", "wh", None))
    clauses.extend(suggest("pl", "wh", "wr", "st", "sc", "wh"))
    clauses.extend(suggest("sc", "pl", "ro", "co", "mu", "pl"))
    clauses.extend(suggest("mu", "pe", "ro", "ba", "wh", None))
    clauses.extend(suggest("wh", "mu", "ca", "st", "gr", None))
    clauses.extend(suggest("gr", "pe", "kn", "di", "pe", None))
    clauses.extend(suggest("pe", "mu", "pi", "di", "pl", None))
    clauses.extend(suggest("pl", "gr", "kn", "co", "wh", None))
    clauses.extend(suggest("sc", "pe", "kn", "lo", "mu", "lo"))
    clauses.extend(suggest("mu", "pe", "kn", "di", "wh", None))
    clauses.extend(suggest("wh", "pe", "wr", "ha", "gr", None))
    clauses.extend(suggest("gr", "wh", "pi", "co", "pl", None))
    clauses.extend(suggest("pe", "sc", "pi", "ha", "mu", None))
    clauses.extend(suggest("pl", "pe", "pi", "ba", None, None))
    clauses.extend(suggest("sc", "wh", "pi", "ha", "pe", "ha"))

    # aha! we have discovered that the lead pipe is the correct weapon
    # if you print the notepad here, you should see that we know that
    # it is in the case file. But it looks like the jig is up and 
    # everyone else has figured this out as well...

    clauses.extend(suggest("wh", "pe", "pi", "ha", "pe", None))
    clauses.extend(suggest("pe", "pe", "pi", "ha", None, None))
    clauses.extend(suggest("sc", "gr", "pi", "st", "wh", "gr"))
    clauses.extend(suggest("mu", "pe", "pi", "ba", "pl", None))
    clauses.extend(suggest("wh", "pe", "pi", "st", "sc", "st"))
    clauses.extend(suggest("gr", "wh", "pi", "st", "sc", "wh"))
    clauses.extend(suggest("pe", "wh", "pi", "st", "sc", "wh"))

    # At this point, we are still unsure of whether it happened
    # in the kitchen, or the billiard room. printing our notepad
    # here should reflect that we know all the other information
    clauses.extend(suggest("pl", "pe", "pi", "ki", "gr", None))

    # Aha! Mr. Green must have the Kitchen card in his hand
    print('Before accusation: should show a single solution.')
    print_notepad(clauses)
    print()
    clauses.extend(accuse("sc", "pe", "pi", "bi", True))
    print('After accusation: if consistent, output should remain unchanged.')
    print_notepad(clauses)

if __name__ == '__main__':
    play_clue()