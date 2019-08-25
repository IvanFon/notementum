# dialog_about.py - about dialog
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
