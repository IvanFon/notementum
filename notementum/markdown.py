from typing import TYPE_CHECKING

from mistletoe.block_token import Document
from mistletoe.html_renderer import HTMLRenderer
from mistletoe.latex_renderer import LaTeXRenderer
from pkg_resources import resource_filename
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name as get_lexer, guess_lexer
from pygments.styles import get_style_by_name as get_style

if TYPE_CHECKING:
    from .model import Model


# https://github.com/miyuchina/mistletoe/blob/master/contrib/pygments_renderer.py
# revision 8d96244
# https://github.com/miyuchina/mistletoe/blob/master/contrib/mathjax.py
# revision 6991a8c

class NotementumRenderer(HTMLRenderer, LaTeXRenderer):
    # TODO: load from local file

    formatter = HtmlFormatter()
    formatter.noclasses = True

    def __init__(self, *extras, style='vim', model: 'Model'):
        super().__init__(*extras)
        self.formatter.style = get_style(style)

        self.model = model

    def render_math(self, token):
        """
        Ensure Math tokens are all enclosed in two dollar signs.
        """
        if token.content.startswith('$$') or token.content.startswith('$'):
            return self.render_raw_text(token)
        return '${}$'.format(self.render_raw_text(token))

    def render_block_code(self, token):
        code = token.children[0].content
        if token.language:
            lexer = get_lexer(token.language)
        else:
            lexer = guess_lexer(code)
        return highlight(code, lexer, self.formatter)

    def render_image(self, token):
        template = '<img src="data:image/png;base64,{}" alt="{}"{} />'

        if token.title:
            title = ' title="{}"'.format(self.escape_html(token.title))
        else:
            title = ''

        data = self.model.get_image(token.src).decode('utf-8')

        return template.format(data, self.render_to_plain(token), title)


def gen_preview(model: 'Model', content: str) -> str:
    with NotementumRenderer(model=model) as renderer:
        render = renderer.render(Document(content))

    with open(resource_filename('notementum', 'res/preview.html')) as f:
        preview = f.read()
        preview = preview.replace(
            '{{{CONTENT}}}',
            render)

        return preview
