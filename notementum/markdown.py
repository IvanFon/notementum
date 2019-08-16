import mistletoe

from mistletoe.html_renderer import HTMLRenderer
from mistletoe.latex_renderer import LaTeXRenderer
from pygments import highlight
from pygments.styles import get_style_by_name as get_style
from pygments.lexers import get_lexer_by_name as get_lexer, guess_lexer
from pygments.formatters.html import HtmlFormatter
from pkg_resources import resource_filename


# https://github.com/miyuchina/mistletoe/blob/master/contrib/pygments_renderer.py
# revision 8d96244
# https://github.com/miyuchina/mistletoe/blob/master/contrib/mathjax.py
# revision 6991a8c

class NotementumRenderer(HTMLRenderer, LaTeXRenderer):
    # TODO: load from local file

    formatter = HtmlFormatter()
    formatter.noclasses = True

    def __init__(self, *extras, style='vim'):
        super().__init__(*extras)
        self.formatter.style = get_style(style)

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


def gen_preview(content: str) -> str:
    with open(resource_filename('notementum', 'res/preview.html')) as f:
        preview = f.read()
        preview = preview.replace(
            '{{{CONTENT}}}',
            mistletoe.markdown(content, NotementumRenderer))

        return preview
