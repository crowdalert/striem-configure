from pathlib import Path
from zipfile import ZipFile
from io import BytesIO

import requests
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

def fetch_from_github(repo: str, branch: str = "main", out: str = "") -> Path:
    res = requests.get(f"https://github.com/{repo}/archive/refs/heads/{branch}.zip")
    if res.status_code != 200:
        raise Exception(f"Failed to fetch {repo} from github")
    z = ZipFile(BytesIO(res.content))
    z.extractall(path=out)
    root = Path(z.namelist()[0]).parts[0]
    return Path(out, root)
