'''
repository for dataclasses
'''
from typing import List
from dataclasses import dataclass


@dataclass
class Card:
    """
    base class for Deck object

    Args:
        name (str): Gatherer name of card
        count (int): number of card in deck
        mana_cost (str): cost to cast card
        cmc (int): converted mana cost of card
        color_identity (str): commander color ID
        card_type (tuple): type(s) of spell
        text (str): oracle text of card
    """

    name: str
    count: int
    mana_cost: str
    cmc: int
    color_identity: str
    card_type: tuple
    text: str


@dataclass
class Deck:
    """
    class containing deck name and list of all Cards

    Args:
        name (str): name of deck
        cards (List of Cards): list containing Card objects
    """

    name: str
    cards: List[Card]

    def n_cards(self):
        '''
        returns number of total cards in deck
        '''
        n = 0
        for card in self.cards:
            n += card.count

        return int(n)

    def n_unique_cards(self):
        '''
        returns number of unique Cards in Deck
        '''
        return len(self.cards)

    def n_card_type(self, type_string):
        '''
        returns number of cards containing type in card_type param

        Args:
            type_string (str): type of card
        Returns:
            (int): number of cards sharing type
        '''
        n = 0
        for c in self.cards:
            if any(type_string in str_ for str_ in c.card_type):
                n += 1

        return n

    def n_keyword(self, keyword):
        '''
        return number of cards containing keyword in oracle text

        Args:
            keyword (str): string to be searched for
        Returns:
            (int): number of cards containing keyword
        '''
        n = 0
        for c in self.cards:
            if keyword in c.text:
                n += 1

        return n

    def cmc_distribution(self, cost):
        '''
        return distribution of cmc greater and less than cost

        Args:
            cost (int): mana cost to be compared against
        Returns:
            (int, int, int): number of cards with cmc==cost, number of cards
            with cmc < cost, number of cards with cmc > cost
        '''
        dist = [0, 0, 0]
        for c in self.cards:
            if c.cmc == cost:
                dist[0] += c.count
            elif c.cmc < cost:
                dist[1] += c.count
            else:
                dist[2] += c.count

        return dist

    def average_cmc(self):
        '''
        return average cmc of cards in deck
        '''
        nonlands = [c for c in self.cards if 'Land,' not in c.card_type]

        # count won't always == 1, implement this way to handle multiples
        n_nonlands = 0
        total_mc = 0
        for n in nonlands:
            n_nonlands += n.count
            total_mc += n.count*n.cmc

        return total_mc/n_nonlands
