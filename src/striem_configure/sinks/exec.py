from prompt_toolkit.layout import HSplit, AnyContainer
from prompt_toolkit.layout.dimension import Dimension as D

from prompt_toolkit.widgets import Label, TextArea
from prompt_toolkit.formatted_text import HTML

from . import Sink


class Exec(Sink):
    label = "Exec Command"

    def __init__(self, *args, **kwargs):
        self.command = TextArea(
            text="",
            multiline=False,
            wrap_lines=False,
            width=D(preferred=60),
        )
        super().__init__(*args, **kwargs)

    def validate(self):
        return self.command.text

    @property
    def config(self) -> dict:
        return {
            "type": "exec",
            "mode": "once",
            "command": self.command.text.split(" "),
        }

    @property
    def friendly_id(self) -> str:
        return str(self.command.text)

    @property
    def body(self) -> AnyContainer:
        return HSplit(
            [
                Label(text=HTML("<b>Command</b>")),
                self.command,
            ]
        )
