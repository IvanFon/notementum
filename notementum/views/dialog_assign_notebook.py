# dialog_assign_notebook.py - Assign notebook dialog
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

from typing import TYPE_CHECKING, Callable, Dict, List, Tuple

from gi.repository import Gtk

if TYPE_CHECKING:
    from .view_controller import ViewController


class AssignNotebookDialog:
    def __init__(self,
                 controller: 'ViewController',
                 builder: Gtk.Builder) -> None:
        self.controller = controller

        self.dialog_assign_notebook = builder.get_object(
            'dialog_assign_notebook')
        self.btn_assign_notebook_apply = builder.get_object(
            'btn_assign_notebook_apply')
        self.store_assign_notebooks = builder.get_object(
            'store_assign_notebooks')
        self.tree_selection_assign_notebook = builder.get_object(
            'tree_selection_assign_notebook')

        self.new_notebook_iter = None

    def show(self, notebooks: List[str]) -> Tuple[Gtk.ResponseType, str]:
        self.store_assign_notebooks.clear()

        self.none_notebook_iter = self.store_assign_notebooks.append([
            'None (All Notes)', False])
        self.new_notebook_iter = self.store_assign_notebooks.append([
            '<New notebook>', True])

        for notebook in notebooks:
            self.store_assign_notebooks.append([notebook, False])

        res = self.dialog_assign_notebook.run()
        self.dialog_assign_notebook.hide()

        model, treeiter = self.tree_selection_assign_notebook.get_selected()
        return res, model[treeiter][0]

    def get_signal_handlers(self) -> Dict[str, Callable[..., None]]:
        return {
            'on_tree_cell_assign_notebook_name_edited':
                self.on_tree_cell_assign_notebook_name_edited,
        }

    def on_tree_cell_assign_notebook_name_edited(self,
                                                 renderer: Gtk.CellRenderer,
                                                 path: int,
                                                 new_text: str) -> None:
        if self.new_notebook_iter is None:
            return

        self.store_assign_notebooks.insert_after(self.new_notebook_iter,
                                                 [new_text, False])
        self.tree_selection_assign_notebook.select_path(int(path) + 1)
        self.btn_assign_notebook_apply.grab_focus()
