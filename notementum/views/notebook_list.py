from typing import TYPE_CHECKING, Callable, Dict, List

from gi.repository import Gtk

if TYPE_CHECKING:
    from .view_controller import ViewController


class NotebookList:
    def __init__(self,
                 controller: 'ViewController',
                 builder: Gtk.Builder) -> None:
        self.controller = controller

        self.tree_selection_notebooks = builder.get_object(
            'tree_selection_notebooks')
        self.store_notebooks = builder.get_object('store_notebooks')

    def display_notebooks(self, notebooks: List[str]) -> None:
        self.store_notebooks.clear()

        self.store_notebooks.append(['All Notes'])

        for notebook in notebooks:
            self.store_notebooks.append([notebook])

    def select_notebook(self, notebook: str) -> None:
        nb_iter = self.store_notebooks.get_iter_first()
        while nb_iter is not None:
            if self.store_notebooks[nb_iter][0] == notebook:
                self.tree_selection_notebooks.select_iter(nb_iter)
                return
            nb_iter = self.store_notebooks.iter_next(nb_iter)

    def get_signal_handlers(self) -> Dict[str, Callable[..., None]]:
        return {
            'on_tree_selection_notebooks_changed':
                self.on_tree_selection_notebooks_changed,
        }

    def on_tree_selection_notebooks_changed(self,
                                            selection: Gtk.TreeSelection):
        model, treeiter = selection.get_selected()

        if not treeiter:
            return

        self.controller.notebook_selected(model[treeiter][0])
