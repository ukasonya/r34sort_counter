from pathlib import Path
from typing import Annotated

from typer import Argument, Option, Typer

from r34sort_counter.constants import ENV_API_KEY, ENV_USER_ID
from r34sort_counter.utils import (
    fetch_count,
    readlines,
    sanitisize,
    save_content,
)

app = Typer()


@app.command()
def _main(
    path: Annotated[Path, Argument()],
    api_key: Annotated[str, Option(envvar=ENV_API_KEY)],
    user_id: Annotated[str, Option(envvar=ENV_USER_ID)],
    force_commented: Annotated[bool, Option()] = False,
) -> None:
    if not path.is_absolute():
        path = Path().joinpath(path)

    content: list[str] = readlines(path)

    if not (cppath := path.with_name(path.name + "original")).exists():
        path.copy(cppath)

    with open(path, "r+") as f:
        for pos, line in enumerate(content):
            line, comment = sanitisize(line)
            tags = line.split()

            if not force_commented and comment:
                continue

            count = fetch_count(tags, api_key, user_id)

            print(
                f'[*] <{line}> has {count} posts{f" [comment: {comment}]" if comment else ""}'
            )

            content[pos] = f"{line} # {count}{ f" [old: {comment}]" if comment else ""}"

            save_content(f, content)


def main() -> None:
    app()
