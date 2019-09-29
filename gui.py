"""
code for handling GUI
"""
from pathlib import Path
import PySimpleGUI as sg
from reader import *
from database import *
from classes import Card, Deck


def generate_gui():
    """
    function for generating GUI
    """
    layout = [
        [sg.Text("Load from file: ", size=(40, 1),
                 font=(38,), key="-LOAD_STATUS-")],
        [sg.InputText(""), sg.FileBrowse("Browse")],
        [sg.Button("Load")],
        [sg.Text("Query:"), sg.Text("", size=(40, 1), key="-OUTPUT-")],
        [sg.Input(key="-QUERY-")],
        [sg.Button("Output - CSV"), sg.Button("Output - Images"), sg.Exit()],
    ]

    window = sg.Window("MTG SQL Interface", layout)

    while True:
        event, values = window.Read()
        if event in (None, "Exit"):
            break

        if event == "Load":
            # load file into Deck object & database
            if values["Browse"] != "":
                p = Path(values["Browse"])
                _, db = file_to_db(p, window)
                window["-QUERY-"].Update(f"""SELECT * FROM {p.stem} WHERE""")

        if event == "Output - CSV":
            # query database, store output as csv
            p = Path(values["Browse"]).stem + ".db"
            d = query_db(p, values["-QUERY-"], output="text")
            window["-OUTPUT-"].Update("written to CSV")

        if event == "Output - Images":
            # query database, download corresponding images
            p = Path(values["Browse"]).stem + ".db"
            d = query_db(p, values["-QUERY-"], output="images")
            window["-OUTPUT-"].Update("images saved")

    window.Close()


if __name__ == "__main__":
    generate_gui()
