from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options

from mkdocs_callouts.utils import CalloutParser


class CalloutsPlugin(BasePlugin):
    """
    Reads your markdown docs for the following style of callout block:
       > [!INFO] Title
       > An information callout from Obsidian
       > inspired by the syntax from the Microsoft Docs

    and converts it into a mkdocs supported admonition:
       !!! info "Title"
           An admonition block for MkDocs.
           Allowing you to edit your notes
           with confidence using Obsidian.
    """
    config_scheme = {  # pragma: no cover
        ('aliases', config_options.Type(bool, default=True))
    }

    def on_page_markdown(self, markdown, page, config, files):
        parser = CalloutParser(
            convert_aliases=self.config.get('aliases', True)
        )
        return parser.parse(markdown)
