from typing import List, MutableSet, Optional

import requests
from loguru import logger

from .helper import BASE_HEADERS, normalize_url, parse_host
from .visitor import Context, Result, SiteVisitor, Visitor


class Iwashi(Visitor):
    def __init__(self) -> None:
        self.visitors: List[SiteVisitor] = []
        self.visited: MutableSet[str] = set()

    def add_visitor(self, visitor: SiteVisitor) -> None:
        self.visitors.append(visitor)

    def is_visited(self, url: str) -> bool:
        return url in self.visited

    def mark_visited(self, url: str) -> bool:
        url = url.lower()
        if self.is_visited(url):
            return False
        self.visited.add(url)
        return True

    def visit(self, url: str, context: Optional[Context] = None) -> Optional[Result]:
        url = normalize_url(url)
        context = context or Context(url=url, visitor=self)
        if self.is_visited(url):
            return None
        for visitor in self.visitors:
            match = visitor.match(url, context)
            if match is None:
                continue

            try:
                normalized = visitor.normalize(url)
                if self.mark_visited(normalized):
                    match = visitor.match(normalized, context)
                    if match is not None:
                        visitor.visit(normalized, context, **match.groupdict())
                elif context.parent is not None:
                    context.parent.link(normalized)
            except Exception as e:
                logger.warning(f"[Visitor Error] {url} {visitor.__class__.__name__}")
                logger.exception(e)
                continue
            break
        else:
            self.try_redirect(url, context)
            context.create_result(site_name=parse_host(url), url=url, score=1.0)
            self.mark_visited(url)
            logger.warning(f"[No Visitor Found] {url}")

        return context.result

    def try_redirect(self, url: str, context: Context) -> None:
        res = requests.get(url, allow_redirects=True, headers=BASE_HEADERS)
        if res.url == url:
            return
        context.create_result(site_name=parse_host(url), url=url, score=1.0)
        context.visit(res.url)
        logger.info(f"[Redirect] {url} -> {res.url}")


def get_iwashi():
    iwashi = Iwashi()
    from . import visitors

    for attr in dir(visitors):
        value = getattr(visitors, attr)
        if attr.startswith("_"):
            continue
        if isinstance(value, type) and issubclass(value, SiteVisitor):
            iwashi.add_visitor(value())
    return iwashi


def visit(url: str, iwashi: Optional[Iwashi] = None) -> Optional[Result]:
    iwashi = iwashi or get_iwashi()
    return iwashi.visit(url)
