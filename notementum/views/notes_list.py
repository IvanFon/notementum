from typing import TYPE_CHECKING, Callable, Dict, List

from gi.repository import Gtk

from ..model import Note

if TYPE_CHECKING:
    from .view_controller import ViewController


class NotesList:
    def __init__(self,
                 controller: 'ViewController',
                 builder: Gtk.Builder) -> None:
        self.controller = controller

        self.tree_notes = builder.get_object('tree_notes')
        self.tree_selection_notes = builder.get_object('tree_selection_notes')
        self.store_notes = builder.get_object('store_notes')
        self.search_notes = builder.get_object('search_notes')

        self.search_notes.grab_focus()

    def display_notes(self, notes: List[Note]) -> None:
        self.store_notes.clear()

        for note in notes:
            self.store_notes.append([note.id, note.name])

    def get_signal_handlers(self) -> Dict[str, Callable[..., None]]:
        return {
            'on_tree_selection_notes_changed':
                self.on_tree_selection_notes_changed,
            'on_search_notes_search_changed':
                self.on_search_notes_search_changed,
            'on_btn_new_clicked': self.on_btn_new_clicked,
            'on_cell_note_name_edited': self.on_cell_note_name_edited,
        }

    def on_tree_selection_notes_changed(
            self,
            selection: Gtk.TreeSelection) -> None:
        model, treeiter = selection.get_selected()

        if not treeiter:
            return

        self.controller.note_selected(model[treeiter][0])

    def on_search_notes_search_changed(self, *args) -> None:
        print('search changed')

    def on_btn_new_clicked(self, *args) -> None:
        print('btn new clicked')

    def on_cell_note_name_edited(self,
                                 renderer: Gtk.CellRendererText,
                                 path: str,
                                 new_text: str) -> None:
        self.controller.rename_note(self.store_notes[path][0], new_text)
