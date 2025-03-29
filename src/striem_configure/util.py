from prompt_toolkit.application import get_app
from prompt_toolkit.layout import Float
from prompt_toolkit.layout.containers import AnyContainer, FloatContainer


def open_dialog(dialog: AnyContainer):
    app = get_app()
    root: FloatContainer = app.layout.container
    float = Float(content=dialog)
    root.floats.append(float)
    app.layout.focus(float.content)


def close_dialog():
    app = get_app()
    root: FloatContainer = app.layout.container
    root.floats.pop()
    app.layout.focus(root.content)
