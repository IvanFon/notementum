from itertools import chain

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')
from gi.repository import Gtk, GtkSource, GObject
from pkg_resources import resource_filename

from .model import Model
from .views.main_window import MainWindow
from .views.notebook_list import NotebookList
from .views.notes_list import NotesList
from .views.source_editor import SourceEditor

GObject.type_register(GtkSource.View)


class ViewController:
    def __init__(self) -> None:
        self.model = Model()

        builder = self.get_builder()

        self.main_window = MainWindow(self, builder)
        self.notebook_list = NotebookList(self, builder)
        self.notes_list = NotesList(self, builder)
        self.source_editor = SourceEditor(self, builder)

        # Connect signals
        signal_handlers = dict(chain.from_iterable(
            map(dict.items, [
                self.main_window.get_signal_handlers(),
                self.notebook_list.get_signal_handlers(),
                self.notes_list.get_signal_handlers(),
                self.source_editor.get_signal_handlers(),
            ])
        ))
        builder.connect_signals(signal_handlers)

        self.refresh_notebooks()

    def get_builder(self) -> Gtk.Builder:
        builder = Gtk.Builder()
        builder.add_objects_from_file(
            resource_filename('notementum', 'res/notes.ui'),
            ['win_main', 'store_notebooks', 'store_notes'])
        return builder

    def start(self) -> None:
        self.main_window.win_main.show_all()

        Gtk.main()

    def refresh_notebooks(self) -> None:
        notebooks = self.model.get_notebooks()
        self.notebook_list.display_notebooks(notebooks)
