from typing import TYPE_CHECKING, Callable, Dict

from gi.repository import Gtk, GtkSource

if TYPE_CHECKING:
    from .view_controller import ViewController


class SourceEditor:
    def __init__(self,
                 controller: 'ViewController',
                 builder: Gtk.Builder) -> None:
        self.controller = controller

        self.source_edit = builder.get_object('source_edit')

        # Setup SourceView
        lang_manager = GtkSource.LanguageManager.get_default()
        self.source_buffer = GtkSource.Buffer.new_with_language(lang_manager.get_language('markdown'))
        self.source_edit.set_buffer(self.source_buffer)

    def get_signal_handlers(self) -> Dict[str, Callable[..., None]]:
        return {
            'on_tool_edit_clicked': (lambda self, *args:
                print('tool edit clicked')
            ),
            'on_tool_delete_clicked': (lambda self, *args:
                print('tool delete clicked')
            ),
        }
