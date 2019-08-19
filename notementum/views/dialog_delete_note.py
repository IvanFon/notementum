from typing import TYPE_CHECKING

from gi.repository import Gtk

if TYPE_CHECKING:
    from .view_controller import ViewController


class DeleteNoteDialog:
    def __init__(self,
                 controller: 'ViewController',
                 builder: Gtk.Builder) -> None:
        self.controller = controller

        self.dialog_delete_note = builder.get_object('dialog_delete_note')

    def show(self, note_name: str) -> Gtk.ResponseType:
        labels = self.dialog_delete_note.get_message_area().get_children()
        labels[1].set_label(
            'Permanently delete note {}?'.format(note_name))

        res = self.dialog_delete_note.run()
        self.dialog_delete_note.hide()

        return res
