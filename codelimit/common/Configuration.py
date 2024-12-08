from pathlib import Path

from yaml import load, FullLoader


class Configuration:
    excludes: list[str] = []
    verbose = False

    @classmethod
    def load(cls, root: Path):
        config_path = root.joinpath(".codelimit.yml")
        if not config_path.exists():
            return
        with open(config_path) as f:
            d = load(f, Loader=FullLoader)
        if "excludes" in d:
            cls.excludes.extend(d["excludes"])
        if "verbose" in d:
            cls.verbose = d["verbose"]
