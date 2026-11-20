import os
import re
from io import TextIOWrapper
from pathlib import Path

import requests

from .constants import (
    API_URL,
    BASE_PARAMS,
    COMMENTSTR,
    ENV_API_KEY,
    ENV_USER_ID,
    HEADERS,
    REQUEST_TIMEOUT,
)


def readlines(path: Path) -> list[str]:
    with path.open("r") as f:
        return f.readlines()


def fetch_count(
    tags: list[str],
    api_key: str,
    user_id: str,
) -> int | None:
    """Número total de posts del tag (viene como atributo del XML)."""
    params = BASE_PARAMS

    params.update({"api_key": api_key, "user_id": user_id})
    params.update({"limit": "1", "tags": "+".join(tags)})
    count = None
    try:
        r = requests.get(
            API_URL,
            params=params,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
        )
        m = re.search(r'count="(\d+)"', r.text)
        if m:
            count = int(m.group(1))
    except requests.RequestException:
        pass
    return count


def sanitisize(line: str) -> tuple[str, str | None]:
    res = line.split(COMMENTSTR, 1)
    return (res[0].strip(), res[1].strip() if len(res) > 1 else None)


def save_content(f: TextIOWrapper, content: list[str]) -> None:
    f.seek(0)
    f.truncate()
    f.writelines([l.strip() + "\n" for l in content])
