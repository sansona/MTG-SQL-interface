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
    im_url: str


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

    def subset_by_string(self, search_string: str, text='all'):
        '''
        Get subset of deck that contains search string

        Args:
                search_string (str): type of card
                text (str): where in Deck data to perform string comparison:
                options are ('type, text', 'all')
        Returns:
                (Deck): subset of original Deck with search_string
        '''
        subset_list = []
        if text == 'type':
            for c in self.cards:
                if any(search_string in str_ for str_ in c.card_type):
                    subset_list.append(c)
        elif text == 'text':
            for c in self.cards:
                if any(search_string in str_ for str_ in c.text):
                    subset_list.append(c)
        else:
            for c in self.cards:
                if any(search_string in str_ for str_ in (c.text, c.card_type)):
                    subset_list.append(c)

        subset = Deck(f"{search_string}_subset", subset_list)

        return subset

    def subset_by_cmc(self, cost: int):
        '''
        return distribution of cmc greater and less than cost

        Args:
                cost (int): mana cost to be compared against
        Returns:
                (dict): containing subsets corresponding to equal to, below, and
                above cost
        '''
        equal = []
        below = []
        above = []

        for c in self.cards:
            if c.cmc == cost:
                equal.append(c)
            elif c.cmc < cost:
                below.append(c)
            else:
                above.append(c)

        equal = Deck(f"cmc_{cost}", equal)
        below = Deck(f"cmc_below_{below}", below)
        above = Deck(f"cmc_above_{below}", above)

        dist = {'equal': equal, 'below': below, 'above': above}
        return dist

    def subset_by_color(self, colors: tuple, only=False):
        '''
        Get subset of deck that shares color identity
        WIP

        Args:
                colors (tuple): color identity
                only (bool): if True, only subset if color identity perfectly
                matches
        Returns:
                (Deck): subset of original Deck sharing color_identity
        '''
        subset = []
        for c in self.cards:
            color_id = sorted(c.color_identity)
            breakpoint()
            if any(c.color_identity) in colors:
                subset.append(c)

        subset = Deck(f"{colors}_subset", subset)

        return subset

    def get_images(self):
        pass
