from prompt_toolkit.application import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import FloatContainer
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import (
    Box,
    Button,
    Dialog,
)


from .inputs import InputSelector

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


main = Dialog(
    title="StrIEM Configuration",
    with_background=True,
    body=Box(
        InputSelector(),
        padding=1,
        padding_left=0,
        padding_right=1,
    ),
    buttons=[
        Button(
            text="Done",
            width=6,
            handler=lambda: get_app().exit(result={"save": True, "output": "dist"}),
        ),
        Button(
            text="Cancel",
            width=8,
            handler=lambda: get_app().exit({"save": False}),
        ),
    ],
)

root = FloatContainer(content=main, floats=[], z_index=0)
