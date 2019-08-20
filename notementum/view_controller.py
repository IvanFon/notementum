from itertools import chain
from typing import List

import gi
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gdk, Gtk, GtkSource, GObject, WebKit2
from pkg_resources import resource_filename

from .model import Model
from .views.dialog_assign_notebook import AssignNotebookDialog
from .views.dialog_delete_note import DeleteNoteDialog
from .views.main_window import MainWindow
from .views.notebook_list import NotebookList
from .views.notes_list import NotesList
from .views.source_editor import SourceEditor

GObject.type_register(GtkSource.View)
GObject.type_register(WebKit2.WebView)


class ViewController:
    def __init__(self) -> None:
        self.model = Model()

        builder = self.get_builder()

        self.main_window = MainWindow(self, builder)
        self.notebook_list = NotebookList(self, builder)
        self.notes_list = NotesList(self, builder)
        self.source_editor = SourceEditor(self, builder)
        self.assign_notebook_dialog = AssignNotebookDialog(self, builder)
        self.dialog_delete_note = DeleteNoteDialog(self, builder)

        # Connect signals
        signal_handlers = dict(chain.from_iterable(
            map(dict.items, [
                self.main_window.get_signal_handlers(),
                self.notebook_list.get_signal_handlers(),
                self.notes_list.get_signal_handlers(),
                self.source_editor.get_signal_handlers(),
                self.assign_notebook_dialog.get_signal_handlers(),
            ])
        ))
        builder.connect_signals(signal_handlers)

        self.refresh_notebooks()

    def get_builder(self) -> Gtk.Builder:
        builder = Gtk.Builder()
        builder.add_from_file(resource_filename('notementum', 'res/notes.ui'))
        return builder

    def start(self) -> None:
        self.main_window.win_main.show_all()

        Gtk.main()

    def refresh_notebooks(self) -> List[str]:
        # displaying can mistakenly select a different notebook, save it
        selected_notebook = self.model.selected_notebook

        notebooks = self.model.get_notebooks()
        self.notebook_list.display_notebooks(notebooks)

        self.model.selected_notebook = selected_notebook

        self.notebook_list.select_notebook(self.model.selected_notebook)
        return notebooks

    def notebook_selected(self, notebook: str) -> None:
        self.model.set_selected_notebook(notebook)

        if notebook == 'All Notes':
            notes = self.model.get_notes()
        else:
            notes = self.model.get_notes(notebook)

        self.notes_list.display_notes(notes)
        self.notes_list.select_note(-1)

    def note_selected(self, note_id: int) -> None:
        self.model.set_selected_note(note_id)
        content = self.model.get_note_content(note_id)
        self.source_editor.edit_note(content)

    def save_current_note_content(self, content: str) -> None:
        self.model.save_note_content(self.model.selected_note, content)

    def rename_note(self, note_id: int, name: str) -> None:
        self.model.rename_note(note_id, name)
        self.notes_list.display_notes(
            self.model.get_notes(self.model.selected_notebook))
        self.note_selected(note_id)
        self.notes_list.select_note(self.model.selected_note)

    def editor_undo(self) -> None:
        self.source_editor.undo()

    def editor_redo(self) -> None:
        self.source_editor.redo()

    def show_assign_notebook_dialog(self) -> None:
        note_id = self.model.selected_note

        res, notebook = self.assign_notebook_dialog.show(
            self.model.get_notebooks())
        if res == Gtk.ResponseType.APPLY:
            self.model.assign_notebook(self.model.selected_note, notebook)
            self.refresh_notebooks()
            self.notebook_list.select_notebook(notebook)
            self.notes_list.select_note(note_id)

    def delete_selected_note(self) -> None:
        res = self.dialog_delete_note.show(
            self.model.get_note_name(self.model.selected_note))

        if not res == Gtk.ResponseType.APPLY:
            return

        self.model.delete_note(self.model.selected_note)
        notebooks = self.refresh_notebooks()
        if self.model.selected_notebook in notebooks:
            self.notebook_list.select_notebook(self.model.selected_notebook)
            self.notes_list.select_note(-1)
        else:
            self.notebook_list.select_notebook('All Notes')
            self.notebook_selected('All Notes')

    def disable_editor(self) -> None:
        self.source_editor.set_editor_enabled(False, True)

    def toggle_editor(self, editing: bool) -> None:
        self.model.editing = editing

        if editing:
            self.source_editor.show_editor()
        else:
            self.source_editor.save_note()
            self.source_editor.show_preview(
                self.model.get_selected_note_preview())

    def key_pressed(self, keyval: int, state: Gdk.ModifierType) -> None:
        if keyval == Gdk.KEY_e and state == Gdk.ModifierType.CONTROL_MASK:
            self.toggle_editor(not self.model.editing)

    def new_note(self, name: str) -> None:
        if name is None:
            name = 'New note'

        new_note_id = self.model.create_note(
            name, self.model.selected_notebook)

        self.notes_list.clear_search()
        self.notes_list.display_notes(
            self.model.get_notes(self.model.selected_notebook))
        self.note_selected(new_note_id)
        self.focus_editor()

    def focus_editor(self) -> None:
        self.source_editor.focus()
