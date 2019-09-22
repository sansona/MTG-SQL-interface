"""
helper functions for reading deck input into Deck objects
"""
import sys
from xml.dom import minidom
from pathlib import Path
import pandas as pd
import scrython as sc
from classes import Card, Deck


def parse_xml_file(fname):
    """
    reads in .xml file to Deck object

    Args:
        fname (str): filename containing deck information

    Returns:
        (Deck)
    """
    xmldoc = minidom.parse(fname)
    card_xml = xmldoc.getElementsByTagName("card")

    # build Deck object
    card_list = []
    for c in card_xml:
        card_name = c.attributes["name"].value
        card_count = int(c.attributes["number"].value)
        cclass = fetch_card_data(card_name, card_count)
        card_list.append(cclass)

    return Deck(Path(fname).stem, card_list)


def parse_text_file(fname):
    """
    reads in common text file formats (.txt, .csv, .tsv), to Deck

    parsing assumes formatting from tappedout export function

    Args:
        fname (str): filename containing deck information

    Returns:
        (Deck)
    """

    p = Path(fname)

    # read fname into df, handle formatting
    if p.suffix == ".txt":
        df = pd.read_fwf(fname, header=None)
        df.columns = ("Qty", "Name")
    elif p.suffix == ".csv":
        df = pd.read_csv(fname)
    elif p.suffix == ".tsv":
        df = pd.read_csv(fname, sep="\t")
    else:
        sys.exit("Invalid file format")

    df = df.dropna(subset=["Qty", "Name"])

    # get name & qty from df
    card_names = df["Name"].values.tolist()
    qty = df["Qty"].values.tolist()

    # build deck object
    card_list = []
    for c, q in zip(card_names, qty):
        card_list.append(fetch_card_data(c, q))

    return Deck(p.stem, card_list)


def fetch_card_data(card_name, card_count):
    """
    use scryfall API to convert card name to Card object

    Args:
        card_name (str): name of card
        card_count (int): number of card_names included in deck
    Returns:
        (Card): containing relevant attributes fetched from scryfall
    """
    card_obj = sc.cards.Named(fuzzy=card_name)

    mana_cost = card_obj.mana_cost()
    cmc = int(card_obj.cmc())
    color_identity = (card_obj.color_identity(),)
    card_type = (card_obj.type_line(),)
    text = card_obj.oracle_text()
    im_url = card_obj.image_uris()["normal"]

    return Card(
        card_name,
        int(card_count),
        mana_cost,
        cmc,
        color_identity,
        card_type,
        text,
        im_url,
    )
