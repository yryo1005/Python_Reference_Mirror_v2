from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

import requests

from .config import DEFAULT_ARCHIVES_DIR, DocBundle, default_bundles


def download_zip(url: str, destination: Path, *, timeout: int = 120) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading documentation archive from {url} ...")

    with requests.get(url, stream=True, timeout=timeout) as response:
        response.raise_for_status()
        total = int(response.headers.get("Content-Length", 0))
        downloaded = 0
        chunk_size = 1024 * 256

        with destination.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if not chunk:
                    continue
                handle.write(chunk)
                downloaded += len(chunk)
                if total:
                    percent = downloaded * 100 // total
                    print(f"\r  {downloaded // (1024 * 1024)} / {total // (1024 * 1024)} MB ({percent}%)", end="")

    print(f"\nSaved archive to {destination}")


def extract_docs(zip_path: Path, output_dir: Path, *, zip_root: str) -> None:
    print(f"Extracting {zip_path.name} to {output_dir} ...")
    output_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path) as archive:
        members = [name for name in archive.namelist() if name.startswith(zip_root) and not name.endswith("/")]
        for index, member in enumerate(members, start=1):
            relative = member[len(zip_root) :]
            target = output_dir / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(member) as source, target.open("wb") as destination:
                shutil.copyfileobj(source, destination)
            if index % 500 == 0 or index == len(members):
                print(f"\r  Extracted {index} / {len(members)} files", end="")

    print()


def ensure_bundle(
    bundle: DocBundle,
    *,
    archives_dir: Path = DEFAULT_ARCHIVES_DIR,
) -> None:
    index = bundle.docs_dir / "index.html"
    if index.exists():
        return

    zip_path = archives_dir / bundle.zip_name
    if not zip_path.exists():
        download_zip(bundle.zip_url, zip_path)

    extract_docs(zip_path, bundle.docs_dir, zip_root=bundle.zip_root)

    if not index.exists():
        raise RuntimeError(
            f"index.html was not found in {bundle.docs_dir} after extraction. "
            f"The archive layout may have changed."
        )


def ensure_all_docs(
    *,
    archives_dir: Path = DEFAULT_ARCHIVES_DIR,
    bundles: tuple[DocBundle, ...] | None = None,
) -> None:
    if bundles is None:
        bundles = default_bundles()

    for bundle in bundles:
        ensure_bundle(bundle, archives_dir=archives_dir)
