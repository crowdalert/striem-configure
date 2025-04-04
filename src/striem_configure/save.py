from pathlib import Path
import shutil
import yaml

from tempfile import TemporaryDirectory
from prompt_toolkit.validation import Validator

from prompt_toolkit.shortcuts import input_dialog

from .common import style
from .sources import Source

SOURCE_STATIC = Path(Path(__file__).parent, "static")
SOURCE_STATIC_VECTOR = Path(SOURCE_STATIC, "vector")

SOURCE_REMAPS = Path(Path(__file__).parent, "includes", "vrl")

OUT_CONFIG_DIR = Path("config")
OUT_VECTOR_DIR = Path(OUT_CONFIG_DIR, "vector")
OUT_VECTOR_STATIC_DIR = Path(OUT_VECTOR_DIR, "static")

OUT_ASSETS_DIR = Path("assets")
OUT_DETECTIONS_DIR = Path(OUT_ASSETS_DIR, "detections")
OUT_REMAPS_DIR = Path(OUT_ASSETS_DIR, "vrl")
OUT_SCHEMA_DIR = Path(OUT_ASSETS_DIR, "schema")
OUT_DATA_DIR = Path("data")

DOCKER_COMPOSE = Path("docker-compose.yaml")
STRIEM_CONFIG = Path("striem.yaml")

def write_tree(inputs: list[Source]) -> TemporaryDirectory:
    """
    Save the configuration to the specified directory.
    """
    striem_config = {}
    temp = TemporaryDirectory()
    outdir = Path(temp.name)

    if not Path(outdir, OUT_VECTOR_DIR).exists():
        Path(outdir, OUT_VECTOR_DIR).mkdir(parents=True, exist_ok=True)

    shutil.copytree(
        SOURCE_STATIC_VECTOR, Path(outdir, OUT_VECTOR_STATIC_DIR), dirs_exist_ok=True
    )

    for input in inputs:
        fname = input.__class__.__module__.split(".")[-1].lower()
        with open(
            Path(
                outdir,
                OUT_VECTOR_DIR,
                f"{fname}-{input.id}.yaml",
            ),
            "w",
        ) as f:
            f.write(input.dump() + "\n")
        striem_config.update(input.striem_config())

    with open(Path(outdir, OUT_CONFIG_DIR, STRIEM_CONFIG), "w") as f:
        f.write(yaml.dump(striem_config))

    # docker-compose.yaml
    dockercompose = Path(SOURCE_STATIC, DOCKER_COMPOSE)
    shutil.copy(dockercompose, Path(outdir, DOCKER_COMPOSE))

    # VRL transforms
    if Path(SOURCE_REMAPS).exists():
        shutil.copytree(SOURCE_REMAPS, Path(outdir, OUT_REMAPS_DIR), dirs_exist_ok=True)

    # Empty assets directories
    Path(outdir, OUT_DETECTIONS_DIR).mkdir(parents=True, exist_ok=True)
    Path(outdir, OUT_REMAPS_DIR).mkdir(parents=True, exist_ok=True)
    Path(outdir, OUT_SCHEMA_DIR).mkdir(parents=True, exist_ok=True)
    Path(outdir, OUT_DATA_DIR).mkdir(parents=True, exist_ok=True)

    return temp


def save(inputs: list[Source]) -> None:
    """
    Save the configuration to the specified directory.
    """
    configtree = write_tree(inputs)

    confirm: str = input_dialog(
        title="StrIEM Configuration",
        text="Save configuration to",
        ok_text="Save",
        style=style,
        validator=Validator.from_callable(
            lambda x: len(x) > 0 and not Path(x).is_file(),
            error_message="Please enter a directory",
            move_cursor_to_end=True,
        ),
    ).run()

    if not confirm:
        return

    outdir = Path(confirm)

    if not outdir.exists():
        outdir.mkdir(parents=True, exist_ok=True)

    # Copy the assets directory to the output directory
    shutil.copytree(
        configtree.name,
        Path(outdir),
        dirs_exist_ok=True,
    )
