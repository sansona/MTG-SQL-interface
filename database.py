'''
functions related to storage and retrieval of data
'''
import sqlite3
from reader import *


def save_new_deck(deck, path):
    '''
    create new table corresponding to deck

    Args:
        deck (Deck): built Deck object to be converted to database
        path (Path|str): path to save database file
    Returns:
        None
    '''

    db = sqlite3.connect(path)

    cursor = db.cursor()
    cursor.execute(f'''
		CREATE TABLE {deck.name}(id INTEGER PRIMARY KEY, name TEXT,
		count INTEGER, mana_cost TEXT, cmc INTEGER, color_identity TEXT,
		card_type TEXT, text TEXT, im_url TEXT)
		''')
    db.commit()


def update_deck(deck, path):
    '''
    update existing blank table

    Args:
        deck (Deck): built Deck object to be converted to database
        path (Path|str): path to save database file
    Returns:
        None
    '''
    db = sqlite3.connect(path)

    cursor = db.cursor()
    for c in deck.cards:
        print(c)
        cursor.execute(f'''
        	INSERT INTO {deck.name}(name, count, mana_cost,
			cmc, color_identity, card_type, text, im_url)
			VALUES (?,?,?,?,?,?,?,?)''', (str(c.name), int(c.count),
                                 str(c.mana_cost), int(c.cmc),
                                 str(c.color_identity), str(c.card_type),
                                 str(c.text), str(c.im_url)))
        db.commit()


def read_deck(path):
    '''
    read existing table

    Args:
        path (Path|str): path to save database file
    Returns:
        None
    '''
    db = sqlite3.connect(path)

    cursor = db.cursor()
    cursor.execute(f'''SELECT count, color_identity FROM {deck.name}''')
    for row in cursor:
        print(row)
