'''
code for handling GUI
'''
from pathlib import Path
import PySimpleGUI as sg
from reader import *
from database import *
from classes import Card, Deck

layout = [[sg.Text('Load deck: ', size=(40, 1), font=(34,),
                   key='-LOAD_STATUS-')],
          [sg.InputText(''), sg.FileBrowse('Browse')],
          [sg.Button('Load')],
          [sg.Text('Query:'), sg.Text('', size=(40, 1), key='-OUTPUT-')],
          [sg.Input(key='-IN-')],
          [sg.Button('Query'), sg.Exit()]]

window = sg.Window('MTG SQL Interface', layout)

while True:
    event, values = window.Read()
    print(event, values)
    if event in (None, 'Exit'):
        break
    if event == 'Load':
        if values['Browse'] != '':
            p = Path(values['Browse'])
        if p.suffix in ('.txt', '.dek', '.csv', '.tsv'):
            d = parse_text_file(p)
            print(d)
            window['-LOAD_STATUS-'].Update(f'''Loaded {p.stem}''')
        if p.suffix in ('.xml', '.cod'):
            # window['-LOAD_STATUS-'].Update(f'''Loading {p.stem}...''')
            # note that arg isn't Path object like other functions
            d = parse_xml_file(values['Browse'])
            print(d)
            window['-LOAD_STATUS-'].Update(f'''Loaded {p.stem}''')

    if event == 'Query':
        # Update the "output" text element to be the value of "input" element
        window['-OUTPUT-'].Update(values['-IN-'])
window.Close()
