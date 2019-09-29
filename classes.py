"""
repository for dataclasses
"""
import os
import time
import shutil
from pathlib import Path
from io import BytesIO
from typing import List
from dataclasses import dataclass
from PIL import Image
import requests


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
        """
        returns number of total cards in deck
        """
        n = 0
        for card in self.cards:
            n += card.count

        return int(n)

    def n_unique_cards(self):
        """
        returns number of unique Cards in Deck
        """
        return len(self.cards)

    def average_cmc(self):
        """
        return average cmc of cards in deck
        """
        nonlands = [c for c in self.cards if "Land," not in c.card_type]

        # count won't always == 1, implement this way to handle multiples
        n_nonlands = 0
        total_mc = 0
        for n in nonlands:
            n_nonlands += n.count
            total_mc += n.count * n.cmc

        return total_mc / n_nonlands

    def cmc_histogram(self):
        """
        returns data for cmc distribution of deck

        Args:
            None
        Returns:
            (Dict): in format {cmc (int): Deck w/ cmc=cmc}
            (Dict): in format {cmc (int): count cmc}
        """
        dist = {}
        for c in self.cards:
            if c.cmc not in dist:
                dist[c.cmc] = [c]
            else:
                dist[c.cmc].append(c)
        print(dist)
        # filter out lands w/ cmc=0 since don't want in cmc count
        dist[0] = [m for m in dist[0] if 'Land,' in m.card_type]

        count = {}
        for cmc_val in [*dist]:
            count[cmc_val] = len(dist[cmc_val])
        return dist, count

    def subset_by_string(self, search_string: str, text="text"):
        """
        get subset of deck that contains search string

        Args:
            search_string (str): type of card
            text (str): where in Deck data to perform string comparison:
            options are ('type, text')
        Returns:
            (Deck): subset of original Deck with search_string
        """
        subset_list = []
        if text == "type":
            for c in self.cards:
                if any(search_string in str_ for str_ in c.card_type):
                    subset_list.append(c)
        elif text == "text":
            for c in self.cards:
                if any(search_string in str_ for str_ in c.text):
                    subset_list.append(c)

        subset = Deck(f"{search_string}_subset", subset_list)

        return subset

    def subset_by_cmc(self, cost: int):
        """
        return distribution of cmc greater and less than cost

        Args:
            cost (int): mana cost to be compared against
        Returns:
            (dict): containing subsets corresponding to equal to, below, and
            above cost
        """
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

        dist = {"equal": equal, "below": below, "above": above}
        return dist

    def subset_by_color(self, colors: list, exact_colors=False):
        """
        get subset of deck that shares color identity

        Args:
            colors (list): color identity in form ['W', 'B'
            exact_colors (bool): if True, only subset if identity perfectly
                    matches
        Returns:
            (Deck): subset of original Deck sharing color_identity
        """
        colors = sorted(colors)
        subset_list = []
        for c in self.cards:
            # flatten color_id to list, sort
            color_id = [j for k in c.color_identity for j in k]
            color_id = sorted(color_id)

            if exact_colors:
                if color_id == colors:
                    subset_list.append(c)
            else:
                # if any colors in color_id in colors, save card
                if any(i in color_id for i in colors):
                    subset_list.append(c)

        subset = Deck(f"{colors}_subset", subset_list)

        return subset

    def store_images(self, dirname):
        """
        store card image files in new directory

        Args:
            dirname (str): name of dir
        Return:
            (Path): path to dirname
        """
        try:
            os.mkdir(dirname)
        except FileExistsError:
            # if dirname already exists
            pass
        dir_ = Path(dirname)

        # save image file via. requests to dirname
        for c in self.cards:
            response = requests.get(c.im_url)
            im = Image.open(BytesIO(response.content))
            im.save(dir_.joinpath(f"{c.name}.bmp"))
            time.sleep(0.25)

        return dir_

    def cleanup_images(self, dirname):
        """
        delete dir from store_images function once finished with images

        Args:
            dir_path (str): path to dir
        Returns:
            (int): 0/1 corresponding to success/failure
        """
        try:
            shutil.rmtree(dirname)
            return 0
        except FileNotFoundError:
            return 1
