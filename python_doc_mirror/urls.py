from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse, urlunparse


CSS_URL_PATTERN = re.compile(
    r"""url\(\s*(['"]?)([^'"\)]+)\1\s*\)""",
    re.IGNORECASE,
)
CSS_IMPORT_PATTERN = re.compile(
    r"""@import\s+(?:url\()?['"]?([^'"\);]+)['"]?\)?""",
    re.IGNORECASE,
)
SEARCHINDEX_PATTERN = re.compile(
    r"Search\.setIndex\((.*)\)\s*;?\s*$",
    re.DOTALL,
)


PLACEHOLDER_TOKENS = frozenset({"PAGEURL", "PAGETITLE", "DOCUMENTATIONROOT"})


def is_placeholder_url(url: str) -> bool:
    parsed = urlparse(url)
    path = unquote(parsed.path or "")
    segments = [segment for segment in path.split("/") if segment]
    if any(segment in PLACEHOLDER_TOKENS for segment in segments):
        return True
    if any(token in parsed.query for token in PLACEHOLDER_TOKENS):
        return True
    return False


VERSIONED_DOCS_PATTERN = re.compile(r"^/3\.\d+(?:/|$)")


def canonicalize_docs_path(path: str, base_url: str) -> str:
    base_path = urlparse(base_url).path.rstrip("/")
    if VERSIONED_DOCS_PATTERN.match(path):
        suffix = path.split("/", 2)[2] if path.count("/") >= 2 else ""
        if suffix:
            return f"{base_path}/{suffix}"
        return base_path
    return path


def page_base_url(page_url: str) -> str:
    parsed = urlparse(page_url)
    path = parsed.path or "/"
    if path.endswith(".html"):
        directory = path.rsplit("/", 1)[0]
        path = f"{directory}/"
    elif not path.endswith("/"):
        path = f"{path}/"
    return urlunparse((parsed.scheme, parsed.netloc, path, "", "", ""))


def normalize_url(url: str, base_url: str) -> str | None:
    url = url.strip()
    if not url or url.startswith("#") or url.lower().startswith(("javascript:", "mailto:", "data:")):
        return None

    absolute = urljoin(base_url, url)
    if is_placeholder_url(absolute):
        return None

    parsed = urlparse(absolute)
    if parsed.scheme not in {"http", "https"}:
        return None

    path = unquote(parsed.path or "/")
    path = canonicalize_docs_path(path, base_url)
    if path != "/" and path.endswith("/"):
        path = f"{path}index.html"

    clean = urlunparse((parsed.scheme, parsed.netloc, path, "", parsed.query, ""))
    return clean


def is_in_scope(url: str, base_url: str) -> bool:
    normalized = normalize_url(url, base_url)
    if not normalized:
        return False
    base = urlparse(base_url)
    target = urlparse(normalized)
    if target.netloc and target.netloc != base.netloc:
        return False
    base_path = base.path.rstrip("/")
    target_path = target.path.rstrip("/") or "/"
    return target_path == base_path or target_path.startswith(f"{base_path}/")


def url_to_local_path(url: str, base_url: str, output_dir: Path) -> Path:
    normalized = normalize_url(url, base_url) or url
    base = urlparse(base_url)
    target = urlparse(normalized)
    base_prefix = base.path.rstrip("/")
    path = target.path

    if path.startswith(base_prefix):
        relative = path[len(base_prefix) :].lstrip("/")
    else:
        relative = path.lstrip("/")

    if not relative:
        relative = "index.html"
    elif relative.endswith("/"):
        relative = f"{relative}index.html"

    return output_dir / relative


def _resolve_existing_local_path(output_dir: Path, relative: str) -> Path | None:
    candidates = [relative]
    if relative.endswith("/"):
        candidates.append(f"{relative}index.html")
    elif not relative.endswith(".html"):
        candidates.append(f"{relative}.html")

    for candidate in candidates:
        path = output_dir / candidate
        if path.is_file():
            return path
    return None


def local_path_for_link(
    url: str,
    page_base: str,
    base_url: str,
    output_dir: Path,
) -> Path | None:
    """Map a link target to a mirrored local file, if one exists."""
    normalized = normalize_url(url, page_base)
    if normalized and is_in_scope(normalized, base_url):
        target = url_to_local_path(normalized, base_url, output_dir)
        if target.is_file():
            return target

    absolute = urljoin(page_base, url.strip())
    parsed = urlparse(absolute)
    docs_host = urlparse(base_url).netloc
    if parsed.netloc not in {"", docs_host}:
        return None

    relative = unquote(parsed.path.lstrip("/"))
    if not relative:
        relative = "index.html"
    return _resolve_existing_local_path(output_dir, relative)


def local_path_to_page_url(local_path: Path, base_url: str, output_dir: Path) -> str:
    relative = local_path.resolve().relative_to(output_dir.resolve()).as_posix()
    return urljoin(base_url, relative)
