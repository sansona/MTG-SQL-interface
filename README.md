# MTG-SQL Interface

User friendly & cross-platform GUI for performing SQL queries on decklists. 

Functionality:
1. User uploading of decks in common MTG deck formats as exported by tappedout.net & Cockatrice
2. In GUI deck updates via. INSERT and DELETE statements
3. Deck -> SQLite table conversion
4. Query results as either .csv and/or images

To build:
```
pyinstaller --onefile --noconsole gui.py
```
