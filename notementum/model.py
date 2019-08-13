from pathlib import Path
from typing import List
import os
import sqlite3


class Note:
    def __init__(self, name: str, notebook: str, content: str):
        self.name = name
        self.notebook = notebook
        self.content = content


class Model:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(self.get_db_path())
        self.create_notes_table()

    def get_db_path(self) -> Path:
        return Path(os.environ['HOME']).joinpath('.notes.db')

    def create_notes_table(self) -> None:
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS notes (
                        id integer PRIMARY KEY,
                        name text NOT NULL,
                        notebook text,
                        content text
                    );
                ''')

    def get_notebooks(self) -> List[str]:
        notebooks = []

        c = self.conn.cursor()
        c.execute('SELECT DISTINCT notebook FROM notes')

        for res in c:
            if res[0] is None:
                continue

            notebooks.append(res[0])

        return notebooks

    def get_notes(self, notebook: str = None) -> List[Note]:
        notes = []

        c = self.conn.cursor()
        if notebook:
            c.execute('''SELECT * FROM notes
                         WHERE notebook=?
                      ''', (notebook,))
        else:
            c.execute('SELECT * FROM notes')

        for res in c:
            notes.append(Note(
                res[1],
                res[2],
                res[3],
            ))

        return notes
