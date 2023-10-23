from __future__ import annotations

import json
import re
from typing import List, TypedDict

import bs4
import requests
from loguru import logger

from ..helper import BASE_HEADERS, HTTP_REGEX, normalize_url
from ..visitor import Context, SiteVisitor


class TikTok(SiteVisitor):
    NAME = "TikTok"
    URL_REGEX: re.Pattern = re.compile(
        HTTP_REGEX + r"tiktok\.com/@(?P<id>[-\w]+)", re.IGNORECASE
    )

    def normalize(self, url: str) -> str:
        match = self.URL_REGEX.match(url)
        if match is None:
            return url
        return f'https://tiktok.com/@{match.group("id")}'

    def visit(self, url, context: Context, id: str):
        url = f"https://tiktok.com/@{id}"
        res = requests.get(url, headers=BASE_HEADERS)
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        # icon: <meta property="og:image"
        element = soup.select_one('meta[property="og:image"]')
        profile_picture = None
        if element is not None:
            attr = element["content"]
            if isinstance(attr, str):
                profile_picture = normalize_url(attr)

        # data: #Person
        element = soup.select_one("script#Person")
        if element is None:
            logger.warning(f"[TikTok] Could not find data for {url}")
            return
        data: Root = json.loads(element.text)

        context.create_result(
            "TikTok",
            url=url,
            name=data["name"],
            score=1.0,
            description=data["description"],
            profile_picture=profile_picture,
        )


Interactiontype = TypedDict("interactionType", {"@type": "str"})
InteractionstatisticItem = TypedDict(
    "interactionStatistic_item",
    {
        "@type": "str",
        "interactionType": "Interactiontype",
        "userInteractionCount": "int",
    },
)
Mainentityofpage = TypedDict("mainEntityOfPage", {"@id": "str", "@type": "str"})
Root = TypedDict(
    "Root",
    {
        "@context": "str",
        "@type": "str",
        "name": "str",
        "description": "str",
        "alternateName": "str",
        "url": "str",
        "knowsLanguage": "str",
        "nationality": "str",
        "interactionStatistic": "List[InteractionstatisticItem]",
        "mainEntityOfPage": "Mainentityofpage",
    },
)
