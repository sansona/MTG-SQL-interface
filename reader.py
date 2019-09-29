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
    reads in .xml/.cod file to Deck object

    Assumes Cockatrice export formatting

    Args:
        fname (str): filename containing deck information. Unlike
            other functions, cannot be Path object as minidom has
            difficulty reading in

    Returns:
        (Deck)
    """
    p = Path(fname)

    xmldoc = minidom.parse(fname)
    card_xml = xmldoc.getElementsByTagName("card")

    # build Deck object
    card_list = []
    errors = []
    for c in card_xml:
        card_name = c.attributes["name"].value
        card_count = int(c.attributes["number"].value)
        try:
            cclass = fetch_card_data(card_name, card_count)
            card_list.append(cclass)
        except KeyError:
            # if any cards don't exist, save in errors
            errors.append(card_name)

    return Deck(p.stem, card_list)


def pad_txt_file(fname):
    """
    preprocesses .txt files. Other text formats are outputted in consistent
    format via. tappedout exporting function, but .txt ir prone to padding
    issues. If run into problems reading into df from padding issues, pad
    third char

    Args:
        fname (Path): filename containing deck information
    Returns:
        (DataFrame): Nx2 dataframe w/ cols=["Qty", "Name"]
    """
    while True:
        try:
            # try reading into df of Nx2
            df = pd.read_fwf(fname, header=None)
            df.columns = ("Qty", "Name")
        except ValueError:
            # if padding issue, raise ValueError and pad 3rd char in each line
            new_lines = []
            # open fname, pad third char with space to ensure fwf
            with open(fname, "r") as source:
                lines = source.read().splitlines()
                lines = [l for l in lines if l != ""]
                for l in lines:
                    if l[1] == " ":
                        lsplit = l.split(" ")
                        lsplit[0] = lsplit[0] + " "
                        new_lines.append(" ".join(lsplit))
                    else:
                        new_lines.append(l)
            # overwrite previous fname with proper formatting
            with open(fname, "w") as fp:
                for line in new_lines:
                    print(line, file=fp)
            # open new formatted file as df again
            continue
        break
    return df


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

    # read fname into df, handle formatting. txt requires preprocessing
    if (p.suffix == ".txt") or (p.suffix == ".dek"):
        df = pad_txt_file(p)
    # read csv/tsv into df, no preprocessing required
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
    errors = []  # currently not doing anything with this, may use in future
    for c, q in zip(card_names, qty):
        try:
            card_list.append(fetch_card_data(c, q))
        except KeyError:
            # if any cards don't exist, save in errors
            errors.append(c)
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
