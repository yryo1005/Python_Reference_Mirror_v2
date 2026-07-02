from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

from .config import DEFAULT_BASE_URL, MIRROR_STATIC_PREFIX
from .urls import is_in_scope, local_path_for_link, normalize_url, page_base_url, url_to_local_path

_ONLINE_ONLY_SCRIPTS = frozenset(
    {
        "rtd_switcher.js",
        "https://analytics.python.org/js/script.file-downloads.outbound-links.js",
    }
)

_DOCS_HOST_PATTERN = re.compile(
    r"https?://docs\.python\.org(?:/ja)?(?:/3(?:\.\d+)?)?/",
    re.IGNORECASE,
)

_UNAVAILABLE_LINK_CLASS = "offline-unavailable-link"


class LinkRewriter:
    def __init__(self, base_url: str, output_dir: Path) -> None:
        self.base_url = base_url if base_url.endswith("/") else f"{base_url}/"
        self.output_dir = output_dir.resolve()

    def rewrite_html(self, content: bytes, page_url: str) -> bytes:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(content, "lxml")
        page_path = url_to_local_path(page_url, self.base_url, self.output_dir)
        base = page_base_url(page_url)

        for tag in soup.find_all("a"):
            href = tag.get("href")
            if not href:
                continue
            if href.startswith("#"):
                continue
            rewritten, navigable = self._resolve_anchor(href, base, page_path)
            if rewritten is not None:
                tag["href"] = rewritten
            if not navigable:
                self._mark_unavailable(tag)

        rewrite_tags = [
            ("link", "href"),
            ("script", "src"),
            ("img", "src"),
            ("source", "src"),
            ("iframe", "src"),
            ("meta", "content"),
        ]

        for tag_name, attr in rewrite_tags:
            for tag in soup.find_all(tag_name):
                value = tag.get(attr)
                if not value or value.startswith(("data:", "mailto:", "javascript:", "#")):
                    continue
                rewritten = self._rewrite_docs_link(value, base, page_path)
                if rewritten is not None:
                    tag[attr] = rewritten

        for tag in soup.find_all("form"):
            action = tag.get("action")
            if not action:
                continue
            rewritten = self._rewrite_docs_link(action, base, page_path)
            if rewritten is not None:
                tag["action"] = rewritten

        for tag in soup.find_all("script"):
            src = tag.get("src", "")
            if src in _ONLINE_ONLY_SCRIPTS or src.endswith("rtd_switcher.js"):
                tag.decompose()
                continue
            if tag.string:
                tag.string.replace_with(self.rewrite_text_urls(tag.string, page_url))

        for attr in ("style", "onclick", "onload"):
            for tag in soup.find_all(attrs={attr: True}):
                original = tag.get(attr)
                if isinstance(original, str):
                    tag[attr] = self.rewrite_text_urls(original, page_url)

        self._inject_offline_assets(soup)

        html = str(soup)
        html = self.rewrite_text_urls(html, page_url)
        return html.encode("utf-8")

    def rewrite_css(self, content: str, page_url: str) -> str:
        page_path = url_to_local_path(page_url, self.base_url, self.output_dir)
        page_base = page_base_url(page_url)

        def replace_url(match: re.Match[str]) -> str:
            quote = match.group(1) or ""
            raw = match.group(2)
            target_path = local_path_for_link(raw, page_base, self.base_url, self.output_dir)
            if target_path is None:
                return match.group(0)
            relative = self._relative_path(page_path, target_path)
            return f"url({quote}{relative}{quote})"

        content = re.sub(
            r"""url\(\s*(['"]?)([^'"\)]+)\1\s*\)""",
            replace_url,
            content,
            flags=re.IGNORECASE,
        )
        return self.rewrite_text_urls(content, page_url)

    def rewrite_text_urls(self, content: str, page_url: str) -> str:
        page_path = url_to_local_path(page_url, self.base_url, self.output_dir)
        page_base = page_base_url(page_url)

        def replace_docs_url(match: re.Match[str]) -> str:
            url = match.group(0)
            rewritten = self._rewrite_docs_link(url, page_base, page_path)
            return rewritten if rewritten is not None else url

        return _DOCS_HOST_PATTERN.sub(replace_docs_url, content)

    def _resolve_anchor(self, url: str, page_base: str, page_path: Path) -> tuple[str | None, bool]:
        absolute = urljoin(page_base, url.strip())
        parsed = urlparse(absolute)
        docs_host = urlparse(self.base_url).netloc

        if parsed.scheme in {"http", "https"} and parsed.netloc and parsed.netloc != docs_host:
            if not _DOCS_HOST_PATTERN.search(url):
                return "#", False

        for docs_base in self._candidate_doc_bases():
            target_path = local_path_for_link(url, page_base, docs_base, self.output_dir)
            if target_path is not None and target_path.is_file():
                return self._relative_path(page_path, target_path), True

        rewritten = self._rewrite_docs_link(url, page_base, page_path)
        if rewritten is None:
            if parsed.scheme in {"http", "https"} and parsed.netloc and parsed.netloc != docs_host:
                return "#", False
            return None, False

        expected = (page_path.parent / rewritten).resolve()
        if expected.is_file():
            return rewritten, True
        return "#", False

    def _rewrite_docs_link(self, url: str, page_base: str, page_path: Path) -> str | None:
        if not _DOCS_HOST_PATTERN.search(url):
            normalized = normalize_url(url, page_base)
            if not normalized or not is_in_scope(normalized, self.base_url):
                return None

        for docs_base in self._candidate_doc_bases():
            target_path = local_path_for_link(url, page_base, docs_base, self.output_dir)
            if target_path is not None:
                return self._relative_path(page_path, target_path)

            normalized = normalize_url(url, page_base) or normalize_url(url, docs_base)
            if normalized and is_in_scope(normalized, docs_base):
                expected = url_to_local_path(normalized, docs_base, self.output_dir)
                return self._relative_path(page_path, expected)

        if _DOCS_HOST_PATTERN.search(url):
            fallback = self.output_dir / "_static" / "og-image.png"
            if fallback.is_file() and ("_images/social_previews/" in url or url.endswith("og-image.png")):
                return self._relative_path(page_path, fallback)

        return None

    def _candidate_doc_bases(self) -> tuple[str, ...]:
        bases = [self.base_url]
        if self.base_url != DEFAULT_BASE_URL:
            bases.append(DEFAULT_BASE_URL)
        return tuple(dict.fromkeys(bases))

    def _mark_unavailable(self, tag) -> None:
        tag["href"] = "#"
        tag["aria-disabled"] = "true"
        classes = list(tag.get("class") or [])
        if _UNAVAILABLE_LINK_CLASS not in classes:
            classes.append(_UNAVAILABLE_LINK_CLASS)
        tag["class"] = classes

    def _inject_offline_assets(self, soup) -> None:
        if soup.head is None:
            return

        if not soup.head.find("link", href=f"{MIRROR_STATIC_PREFIX}offline_mirror.css"):
            css = soup.new_tag(
                "link",
                rel="stylesheet",
                href=f"{MIRROR_STATIC_PREFIX}offline_mirror.css",
            )
            soup.head.append(css)

        if not soup.head.find("script", src=f"{MIRROR_STATIC_PREFIX}offline_switchers.js"):
            script = soup.new_tag(
                "script",
                src=f"{MIRROR_STATIC_PREFIX}offline_switchers.js",
            )
            script["defer"] = ""
            soup.head.append(script)

    def _relative_path(self, from_path: Path, to_path: Path) -> str:
        import os

        return os.path.relpath(to_path, from_path.parent).replace("\\", "/")
