from __future__ import annotations

import mimetypes
import re
import webbrowser
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from .config import (
    DEFAULT_START_LANGUAGE,
    MIRROR_STATIC_PREFIX,
    PACKAGE_STATIC_DIR,
    DocBundle,
    default_bundles,
)
from .downloader import ensure_all_docs
from .rewriter import LinkRewriter
from .urls import local_path_to_page_url


class DocsHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(
        self,
        *args,
        bundles: dict[str, DocBundle] | None = None,
        rewriters: dict[str, LinkRewriter] | None = None,
        mirror_static_dir: Path = PACKAGE_STATIC_DIR,
        **kwargs,
    ):
        self.bundles = bundles or {}
        self.rewriters = rewriters or {}
        self.mirror_static_dir = mirror_static_dir
        self.current_bundle = next(iter(self.bundles.values()))
        self.rewriter = self.rewriters.get(self.current_bundle.language)
        super().__init__(*args, directory=str(self.current_bundle.docs_dir), **kwargs)

    def _normalize_request_path(self, request_path: str) -> str:
        parts = [part for part in request_path.split("/") if part]
        return f"/{'/'.join(parts)}" if parts else "/"

    def translate_path(self, path: str) -> str:
        request_path = self._normalize_request_path(unquote(urlparse(path).path))

        if request_path.startswith(MIRROR_STATIC_PREFIX):
            relative = request_path[len(MIRROR_STATIC_PREFIX) :]
            return str(self.mirror_static_dir / relative)

        bundle = self._bundle_for_path(request_path)
        self.current_bundle = bundle
        self.rewriter = self.rewriters[bundle.language]

        relative = self._relative_doc_path(request_path, bundle)
        return str(bundle.docs_dir / relative)

    def _bundle_for_path(self, request_path: str) -> DocBundle:
        japanese = self.bundles.get("ja")
        if japanese and (
            request_path == f"/{japanese.mount_prefix}"
            or request_path.startswith(f"/{japanese.mount_prefix}/")
        ):
            return japanese
        return self.bundles["en"]

    def _relative_doc_path(self, request_path: str, bundle: DocBundle) -> str:
        if bundle.mount_prefix:
            prefix = f"/{bundle.mount_prefix}"
            if request_path == prefix:
                return "index.html"
            relative = request_path[len(prefix) + 1 :].lstrip("/")
        else:
            relative = request_path.lstrip("/")

        if not relative:
            return "index.html"
        if relative.endswith("/"):
            return f"{relative}index.html"
        return relative

    def do_GET(self) -> None:
        request_path = self._normalize_request_path(unquote(urlparse(self.path).path))
        if request_path.startswith(MIRROR_STATIC_PREFIX):
            super().do_GET()
            return
        if self.rewriter and self._serve_rewritten():
            return
        super().do_GET()

    def _serve_rewritten(self) -> bool:
        request_path = unquote(urlparse(self.path).path)
        fs_path = Path(self.translate_path(request_path))
        if not fs_path.is_file():
            return False

        suffix = fs_path.suffix.lower()
        if suffix == ".html":
            self._send_rewritten_html(fs_path)
            return True
        if suffix == ".css":
            self._send_rewritten_css(fs_path)
            return True
        if fs_path.name == "opensearch.xml":
            self._send_rewritten_opensearch(fs_path)
            return True
        return False

    def _page_url_for(self, fs_path: Path) -> str:
        return local_path_to_page_url(
            fs_path,
            self.current_bundle.base_url,
            self.current_bundle.docs_dir,
        )

    def _send_bytes(self, content: bytes, content_type: str) -> None:
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _send_rewritten_html(self, fs_path: Path) -> None:
        content = fs_path.read_bytes()
        content = self.rewriter.rewrite_html(content, self._page_url_for(fs_path))
        self._send_bytes(content, "text/html; charset=utf-8")

    def _send_rewritten_css(self, fs_path: Path) -> None:
        text = fs_path.read_text(encoding="utf-8", errors="replace")
        text = self.rewriter.rewrite_css(text, self._page_url_for(fs_path))
        self._send_bytes(text.encode("utf-8"), "text/css; charset=utf-8")

    def _send_rewritten_opensearch(self, fs_path: Path) -> None:
        text = fs_path.read_text(encoding="utf-8", errors="replace")
        host = self.headers.get("Host", "127.0.0.1")
        prefix = self.current_bundle.mount_path.rstrip("/")
        local_template = f"http://{host}{prefix}/search.html?q={{searchTerms}}"
        text = re.sub(
            r'template="https://docs\.python\.org/[^"]+"',
            f'template="{local_template}"',
            text,
        )
        self._send_bytes(text.encode("utf-8"), "application/opensearchdescription+xml")

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        print(f"[{self.log_date_time_string()}] {format % args}")


def run_server(
    docs_dir: Path,
    *,
    host: str = "127.0.0.1",
    port: int = 8000,
    open_browser: bool = True,
    bundles: tuple[DocBundle, ...] | None = None,
) -> None:
    if bundles is None:
        bundles = default_bundles()

    ensure_all_docs(bundles=bundles)

    bundle_map = {bundle.language: bundle for bundle in bundles}
    start_bundle = bundle_map.get(DEFAULT_START_LANGUAGE) or bundle_map["en"]
    if not (start_bundle.docs_dir / "index.html").exists():
        raise FileNotFoundError(f"index.html not found in {start_bundle.docs_dir}.")

    rewriters = {
        bundle.language: LinkRewriter(bundle.base_url, bundle.docs_dir)
        for bundle in bundles
    }

    mimetypes.add_type("application/javascript", ".js")
    mimetypes.add_type("font/woff2", ".woff2")
    mimetypes.add_type("font/woff", ".woff")

    handler = lambda *args, **kwargs: DocsHTTPRequestHandler(  # noqa: E731
        *args,
        bundles=bundle_map,
        rewriters=rewriters,
        **kwargs,
    )

    try:
        server = ThreadingHTTPServer((host, port), handler)
    except OSError as exc:
        raise RuntimeError(f"Could not start server on {host}:{port}: {exc}") from exc

    if start_bundle.mount_prefix:
        default_page = f"{start_bundle.mount_prefix}/index.html"
    else:
        default_page = "index.html"

    url = f"http://{host}:{port}/{default_page}"
    languages = ", ".join(bundle.label for bundle in bundles)
    print("Serving Python documentation (offline, links rewritten to local files)")
    print(f"Languages: {languages}")
    print(f"Local URL: {url}")
    if start_bundle.language == "ja":
        print(f"English URL: http://{host}:{port}/index.html")
    else:
        print(f"Japanese URL: http://{host}:{port}/ja/index.html")
    print("Press Ctrl+C to stop.")

    if open_browser:
        webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        server.server_close()
