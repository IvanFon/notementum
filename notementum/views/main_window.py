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

    def get_signal_handlers(self) -> Dict[str, Callable[..., None]]:
        return {
            'on_win_main_destroy': (lambda self, *args:
                Gtk.main_quit()
            ),
            'on_menu_item_new_activate': (lambda self, *args:
                print('menu item new activated')
            ),
            'on_menu_item_quit_activate': (lambda self, *args:
                Gtk.main_quit()
            ),
        }
