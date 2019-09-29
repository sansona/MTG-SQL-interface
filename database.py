'''
functions related to storage and retrieval of data
'''
from pathlib import Path
import sqlite3
import pandas as pd
from reader import *
from classes import Deck


def create_empty_table(deck, path):
    '''
    create empty table corresponding to deck. Will overwrite existing table

    Args:
        deck (Deck): built Deck object to be converted to database
        path (Path|str): path to save database file
    Returns:
        (DB object)
    '''
    p = Path(path)
    db = sqlite3.connect(p)
    query = f'''CREATE TABLE {p.stem}(id INTEGER PRIMARY KEY, name TEXT,
			count INTEGER, mana_cost TEXT, cmc INTEGER, color_identity TEXT,
			card_type TEXT, text TEXT, im_url TEXT)'''
    try:
        # make new table
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
    except sqlite3.OperationalError:
        # if table already exists, drop and make new table
        cursor.execute(f'''DROP TABLE {p.stem}''')
        cursor.execute(query)
        db.commit()

    return db


def deck_to_db(deck, path):
    '''
    update empty table with Deck info

    Args:
        deck (Deck): built Deck object to be converted to database
        path (Path): Path object to database file
    Returns:
        (DB object)
    '''
    p = Path(str(path) + '.db')
    db = create_empty_table(deck, p)

    cursor = db.cursor()
    for c in deck.cards:
        cursor.execute(f'''
			INSERT INTO {p.stem}(name, count, mana_cost,
			cmc, color_identity, card_type, text, im_url)
			VALUES (?,?,?,?,?,?,?,?)''', (str(c.name), int(c.count),
                                 str(c.mana_cost), int(c.cmc),
                                 str(c.color_identity), str(c.card_type),
                                 str(c.text), str(c.im_url)))
        db.commit()

    return db


def query_db(path, query, output='text'):
    '''
    query existing table, save Deck corresponding to new query

    if id included in query, populate Deck object

    Args:
        path (Path|str): path to database file
        query (str): SQL query to be run
        output (str): how to output query results - 'text' or 'images'

    Returns:
        (Deck)
    '''
    p = Path(path)
    db = sqlite3.connect(p)
    query_df = pd.read_sql(query, db)

    # get Deck object corresponding to query if id in query
    cards = []
    cursor = db.cursor()
    if 'id' in query_df.columns:
        all_ids = tuple(query_df['id'])
        cursor.execute(f'''SELECT name FROM {p.stem} WHERE id IN {all_ids}''')
        for row in cursor:
            cards.append(fetch_card_data(row, 1))

        if output == 'text':
            query_df.to_csv(query, sep=' ', index=False)

    return Deck(query, cards)


def db_to_deck(path):
    '''
    converts sqlite table to Deck object if none previously exists

    used when loading new deck from table

    Args:
        path (Path): path to database file
    '''
    p = Path(path)
    db = sqlite3.connect(p)
    query_df = pd.read_sql(f'''SELECT name, count FROM {p.stem}''', db)
    names, counts = list(query_df['name']), list(query_df['count'])

    cards = []
    for name, count in zip(names, counts):
        c = fetch_card_data(name, count)
        cards.append(c)

    return Deck(p.stem, cards)


def file_to_db(path, window):
    '''
    wrapper function for all reading methods

    function reads in any file and handles converting to db
    if appropriate

    Args:
        path (Path|str): Path object to file
        window (Window): Window object from pysimplegui

    Returns:
        (Deck), (DB object)
    '''
    p = Path(path)
    if p.suffix in ('.txt', '.dek', '.csv', '.tsv'):
        deck = read_text_file(p)
        db = deck_to_db(deck, p.stem)
        window['-LOAD_STATUS-'].Update(f'''{p.stem} object ready''')

    if p.suffix in ('.xml', '.cod'):
        # note that arg isn't Path object like other functions
        deck = read_xml_file(values['Browse'])
        db = deck_to_db(deck, p.stem)
        window['-LOAD_STATUS-'].Update(f'''{p.stem} object ready''')

    if p.suffix == '.db':
        # loading from db file, no extension
        deck = db_to_deck(p)
        db = sqlite3.connect(p)
        window['-LOAD_STATUS-'].Update(f'''{p.stem} object ready''')

    return deck, db
