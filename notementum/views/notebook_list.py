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

    def display_notebooks(self, notebooks: List[str]) -> None:
        self.store_notebooks.clear()
        self.store_notebooks.append(['All Notes'])

        for notebook in notebooks:
            self.store_notebooks.append([notebook])

    def get_signal_handlers(self) -> Dict[str, Callable[..., None]]:
        return {
            'on_tree_selection_notebooks_changed': (lambda self, *args:
                print('notebook selection changed')
            ),
        }
