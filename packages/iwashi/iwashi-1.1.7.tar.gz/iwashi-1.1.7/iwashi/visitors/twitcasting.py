import json
import re
from typing import List, TypedDict

import bs4
import requests
from loguru import logger

from ..helper import BASE_HEADERS, HTTP_REGEX, normalize_url
from ..visitor import Context, SiteVisitor


class TwitCasting(SiteVisitor):
    NAME = "TwitCasting"
    URL_REGEX: re.Pattern = re.compile(
        HTTP_REGEX + r"twitcasting\.tv/(?P<id>[-\w]+)", re.IGNORECASE
    )

    def normalize(self, url: str) -> str:
        match = self.URL_REGEX.match(url)
        if match is None:
            return url
        return f'https://twitcasting.tv/{match.group("id")}'

    def visit(self, url, context: Context, id: str):
        url = f"https://twitcasting.tv/{id}"
        res = requests.get(url, headers=BASE_HEADERS)
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        # name: .tw-user-nav-name
        element = soup.select_one(".tw-user-nav-name")
        if element is None:
            logger.warning(f"[TwitCasting] Could not find name for {url}")
            return
        name = element.text.strip()
        # icon: .tw-user-nav-icon > img
        element = soup.select_one(".tw-user-nav-icon > img")
        profile_picture = None
        if element is not None:
            attr = element["src"]
            if isinstance(attr, str):
                profile_picture = normalize_url(attr)

        context.create_result(
            "TwitCasting",
            url=url,
            name=name,
            score=1.0,
            description=None,
            profile_picture=profile_picture,
        )

        links = set()
        for element in soup.select(".tw-follow-list-row-icon"):
            links.add(element["href"])
        for link in links:
            if link.startswith("/"):
                continue
            context.visit(link)
