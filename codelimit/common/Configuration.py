from pathlib import Path

from yaml import load, FullLoader

from codelimit.common.GithubRepository import GithubRepository


class Configuration:
    exclude: list[str] = []
    verbose = False
    repository: GithubRepository | None = None

    @classmethod
    def load(cls, root: Path):
        config_path = root.joinpath(".codelimit.yml")
        if not config_path.exists():
            return
        with open(config_path) as f:
            d = load(f, Loader=FullLoader)
        if "exclude" in d:
            cls.exclude.extend(d["exclude"])
        if "verbose" in d:
            cls.verbose = d["verbose"]
