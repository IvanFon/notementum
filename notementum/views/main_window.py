# main_window.py - main window
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
            'on_win_main_key_press_event': self.on_win_main_key_press_event,
            'on_menu_item_new_activate':
                (lambda *a: self.controller.new_note(None)),
            'on_menu_item_quit_activate': (lambda *a: Gtk.main_quit()),
            'on_menu_item_undo_activate':
                (lambda *a: self.controller.editor_undo()),
            'on_menu_item_redo_activate':
                (lambda *a: self.controller.editor_redo()),
            'on_menu_item_about_activate':
                (lambda *a: self.controller.show_about_dialog()),
        }

    def on_win_main_key_press_event(self,
                                    widget: Gtk.Widget,
                                    event: Gdk.Event,
                                    *args) -> None:
        self.controller.key_pressed(event.keyval, event.state)
