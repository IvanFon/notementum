from itertools import chain

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')
from gi.repository import Gtk, GtkSource, GObject
from pkg_resources import resource_filename

from .model import Model
from .views.dialog_assign_notebook import AssignNotebookDialog
from .views.main_window import MainWindow
from .views.notebook_list import NotebookList
from .views.notes_list import NotesList
from .views.source_editor import SourceEditor

GObject.type_register(GtkSource.View)


class ViewController:
    def __init__(self) -> None:
        self.model = Model()

        builder = self.get_builder()

        self.main_window = MainWindow(self, builder)
        self.notebook_list = NotebookList(self, builder)
        self.notes_list = NotesList(self, builder)
        self.source_editor = SourceEditor(self, builder)
        self.assign_notebook_dialog = AssignNotebookDialog(self, builder)

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
        builder.add_objects_from_file(
            resource_filename('notementum', 'res/notes.ui'),
            [
                'win_main',
                'store_notebooks',
                'store_notes',
                'dialog_assign_notebook',
                'store_assign_notebooks',
            ])
        return builder

    def start(self) -> None:
        self.main_window.win_main.show_all()

        Gtk.main()

    def refresh_notebooks(self) -> None:
        notebooks = self.model.get_notebooks()

        if self.model.selected_notebook == 'All Notes':
            self.notebook_list.display_notebooks(notebooks, True)
        else:
            self.notebook_list.display_notebooks(notebooks)

    def notebook_selected(self, notebook: str) -> None:
        self.model.set_selected_notebook(notebook)

        if notebook == 'All Notes':
            notes = self.model.get_notes()
        else:
            notes = self.model.get_notes(notebook)

        self.notes_list.display_notes(notes)

    def note_selected(self, note_id: int) -> None:
        self.model.set_selected_note(note_id)
        content = self.model.get_note_content(note_id)
        self.source_editor.display_content(content)

    def save_current_note_content(self, content: str) -> None:
        self.model.save_note_content(self.model.selected_note, content)

    def rename_note(self, note_id: int, name: str) -> None:
        self.model.rename_note(note_id, name)

    def update_undo_redo(self, can_undo: bool, can_redo: bool) -> None:
        self.main_window.update_undo_redo(can_undo, can_redo)

    def editor_undo(self) -> None:
        self.source_editor.undo()

    def editor_redo(self) -> None:
        self.source_editor.redo()

    def show_assign_notebook_dialog(self) -> None:
        res = self.assign_notebook_dialog.show(self.model.get_notebooks())
        if res == Gtk.ResponseType.APPLY:
            # TODO: refresh notes list
            # reselect if notebook changed
            self.refresh_notebooks()

    def assign_notebook(self, notebook: str) -> None:
        self.model.assign_notebook(self.model.selected_note, notebook)