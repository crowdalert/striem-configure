from pathlib import Path
import shutil
import yaml

from .sources import inputs

SOURCE_STATIC = Path(Path(__file__).parent, "static")
SOURCE_STATIC_VECTOR = Path(SOURCE_STATIC, "vector")

OUT_CONFIG_DIR = Path("config")
OUT_VECTOR_DIR = Path(OUT_CONFIG_DIR, "vector")
OUT_VECTOR_STATIC_DIR = Path(OUT_VECTOR_DIR, "static")

OUT_ASSETS_DIR = Path("assets")
OUT_DETECTIONS_DIR = Path(OUT_ASSETS_DIR, "detections")
OUT_REMAPS_DIR = Path(OUT_ASSETS_DIR, "remaps")
OUT_SCHEMA_DIR = Path(OUT_ASSETS_DIR, "schema")
OUT_DATA_DIR = Path("data")

DOCKER_COMPOSE = Path("docker-compose.yaml")
STRIEM_CONFIG = Path("striem.yaml")

def save(savedir: str = "dist") -> None:
    """
    Save the configuration to the specified directory.
    """
    striem_config = {}
    if not Path(savedir, OUT_VECTOR_DIR).exists():
        Path(savedir, OUT_VECTOR_DIR).mkdir(parents=True, exist_ok=True)

    shutil.copytree(
        SOURCE_STATIC_VECTOR, Path(savedir, OUT_VECTOR_STATIC_DIR), dirs_exist_ok=True
    )

    for input in inputs:
        fname = input.__class__.__module__.split(".")[-1].lower()
        with open(
            Path(
                savedir,
                OUT_VECTOR_DIR,
                f"{fname}-{input.id}.yaml",
            ),
            "w",
        ) as f:
            f.write(input.dump() + "\n")
        striem_config.update(input.striem_config())

    with open(Path(savedir, OUT_CONFIG_DIR, STRIEM_CONFIG), "w") as f:
        f.write(yaml.dump(striem_config))

    dockercompose = Path(SOURCE_STATIC, DOCKER_COMPOSE)
    shutil.copy(dockercompose, Path(savedir, DOCKER_COMPOSE))

    Path(savedir, OUT_DETECTIONS_DIR).mkdir(parents=True, exist_ok=True)
    Path(savedir, OUT_REMAPS_DIR).mkdir(parents=True, exist_ok=True)
    Path(savedir, OUT_SCHEMA_DIR).mkdir(parents=True, exist_ok=True)
    Path(savedir, OUT_DATA_DIR).mkdir(parents=True, exist_ok=True)
