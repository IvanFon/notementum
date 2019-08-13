from typing import TYPE_CHECKING, Callable, Dict

from gi.repository import Gtk

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

    def get_signal_handlers(self) -> Dict[str, Callable[..., None]]:
        return {
            'on_btn_new_clicked': (lambda self, *args:
                print('btn_new_clicked')
            ),
            'on_search_notes_search_changed': (lambda self, *args:
                print('search changed')
            ),
            'on_tree_selection_notes_changed': (lambda self, *args:
                print('notes selection changed')
            ),
        }
