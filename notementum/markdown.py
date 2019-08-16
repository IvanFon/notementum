import mistletoe

from mistletoe.html_renderer import HTMLRenderer
from mistletoe.latex_renderer import LaTeXRenderer
from pygments import highlight
from pygments.styles import get_style_by_name as get_style
from pygments.lexers import get_lexer_by_name as get_lexer, guess_lexer
from pygments.formatters.html import HtmlFormatter


# https://github.com/miyuchina/mistletoe/blob/master/contrib/pygments_renderer.py
# revision 8d96244
# https://github.com/miyuchina/mistletoe/blob/master/contrib/mathjax.py
# revision 6991a8c

class NotementumRenderer(HTMLRenderer, LaTeXRenderer):
    # TODO: load from local file
    mathjax_src = '<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML"></script>\n'

    formatter = HtmlFormatter()
    formatter.noclasses = True

    def __init__(self, *extras, style='vim'):
        super().__init__(*extras)
        self.formatter.style = get_style(style)

    def render_math(self, token):
        """
        Ensure Math tokens are all enclosed in two dollar signs.
        """
        if token.content.startswith('$$'):
            return self.render_raw_text(token)
        return '${}$'.format(self.render_raw_text(token))

    def render_block_code(self, token):
        code = token.children[0].content
        lexer = get_lexer(token.language) if token.language else guess_lexer(code)
        return highlight(code, lexer, self.formatter)

    def render_document(self, token):
        """
        Append CDN link for MathJax to the end of <body>.
        """
        return super().render_document(token) + self.mathjax_src


def gen_preview(content: str) -> str:
        preview = '''<style>
                       body {
                         background-color: #404552;
                         color: #d3dae3;
                       }
                     </style>'''

        preview += mistletoe.markdown(content, NotementumRenderer)

        return preview
