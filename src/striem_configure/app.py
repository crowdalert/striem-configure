from prompt_toolkit.application import Application
from prompt_toolkit.layout import (
    Layout,
)
from prompt_toolkit.layout.containers import FloatContainer

from .common import kb, style
from .save import save
from .inputs import InputSelectDialog
from .sources import Source


app: Application[None] = Application(
    layout=Layout(FloatContainer(content=InputSelectDialog(), floats=[], z_index=0)),
    full_screen=True,
    key_bindings=kb,
    style=style,
)


def run():
    final: list[Source] | None = app.run()

    if final:
        save(final)
