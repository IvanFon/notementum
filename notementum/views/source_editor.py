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
        self.webview_preview = builder.get_object('webview_preview')
        self.stack_editor = builder.get_object('stack_editor')
        self.stack_save_status = builder.get_object('stack_save_status')
        self.tool_edit = builder.get_object('tool_edit')
        self.tool_notebook = builder.get_object('tool_notebook')
        self.tool_delete = builder.get_object('tool_delete')

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

        if content is None:
            content = ''

        if self.save_timer is not None:
            GLib.Source.remove(self.save_timer)

        self.set_loading_status(True)
        self.source_buffer.set_text(content)
        self.set_editor_enabled(True)
        self.set_loading_status(False)
        self.tool_edit.set_active(True)

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

    def set_editor_enabled(self, enabled: bool, clear: bool = False) -> None:
        self.source_edit.set_editable(enabled)
        self.source_edit.set_cursor_visible(enabled)
        self.tool_edit.set_sensitive(enabled)
        self.tool_notebook.set_sensitive(enabled)
        self.tool_delete.set_sensitive(enabled)

        if clear:
            self.source_buffer.set_text('')

    def show_editor(self) -> None:
        self.tool_edit.set_active(True)
        self.stack_editor.set_visible_child(
            self.stack_editor.get_children()[0])

    def show_preview(self, preview_content: str) -> None:
        self.tool_edit.set_active(False)
        self.stack_editor.set_visible_child(
            self.stack_editor.get_children()[1])
        self.webview_preview.load_html(preview_content)

    def focus(self) -> None:
        self.source_edit.grab_focus()

        # Place cursor at start
        self.source_buffer.place_cursor(
            self.source_buffer.get_start_iter())

    def insert(self, data: str) -> None:
        self.source_buffer.insert_at_cursor(data, len(data))

    def get_signal_handlers(self) -> Dict[str, Callable[..., None]]:
        return {
            'on_source_edit_destroy': (lambda *a: self.save_note(False)),
            'on_tool_edit_toggled': self.on_tool_edit_toggled,
            'on_tool_notebook_clicked': (
                lambda *a: self.controller.show_assign_notebook_dialog()
            ),
            'on_tool_attach_clicked': (
                lambda *a: self.controller.show_attachment_dialog()
            ),
            'on_tool_delete_clicked': (
                lambda *a: self.controller.delete_selected_note()
            ),
        }

    def on_tool_edit_toggled(self, *args) -> None:
        self.controller.toggle_editor(self.tool_edit.get_active())

    def on_source_buffer_changed(self, *args) -> None:
        if self.loading_note:
            return

        self.set_loading_status(True)

        if self.save_timer is not None:
            GLib.Source.remove(self.save_timer)

        self.save_timer = GLib.timeout_add_seconds(3, self.save_note)
