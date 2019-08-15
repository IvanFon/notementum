from typing import TYPE_CHECKING, Callable, Dict, List

from gi.repository import Gtk

if TYPE_CHECKING:
    from .view_controller import ViewController


class NotebookList:
    def __init__(self,
                 controller: 'ViewController',
                 builder: Gtk.Builder) -> None:
        self.controller = controller

        self.tree_notebooks = builder.get_object('tree_notebooks')
        self.tree_selection_notebooks = builder.get_object('tree_selection_notebooks')
        self.store_notebooks = builder.get_object('store_notebooks')

    def display_notebooks(self,
                          notebooks: List[str],
                          select_all: bool = False) -> None:
        self.store_notebooks.clear()
        all_notes = self.store_notebooks.append(['All Notes'])

        for notebook in notebooks:
            self.store_notebooks.append([notebook])

        if select_all:
            self.tree_selection_notebooks.select_iter(all_notes)

    def get_signal_handlers(self) -> Dict[str, Callable[..., None]]:
        return {
            'on_tree_selection_notebooks_changed':
                self.on_tree_selection_notebooks_changed,
        }

    def on_tree_selection_notebooks_changed(
            self,
            selection: Gtk.TreeSelection) -> None:
        model, treeiter = selection.get_selected()

        if not treeiter:
            return

        self.controller.notebook_selected(model[treeiter][0])
