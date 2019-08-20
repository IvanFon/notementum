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
        self.tree_filter_notes = builder.get_object('tree_filter_notes')
        self.store_notes = builder.get_object('store_notes')
        self.search_notes = builder.get_object('search_notes')

        self.tree_filter_notes.set_visible_func(self.search_filter)

        self.search_notes.grab_focus()

    def display_notes(self, notes: List[Note]) -> None:
        self.store_notes.clear()

        for note in notes:
            self.store_notes.append([note.id, note.name])

    def select_note(self, note_id: int) -> None:
        if self.store_notes.iter_n_children() == 0:
            self.controller.disable_editor()

        if note_id == -1:
            self.tree_selection_notes.select_path(Gtk.TreePath(0))
            return

        note_iter = self.store_notes.get_iter_first()
        while note_iter is not None:
            if self.store_notes[note_iter][0] == note_id:
                self.tree_selection_notes.select_iter(note_iter)
                return
            note_iter = self.store_notes.iter_next(note_iter)

    def clear_search(self) -> None:
        self.search_notes.set_text('')

    def search_filter(self, model, treeiter, data) -> bool:
        search_text = self.search_notes.get_text()

        if search_text == '':
            return True

        if search_text.lower() in model[treeiter][1].lower():
            return True

        return False

    def get_signal_handlers(self) -> Dict[str, Callable[..., None]]:
        return {
            'on_tree_selection_notes_changed':
                self.on_tree_selection_notes_changed,
            'on_search_notes_search_changed':
                self.on_search_notes_search_changed,
            'on_search_notes_activate': self.on_search_notes_activate,
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
        self.tree_filter_notes.refilter()

        self.select_note(-1)

    def on_search_notes_activate(self, *args) -> None:
        model, treeiter = self.tree_selection_notes.get_selected()

        if treeiter is None:
            self.controller.new_note(self.search_notes.get_text())
        else:
            self.controller.note_selected(model[treeiter][0])

        self.controller.focus_editor()

    def on_btn_new_clicked(self, *args) -> None:
        search = self.search_notes.get_text()
        self.controller.new_note(None if search == '' else search)

    def on_cell_note_name_edited(self,
                                 renderer: Gtk.CellRendererText,
                                 path: str,
                                 new_text: str) -> None:
        self.controller.rename_note(self.store_notes[path][0], new_text)
