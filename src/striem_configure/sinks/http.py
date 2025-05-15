from prompt_toolkit.layout import HSplit, AnyContainer
from prompt_toolkit.layout.dimension import Dimension as D

from prompt_toolkit.widgets import Label, TextArea
from prompt_toolkit.formatted_text import HTML

from . import Sink


class Exec(Sink):
    label = "HTTP POST"

    def __init__(self, *args, **kwargs):
        self.uri = TextArea(
            text="",
            multiline=False,
            wrap_lines=False,
            width=D(preferred=60),
        )
        super().__init__(*args, **kwargs)

    def validate(self):
        return self.uri.text

    @property
    def config(self) -> dict:
        return {
            "type": "http",
            "uri": self.uri.text.split(" "),
        }

    @property
    def friendly_id(self) -> str:
        return str(self.uri.text)

    @property
    def body(self) -> AnyContainer:
        return HSplit(
            [
                Label(text=HTML("<b>URI</b>")),
                self.uri,
            ]
        )
