from typing import TYPE_CHECKING, Callable, Dict, List, Tuple

from gi.repository import Gtk

if TYPE_CHECKING:
    from .view_controller import ViewController


class AttachmentsDialog:
    def __init__(self,
                 controller: 'ViewController',
                 builder: Gtk.Builder) -> None:
        self.controller = controller

        self.dialog_attachments = builder.get_object('dialog_attachments')
        self.store_attachments = builder.get_object('store_attachments')
        self.tree_selection_attachments = builder.get_object(
            'tree_selection_attachments')
        self.dialog_file_attachment = builder.get_object(
            'dialog_file_attachment')
        self.btn_attachments_insert_selected = builder.get_object(
            'btn_attachments_insert_selected')

    def show(self,
             attachments: List[Tuple[int, str]]
             ) -> Tuple[Gtk.ResponseType, str]:
        self.refresh_attachments(attachments)

        res = self.dialog_attachments.run()
        self.dialog_attachments.hide()

        model, treeiter = self.tree_selection_attachments.get_selected()
        if not treeiter:
            return res, ''
        else:
            return res, model[treeiter][1]

    def refresh_attachments(self,
                            attachments: List[Tuple[int, str]]) -> None:
        self.store_attachments.clear()

        for attach in attachments:
            self.store_attachments.append([
                attach[0],
                attach[1],
            ])

        self.btn_attachments_insert_selected.set_sensitive(False)

    def get_signal_handlers(self) -> Dict[str, Callable[..., None]]:
        return {
            'on_tool_attachment_add_clicked': self.add_attachment,
            'on_tool_attachment_delete_clicked': self.delete_attachment,
            'on_tree_selection_attachments_changed':
                self.on_tree_selection_attachments_changed,
        }

    def add_attachment(self, *args) -> None:
        res = self.dialog_file_attachment.run()
        if res == Gtk.ResponseType.APPLY:
            self.controller.add_attachment(
                self.dialog_file_attachment.get_filename())
        self.dialog_file_attachment.hide()

    def delete_attachment(self, *args) -> None:
        model, treeiter = self.tree_selection_attachments.get_selected()
        self.controller.delete_attachment(model[treeiter][0],
                                          model[treeiter][1])

    def on_tree_selection_attachments_changed(self, *args) -> None:
        self.btn_attachments_insert_selected.set_sensitive(True)
