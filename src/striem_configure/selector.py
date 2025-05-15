from prompt_toolkit.application import get_app
from prompt_toolkit.formatted_text import HTML, merge_formatted_text
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import (
    HSplit,
    VSplit,
    HorizontalAlign,
    Dimension,
    FormattedTextControl,
    FloatContainer,
    Window,
)
from prompt_toolkit.layout.margins import ScrollbarMargin

from prompt_toolkit.widgets import (
    Box,
    Button,
    Dialog,
    Label,
)
from prompt_toolkit.filters import Condition

from .sources import SourcePicker, Source
from .sinks import SinkPicker, Sink
from .util import open_dialog


class Selector:
    inputs: list[Source | Sink]
    picker: type[SourcePicker | SinkPicker]
    title: str

    def __init__(self, picker: type[SourcePicker | SinkPicker], title: str):
        self.selected_line = 0
        self.inputs = []
        self.picker = picker
        self.title = title

    def _get_formatted_text(self):
        result = []
        max = 0
        for entry in self.inputs:
            if len(str(entry)) > max:
                max = len(str(entry))
        for i, entry in enumerate(self.inputs):
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
            self.selected_line = (self.selected_line - 1) % len(self.inputs)

        @kb.add("down")
        def _go_up(event) -> None:
            self.selected_line = (self.selected_line + 1) % len(self.inputs)

        @kb.add("enter")
        def _select(event) -> None:
            pass

        return kb

    def __pt_container__(self):
        return Box(
            HSplit(
                [
                    Label(f"* {self.title}", style="fg:ansiblue"),
                    VSplit(
                        [
                            Label(" \n" * 5, width=2),
                            Window(
                                content=FormattedTextControl(
                                    text=self._get_formatted_text,
                                    focusable=Condition(lambda: bool(self.inputs)),
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
                                text="Add",
                                width=5,
                                handler=lambda: open_dialog(
                                    self.picker(inputs=self.inputs)
                                ),
                            )
                        ],
                        align=HorizontalAlign.RIGHT,
                    ),
                ],
            ),
            padding=1,
        )


class SelectDialog:
    selectors: list[Selector]

    def __init__(self):
        self.selectors = [
            Selector(SourcePicker, "Inputs"),
            Selector(SinkPicker, "Outputs & Actions"),
        ]

    def __pt_container__(self) -> FloatContainer:
        return Dialog(
            title="StrIEM Configuration",
            with_background=True,
            body=Box(
                HSplit(self.selectors),
                padding=1,
                padding_left=0,
                padding_right=1,
            ),
            buttons=[
                Button(
                    text="Done",
                    width=6,
                    handler=lambda: get_app().exit(
                        result=[i for s in self.selectors for i in s.inputs]
                    ),
                ),
                Button(
                    text="Cancel",
                    width=8,
                    handler=lambda: get_app().exit(),
                ),
            ],
        )
