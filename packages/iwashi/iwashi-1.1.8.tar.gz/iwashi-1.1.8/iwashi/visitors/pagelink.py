from __future__ import annotations

import re
import urllib.parse

import requests

from ..helper import HTTP_REGEX
from ..visitor import Context, SiteVisitor


class PageLink(SiteVisitor):
    NAME = "Misskey"
    URL_REGEX: re.Pattern = re.compile(
        HTTP_REGEX + r"(?P<host>\w+)\.page\.link/\?link=(?P<link>[^&]+)", re.IGNORECASE
    )

    def normalize(self, url: str) -> str:
        match = self.URL_REGEX.match(url)
        if match is None:
            return url
        return f'https://{match.group("host")}.page.link/?link={match.group("link")}'

    def visit(self, url, context: Context, host: str, link: str):
        context.create_result(
            "PageLink",
            url=url,
            score=1.0,
        )
        context.visit(urllib.parse.unquote(link))
