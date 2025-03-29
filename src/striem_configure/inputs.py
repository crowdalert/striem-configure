from prompt_toolkit.formatted_text import HTML, merge_formatted_text
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import (
    Dimension,
    FormattedTextControl,
    Window,
)
from prompt_toolkit.layout.margins import ScrollbarMargin

from .sources import inputs

from prompt_toolkit.layout import (
    HSplit,
    VSplit,
    HorizontalAlign,
)
from prompt_toolkit.widgets import (
    Box,
    Button,
    Label,
)

from .sources import SourcePicker
from .util import open_dialog


class InputSelector:
    def __init__(self):
        self.selected_line = 0

    def _get_formatted_text(self):
        result = []
        max = 0
        for entry in inputs:
            if len(str(entry)) > max:
                max = len(str(entry))
        for i, entry in enumerate(inputs):
            if i == self.selected_line:
                result.append([("[SetCursorPosition]", "")])
            result.append(
                HTML(f"<b>{entry.label.ljust(max - 1)}</b>{entry.friendly_id}")
            )
            result.append("\n")

        return merge_formatted_text(result)

    def _get_key_bindings(self):
        kb = KeyBindings()

        @kb.add("up")
        def _go_up(event) -> None:
            self.selected_line = (self.selected_line - 1) % len(inputs)

        @kb.add("down")
        def _go_up(event) -> None:
            self.selected_line = (self.selected_line + 1) % len(inputs)

        @kb.add("enter")
        def _select(event) -> None:
            pass

        return kb

    def __pt_container__(self):
        return Box(
            HSplit(
                [
                    Label("* Inputs", style="fg:ansiblue"),
                    VSplit(
                        [
                            Label(" \n" * 5, width=2),
                            Window(
                                content=FormattedTextControl(
                                    text=self._get_formatted_text,
                                    focusable=True,
                                    key_bindings=self._get_key_bindings(),
                                ),
                                height=Dimension(preferred=5, max=5),
                                cursorline=True,
                                right_margins=[
                                    ScrollbarMargin(display_arrows=True),
                                ],
                                style="class:select-box",
                            ),
                        ],
                    ),
                    VSplit(
                        [
                            Button(
                                text="Add Input",
                                width=11,
                                handler=lambda: open_dialog(SourcePicker()),
                            )
                        ],
                        align=HorizontalAlign.RIGHT,
                    ),
                ],
            ),
            padding=1,
        )
