from typing import TYPE_CHECKING

from gi.repository import Gtk

if TYPE_CHECKING:
    from .view_controller import ViewController


class DeleteAttachmentDialog:
    def __init__(self,
                 controller: 'ViewController',
                 builder: Gtk.Builder) -> None:
        self.controller = controller

        self.dialog_delete_attachment = builder.get_object(
            'dialog_delete_attachment')

    def show(self, attachment_name: str) -> Gtk.ResponseType:
        labels = self.dialog_delete_attachment.get_message_area().get_children()
        labels[1].set_label(
            'Permanently delete attachment {}?'.format(attachment_name))

        res = self.dialog_delete_attachment.run()
        self.dialog_delete_attachment.hide()

        return res
