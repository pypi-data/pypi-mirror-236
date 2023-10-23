import random
import re
import string
from typing import Any, Callable

from .visitor import Result

USER_AGENT = "https://github.com/am230/iwashi"
BASE_HEADERS = {"User-Agent": USER_AGENT}
HTTP_REGEX = "(https?://)?(www.)?"


def print_result(
    result: Result, indent_level=0, print: Callable[[str], Any] = print
) -> None:
    indent = indent_level * "    "
    print(f"{indent}{result.site_name}")
    print(f"{indent}│url  : {result.url}")
    print(f"{indent}│name : {result.title}")
    print(f"{indent}│score: {result.score}")
    print(f"{indent}│links : {result.links}")
    if result.description:
        print(f"{indent}│description: " + result.description.replace("\n", "\\n"))
    for child in result.children:
        print_result(child, indent_level + 1, print)


def parse_host(url: str) -> str:
    match = re.search(r"(https?:\/\/)?(www\.)?(?P<host>[\w.]+)/", url)
    if match is None:
        return url
    return match.group("host")


def random_string(length: int) -> str:
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


URL_NORMALIZE_REGEX = r"(?P<protocol>https?)?:?\/?\/?(?P<domain>[^.]+\.[^\/]+)(?P<path>[^?#]+)?(?P<query>.+)?"


def normalize_url(url: str) -> str:
    match = re.match(URL_NORMALIZE_REGEX, url)
    if match is None:
        raise ValueError(f"Invalid URL: {url}")
    return f"{match.group('protocol') or 'https'}://{match.group('domain')}{match.group('path') or ''}{match.group('query') or ''}"
