from dataclasses import dataclass


@dataclass
class GithubRepository:
    owner: str
    name: str
    branch: str | None = None
    tag: str | None = None

    def __str__(self) -> str:
        result = f'{self.owner}/{self.name}'
        if self.tag:
            result += f'@{self.tag}'
        return result
