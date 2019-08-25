from typing import TYPE_CHECKING

from gi.repository import Gtk
from pkg_resources import require


if TYPE_CHECKING:
    from .view_controller import ViewController


__version__ = require('notementum')[0].version


class AboutDialog:
    def __init__(self,
                 controller: 'ViewController',
                 builder: Gtk.Builder) -> None:
        self.controller = controller

        self.dialog_about = builder.get_object('dialog_about')
        self.dialog_about.set_version(__version__)

    def show(self) -> None:
        self.dialog_about.run()
        self.dialog_about.hide()
