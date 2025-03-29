from prompt_toolkit.application import Application
from prompt_toolkit.layout import (
    Layout,
)
from .save import save
from .main import root, kb, style

app: Application[None] = Application(
    layout=Layout(root),
    full_screen=True,
    key_bindings=kb,
    style=style,
)


def run():
    final: dict = app.run()

    if final and final.get("save"):
        output = final.get("output")
        save(output)
