from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

DEFAULT_BASE_URL = "https://docs.python.org/3/"
DEFAULT_OUTPUT_DIR = Path("docs")
DEFAULT_ARCHIVES_DIR = Path("archives")
DEFAULT_ZIP_NAME = "python-3.14-docs-html.zip"
DEFAULT_ZIP_URL = "https://docs.python.org/3/archives/python-3.14-docs-html.zip"
DEFAULT_ZIP_ROOT = "python-3.14-docs-html/"

DEFAULT_JA_BASE_URL = "https://docs.python.org/ja/3/"
DEFAULT_JA_OUTPUT_DIR = Path("docs-ja")
DEFAULT_JA_ZIP_NAME = "python-3.14-docs-html-ja.zip"
DEFAULT_JA_ZIP_URL = "https://docs.python.org/ja/3/archives/python-3.14-docs-html.zip"

PACKAGE_STATIC_DIR = Path(__file__).resolve().parent / "static"
MIRROR_STATIC_PREFIX = "/_mirror/"
DEFAULT_START_LANGUAGE = "ja"


@dataclass(frozen=True)
class DocBundle:
    language: str
    label: str
    docs_dir: Path
    base_url: str
    mount_prefix: str
    zip_name: str
    zip_url: str
    zip_root: str = DEFAULT_ZIP_ROOT

    @property
    def mount_path(self) -> str:
        if not self.mount_prefix:
            return "/"
        return f"/{self.mount_prefix}/"


def default_bundles() -> tuple[DocBundle, DocBundle]:
    english = DocBundle(
        language="en",
        label="English",
        docs_dir=DEFAULT_OUTPUT_DIR,
        base_url=DEFAULT_BASE_URL,
        mount_prefix="",
        zip_name=DEFAULT_ZIP_NAME,
        zip_url=DEFAULT_ZIP_URL,
    )
    japanese = DocBundle(
        language="ja",
        label="Japanese | 日本語",
        docs_dir=DEFAULT_JA_OUTPUT_DIR,
        base_url=DEFAULT_JA_BASE_URL,
        mount_prefix="ja",
        zip_name=DEFAULT_JA_ZIP_NAME,
        zip_url=DEFAULT_JA_ZIP_URL,
    )
    return english, japanese
