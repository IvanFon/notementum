from typing import TYPE_CHECKING, Callable, Dict

from gi.repository import Gtk

if TYPE_CHECKING:
    from .view_controller import ViewController


class MainWindow:
    def __init__(self,
                 controller: 'ViewController',
                 builder: Gtk.Builder) -> None:
        self.controller = controller

        self.win_main = builder.get_object('win_main')
        self.menu_item_undo = builder.get_object('menu_item_undo')
        self.menu_item_redo = builder.get_object('menu_item_redo')

    def update_undo_redo(self, can_undo: bool, can_redo: bool) -> None:
        #  self.menu_item_undo.set_sensitive(can_undo)
        #  self.menu_item_redo.set_sensitive(can_redo)
        pass

    def get_signal_handlers(self) -> Dict[str, Callable[..., None]]:
        return {
            'on_win_main_destroy': self.on_win_main_destroy,
            'on_menu_item_new_activate': self.on_menu_item_new_activate,
            'on_menu_item_quit_activate': self.on_menu_item_quit_activate,
            'on_menu_item_undo_activate': self.on_menu_item_undo_activate,
            'on_menu_item_redo_activate': self.on_menu_item_redo_activate,
        }

    def on_win_main_destroy(self, *args) -> None:
        Gtk.main_quit()

    def on_menu_item_new_activate(self, *args) -> None:
        print('menu file new activated')

    def on_menu_item_quit_activate(self, *args) -> None:
        Gtk.main_quit()

    def on_menu_item_undo_activate(self, *args) -> None:
        self.controller.editor_undo()

    def on_menu_item_redo_activate(self, *args) -> None:
        self.controller.editor_redo()
