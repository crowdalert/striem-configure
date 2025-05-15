from prompt_toolkit.application import Application
from prompt_toolkit.layout import (
    Layout,
)
from prompt_toolkit.layout.containers import FloatContainer

from .common import kb, style
from .save import save
from .selector import SelectDialog
from .sources import Source


app: Application[None] = Application(
    layout=Layout(FloatContainer(content=SelectDialog(), floats=[], z_index=0)),
    full_screen=True,
    key_bindings=kb,
    style=style,
)


def run():
    final: list[Source] | None = app.run()

    if final:
        save(final)
