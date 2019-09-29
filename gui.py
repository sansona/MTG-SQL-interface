'''
code for handling GUI
'''
from pathlib import Path
import PySimpleGUI as sg
from reader import *
from database import *
from classes import Card, Deck

layout = [[sg.Text('Load from file: ', size=(40, 1), font=(38,),
                   key='-LOAD_STATUS-')],
          [sg.InputText(''), sg.FileBrowse('Browse')],
          [sg.Button('Load'), sg.Button('Download Images')],
          [sg.Text('Query:'), sg.Text('', size=(40, 1), key='-OUTPUT-')],
          [sg.Input(key='-QUERY-')],
          [sg.Button('Query'), sg.Exit()]]

window = sg.Window('MTG SQL Interface', layout)

while True:
    event, values = window.Read()
    if event in (None, 'Exit'):
        break

    if event == 'Load':
        # load file into Deck object & database
        if values['Browse'] != '':
            p = Path(values['Browse'])
            d, db = file_to_db(p, window)

    if event == 'Download Images':
        d.store_images(p.stem)
        window['-LOAD_STATUS-'].Update(f'''{p.stem} images downloaded''')

    if event == 'Query':
        # query database
        p = Path(values['Browse']).stem + '.db'
        query_db(p, values['QUERY'], output='text')
        # Update the "output" text element to be the value of "input" element
        window['-OUTPUT-'].Update(values['-QUERY-'])

window.Close()
