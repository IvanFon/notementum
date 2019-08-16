from typing import TYPE_CHECKING, Callable, Dict

from gi.repository import GLib, Gtk, GtkSource

if TYPE_CHECKING:
    from .view_controller import ViewController


class SourceEditor:
    def __init__(self,
                 controller: 'ViewController',
                 builder: Gtk.Builder) -> None:
        self.controller = controller

        self.source_edit = builder.get_object('source_edit')
        self.stack_save_status = builder.get_object('stack_save_status')

        self.set_loading_status(False)

        # Setup SourceView
        lang_manager = GtkSource.LanguageManager.get_default()
        self.source_buffer = GtkSource.Buffer.new_with_language(
            lang_manager.get_language('markdown'))
        self.source_edit.set_buffer(self.source_buffer)

        self.source_buffer.connect('changed', self.on_source_buffer_changed)

        self.save_timer = None
        self.loading_note = False

    def set_loading_status(self, loading: bool) -> None:
        if loading:
            self.stack_save_status.set_visible_child(
                self.stack_save_status.get_children()[0])
        else:
            self.stack_save_status.set_visible_child(
                self.stack_save_status.get_children()[1])

    def edit_note(self, content: str) -> None:
        self.loading_note = True

        if self.save_timer is not None:
            GLib.Source.remove(self.save_timer)

        self.set_loading_status(True)
        self.source_buffer.set_text(content)
        self.source_edit.set_editable(True)
        self.source_edit.set_cursor_visible(True)
        self.set_loading_status(False)

        self.loading_note = False

    def save_note(self, set_status: bool = True) -> None:
        self.controller.save_current_note_content(
            self.source_buffer.get_text(
                self.source_buffer.get_start_iter(),
                self.source_buffer.get_end_iter(),
                True
            ))

        if set_status:
            self.set_loading_status(False)

    def undo(self) -> None:
        self.source_buffer.undo()

    def redo(self) -> None:
        self.source_buffer.redo()

    def get_signal_handlers(self) -> Dict[str, Callable[..., None]]:
        return {
            'on_source_edit_destroy': (lambda *a: self.save_note(False)),
            'on_tool_edit_toggled': self.on_tool_edit_toggled,
            'on_tool_notebook_clicked': (
                lambda *a: self.controller.show_assign_notebook_dialog()
            ),
            'on_tool_delete_clicked': self.on_tool_delete_clicked,
        }

    def on_tool_edit_toggled(self, *args) -> None:
        print('edit tool toggled')

    def on_tool_delete_clicked(self, *args) -> None:
        print('delete tool clicked')

    def on_source_buffer_changed(self, *args) -> None:
        if self.loading_note:
            return

        self.set_loading_status(True)

        if self.save_timer is not None:
            GLib.Source.remove(self.save_timer)

        self.save_timer = GLib.timeout_add_seconds(3, self.save_note)
