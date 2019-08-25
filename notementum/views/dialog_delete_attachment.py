# dialog_delete_attachment.py - delete attachment dialog
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
