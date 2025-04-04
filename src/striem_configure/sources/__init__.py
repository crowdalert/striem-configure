import pkgutil
import importlib

from ._source import Source, SourcePicker

_sourcetypes: list[Source] = []

_guard = {}

if not _guard.get(__name__):
    _guard[__name__] = True
    for _, _m, _ in pkgutil.iter_modules(path=__path__):
        mod = importlib.import_module(f"{__name__}.{_m}")
        for _name in dir(mod):
            _attr = getattr(mod, _name)
            if (
                isinstance(_attr, type)
                and issubclass(_attr, Source)
                and _attr is not Source
            ):
                _sourcetypes.append(_attr)

__all__ = [
    "Source",
    "SourcePicker",
]
