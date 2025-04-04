import inspect

from pathlib import Path
from string import Template
from uuid import uuid4

from prompt_toolkit.application.current import get_app
from prompt_toolkit.layout import HorizontalAlign, ConditionalContainer
from prompt_toolkit.widgets import RadioList, Dialog, Button
from prompt_toolkit.layout import AnyContainer, Float, FloatContainer
from prompt_toolkit.filters import Condition
from prompt_toolkit.layout.containers import HSplit, VSplit


class Source:
    id: str
    label: str
    friendly_id: str = ""
    _inputs: list["Source"]
    _container: AnyContainer

    def __init__(self, inputs=None, id=None):
        self.id = id if id else str(uuid4())
        self._inputs = inputs
        self._container = Dialog(
            title=self.label,
            body=HSplit(
                [
                    self.body,
                    VSplit(
                        [
                            ConditionalContainer(
                                Button(text="OK", width=4, handler=self.ok),
                                Condition(lambda: self.validate()),
                            ),
                            Button(text="Cancel", width=8, handler=self.close),
                        ],
                        align=HorizontalAlign.RIGHT,
                        padding=1,
                    ),
                ],
            ),
            with_background=True,
        )

    def dump(self) -> str:
        raise NotImplementedError

    def validate(self):
        raise NotImplementedError

    @property
    def body(self) -> AnyContainer:
        raise NotImplementedError

    def striem_config(self) -> dict:
        return {}

    @property
    def template(self) -> Template:
        classfile = Path(inspect.getfile(self.__class__))
        template_file = Path(
            classfile.parent.parent,
            "template",
            classfile.name.replace(classfile.suffix, ".yaml"),
        )
        if template_file.exists():
            with open(template_file) as f:
                return Template(f.read())
        return Template("")

    def ok(self):
        if self.validate():
            self._inputs.append(self)
        self.close()

    def close(self):
        parent: FloatContainer = get_app().layout.container
        parent.floats.pop()
        get_app().layout.focus(parent.content)

    def __pt_container__(self) -> AnyContainer:
        return FloatContainer(content=self._container, floats=[])


class SourcePicker:
    container: FloatContainer
    inputs: list[Source]

    def __init__(self, inputs: list[Source] = None):
        self.inputs = inputs
        from . import _sourcetypes

        sources = [(cls, cls.label) for cls in _sourcetypes]

        self.selection = RadioList(values=sources)

        self.container = FloatContainer(
            content=Dialog(
                title="Add Input",
                body=self.body,
                buttons=[
                    Button(text="OK", handler=self._next),
                    Button(text="Cancel", handler=self.close),
                ],
                with_background=False,
            ),
            floats=[],
        )

    @property
    def body(self) -> AnyContainer:
        return HSplit(
            [self.selection],
            padding=1,
        )

    def _next(self):
        parent: FloatContainer = get_app().layout.container
        floats = parent.floats
        floats.pop()
        child = Float(content=self.selection.current_value(inputs=self.inputs))
        floats.append(child)
        get_app().layout.focus(child.content)

    def close(self):
        parent: FloatContainer = get_app().layout.container
        parent.floats.pop()
        get_app().layout.focus(parent.content)

    def __pt_container__(self) -> AnyContainer:
        return self.container
