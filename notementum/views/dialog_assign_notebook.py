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
        self.store_assign_notebooks = builder.get_object(
            'store_assign_notebooks')
        self.tree_selection_assign_notebook = builder.get_object(
            'tree_selection_assign_notebook')

        self.new_notebook_iter = None

    def show(self, notebooks: List[str]) -> Tuple[Gtk.ResponseType, str]:
        self.store_assign_notebooks.clear()

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
