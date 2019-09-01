# model.py - app data model
# Copyright (C) 2019  Ivan Fonseca
#
# This file is part of Notementum.
#
# Notementum is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Notementum is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Notementum.  If not, see <https://www.gnu.org/licenses/>.

from pathlib import Path
from typing import List, Tuple
import os
import sqlite3

from .constants import ALL_NOTES_NOTEBOOK
from .markdown import gen_preview


class Note:
    def __init__(self, id_: int, name: str, notebook: str):
        self.id = id_
        self.name = name
        self.notebook = notebook


class Model:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(self.get_db_path())
        self.create_notes_table()
        self.create_attachments_table()

        self.selected_notebook = ALL_NOTES_NOTEBOOK
        self.selected_note = ''
        self.editing = True

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

    def create_attachments_table(self) -> None:
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS attachments (
                        id integer PRIMARY KEY,
                        name text NOT NULL,
                        data text NOT NULL
                     );
                  ''')

    def get_notebooks(self) -> List[str]:
        notebooks = []

        c = self.conn.cursor()
        c.execute('''SELECT DISTINCT notebook
                     FROM notes
                  ''')

        for res in c:
            if res[0] is None:
                continue

            notebooks.append(res[0])

        return notebooks

    def get_notes(self, notebook: str = None) -> List[Note]:
        if notebook == ALL_NOTES_NOTEBOOK:
            notebook = None

        notes = []

        c = self.conn.cursor()
        if notebook:
            c.execute('''SELECT *
                         FROM notes
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
        c.execute('''SELECT content
                     FROM notes
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

    def delete_note(self, note_id: int) -> None:
        c = self.conn.cursor()
        c.execute('''DELETE
                     FROM notes
                     WHERE id=?
                  ''', (note_id,))
        self.conn.commit()

    def get_selected_note_preview(self) -> str:
        return gen_preview(self, self.get_note_content(self.selected_note))

    def get_note_name(self, note_id: int) -> str:
        c = self.conn.cursor()
        c.execute('''SELECT name
                     FROM notes
                     WHERE id=?
                  ''', (note_id,))
        return c.fetchone()[0]

    def create_note(self, name: str, notebook: str) -> int:
        if notebook == ALL_NOTES_NOTEBOOK:
            notebook = None

        c = self.conn.cursor()
        c.execute('''INSERT INTO notes (name, notebook)
                     VALUES (?, ?)
                  ''', (name, notebook,))
        self.conn.commit()

        return c.lastrowid

    def add_image(self, name: str, data: str) -> None:
        c = self.conn.cursor()
        c.execute('''INSERT INTO attachments (name, data)
                     VALUES (?, ?)
                  ''', (name, data,))
        self.conn.commit()

    def get_images(self) -> List[Tuple[int, str]]:
        images = []

        c = self.conn.cursor()
        c.execute('''SELECT id, name
                     FROM attachments
                  ''')
        for res in c:
            images.append((res[0], res[1]))

        return images

    def get_image(self, name: str) -> bytes:
        c = self.conn.cursor()
        c.execute('''SELECT data
                     FROM attachments
                     WHERE name=?
                  ''', (name,))
        row = c.fetchone()
        if row is None:
            return b''

        return row[0]

    def delete_image(self, image_id: int) -> str:
        c = self.conn.cursor()
        c.execute('''DELETE
                     FROM attachments
                     WHERE id=?
                  ''', (image_id,))
        self.conn.commit()
