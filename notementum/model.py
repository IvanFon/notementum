from pathlib import Path
from typing import List
import os
import sqlite3


class Note:
    def __init__(self, id_: int, name: str, notebook: str):
        self.id = id_
        self.name = name
        self.notebook = notebook


class Model:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(self.get_db_path())
        self.create_notes_table()

        self.selected_notebook = 'All Notes'
        self.selected_note = ''

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
        if notebook == 'All Notes':
            notebook = None

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
                res[0],
                res[1],
                res[2],
            ))

        return notes

    def set_selected_notebook(self, notebook: str) -> None:
        self.selected_notebook = notebook

    def set_selected_note(self, note_id: int) -> None:
        self.selected_note = note_id

    def get_note_content(self, note_id: int) -> str:
        c = self.conn.cursor()
        c.execute('''SELECT content FROM notes
                     WHERE id=?
                  ''', (note_id,))
        return c.fetchone()[0]

    def save_note_content(self, note_id: int, content: str) -> None:
        c = self.conn.cursor()
        c.execute('''UPDATE notes
                     SET content=?
                     WHERE id=?
                  ''', (content, note_id,))
        self.conn.commit()

    def rename_note(self, note_id: int, name: str) -> None:
        c = self.conn.cursor()
        c.execute('''UPDATE notes
                     SET name=?
                     WHERE id=?
                  ''', (name, note_id,))
        self.conn.commit()

    def assign_notebook(self, note_id: int, notebook: str) -> None:
        c = self.conn.cursor()
        c.execute('''UPDATE notes
                     SET notebook=?
                     WHERE id=?
                  ''', (notebook, note_id,))
        self.conn.commit()
