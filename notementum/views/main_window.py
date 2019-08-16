from typing import TYPE_CHECKING, Callable, Dict

from gi.repository import Gdk, Gtk

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

    def get_signal_handlers(self) -> Dict[str, Callable[..., None]]:
        return {
            'on_win_main_destroy': (lambda *a: Gtk.main_quit()),
            'on_menu_item_new_activate': self.on_menu_item_new_activate,
            'on_menu_item_quit_activate': (lambda *a: Gtk.main_quit()),
            'on_menu_item_undo_activate':
                (lambda *a: self.controller.editor_undo()),
            'on_menu_item_redo_activate':
                (lambda *a: self.controller.editor_redo()),
            'on_win_main_key_press_event': self.on_win_main_key_press_event,
        }

    def on_menu_item_new_activate(self, *args) -> None:
        print('menu file new activated')

    def on_win_main_key_press_event(self,
                                    widget: Gtk.Widget,
                                    event: Gdk.Event,
                                    *args) -> None:
        self.controller.key_pressed(event.keyval, event.state)
