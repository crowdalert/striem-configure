from pathlib import Path
import shutil
from prompt_toolkit.application import Application, get_app
from prompt_toolkit.formatted_text import HTML, merge_formatted_text
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import (
    AnyContainer,
    Dimension,
    FormattedTextControl,
    HSplit,
    Layout,
    VSplit,
    Window,
    HorizontalAlign,
    FloatContainer,
    Float,
)
from prompt_toolkit.layout.margins import ScrollbarMargin
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import (
    Box,
    Button,
    Dialog,
    Label,
)
import yaml

from sources import inputs, SourcePicker


class InputSelector:
    def __init__(self):
        self.selected_line = 0
        self.container = Window(
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
        )

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
        return self.container


def on_save():
    striem_config = {}
    if not Path("dist", "config", "vector").exists():
        Path("dist", "config", "vector").mkdir(parents=True, exist_ok=True)
    for input in inputs:
        fname = input.__class__.__module__.split(".")[-1].lower()
        with open(
            Path(
                "dist",
                "config",
                "vector",
                f"{fname}-{input.id}.yaml",
            ),
            "w",
        ) as f:
            f.write(input.dump() + "\n")
        striem_config.update(input.striem_config())

    with open(Path("dist", "config", "striem.yaml"), "w") as f:
        f.write(yaml.dump(striem_config))

    static = Path(Path(__file__).parent, "static")
    shutil.copytree(
        static, Path("dist", "config", "vector", "static"), dirs_exist_ok=True
    )

    dockercompose = Path(Path(__file__).parent, "docker-compose.yaml")
    shutil.copy(dockercompose, Path("dist", "docker-compose.yaml"))

    Path("dist", "assets", "detections").mkdir(parents=True, exist_ok=True)
    Path("dist", "assets", "remaps").mkdir(parents=True, exist_ok=True)
    Path("dist", "assets", "schema").mkdir(parents=True, exist_ok=True)
    Path("dist", "data").mkdir(parents=True, exist_ok=True)
    get_app().exit()


style = Style.from_dict(
    {
        "dialog.body select-box": "bg:#cccccc",
        "dialog.body select-box cursor-line": "nounderline bg:ansired fg:ansiwhite",
        "dialog.body select-box last-line": "underline",
        "dialog.body text-area": "bg:#4444ff fg:white",
    }
)

kb = KeyBindings()


@kb.add("f6")
def _exit(event):
    event.app.exit()


def open_dialog(dialog: AnyContainer):
    float = Float(content=dialog)
    root_container.floats.append(float)
    app.layout.focus(float.content)


def close_dialog():
    root_container.floats.pop()
    app.layout.focus(main)


dialog_body = Box(
    HSplit(
        [
            Label("* Inputs", style="fg:ansiblue"),
            VSplit(
                [
                    Label(" \n" * 5, width=2),
                    InputSelector(),
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

main = Dialog(
    title="StrIEM Configuration",
    with_background=True,
    body=Box(
        dialog_body,
        padding=1,
        padding_left=0,
        padding_right=1,
    ),
    buttons=[
        Button(
            text="Done",
            width=6,
            handler=on_save,
        ),
        Button(
            text="Cancel",
            width=8,
            handler=lambda: get_app().exit(),
        ),
    ],
)

root_container = FloatContainer(content=main, floats=[], z_index=0)

app: Application[None] = Application(
    layout=Layout(root_container),
    full_screen=True,
    key_bindings=kb,
    style=style,
)

app.run()
