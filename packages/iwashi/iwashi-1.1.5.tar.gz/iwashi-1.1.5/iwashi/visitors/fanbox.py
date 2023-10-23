import re
from typing import List, TypedDict

import requests

from ..helper import BASE_HEADERS, HTTP_REGEX
from ..visitor import Context, SiteVisitor


class Fanbox(SiteVisitor):
    NAME = "Fanbox"
    URL_REGEX: re.Pattern = re.compile(
        HTTP_REGEX + r"(?P<id>\w+)\.fanbox\.cc", re.IGNORECASE
    )

    def normalize(self, url: str) -> str:
        match = self.URL_REGEX.match(url)
        if match is None:
            return url
        return f'https://{match.group("id")}.fanbox.cc'

    def visit(self, url, context: Context, id: str):
        url = f"https://{id}.fanbox.cc"
        session = requests.Session()
        creator_res = session.get(
            f"https://api.fanbox.cc/creator.get?creatorId={id}",
            headers=BASE_HEADERS
            | {
                "accept": "application/json",
                "origin": f"https://{id}.fanbox.cc",
                "referer": f"https://{id}.fanbox.cc/",
            },
        )

        info: Root = creator_res.json()
        context.create_result(
            "Fanbox",
            url=url,
            name=info["body"]["user"]["name"],
            score=1.0,
            description=info["body"]["description"],
            profile_picture=info["body"]["user"]["iconUrl"],
        )

        for link in info["body"]["profileLinks"]:
            context.visit(link)


class User(TypedDict):
    userId: str
    name: str
    iconUrl: str


class ProfileItemsItem0(TypedDict):
    id: str
    type: str
    imageUrl: str
    thumbnailUrl: str


class Body(TypedDict):
    user: User
    creatorId: str
    description: str
    hasAdultContent: bool
    coverImageUrl: str
    profileLinks: List[str]
    profileItems: List[ProfileItemsItem0]
    isFollowed: bool
    isSupported: bool
    isStopped: bool
    isAcceptingRequest: bool
    hasBoothShop: bool


class Root(TypedDict):
    body: Body
