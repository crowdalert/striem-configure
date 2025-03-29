from pathlib import Path
import shutil
import yaml

from .sources import inputs


def save(savedir: str = "dist") -> None:
    """
    Save the configuration to the specified directory.
    """
    striem_config = {}
    if not Path(savedir, "config", "vector").exists():
        Path(savedir, "config", "vector").mkdir(parents=True, exist_ok=True)
    for input in inputs:
        fname = input.__class__.__module__.split(".")[-1].lower()
        with open(
            Path(
                savedir,
                "config",
                "vector",
                f"{fname}-{input.id}.yaml",
            ),
            "w",
        ) as f:
            f.write(input.dump() + "\n")
        striem_config.update(input.striem_config())

    with open(Path(savedir, "config", "striem.yaml"), "w") as f:
        f.write(yaml.dump(striem_config))

    static = Path(Path(__file__).parent, "static", "vector")
    shutil.copytree(
        static, Path(savedir, "config", "vector", "static"), dirs_exist_ok=True
    )

    dockercompose = Path(Path(__file__).parent, "static", "docker-compose.yaml")
    shutil.copy(dockercompose, Path(savedir, "docker-compose.yaml"))

    Path(savedir, "assets", "detections").mkdir(parents=True, exist_ok=True)
    Path(savedir, "assets", "remaps").mkdir(parents=True, exist_ok=True)
    Path(savedir, "assets", "schema").mkdir(parents=True, exist_ok=True)
    Path(savedir, "data").mkdir(parents=True, exist_ok=True)
