#!/usr/bin/env python3
"""Download a web page and save it with robust error handling.

Usage:
    python3 scrape_page.py https://example.com -o page.html
"""

from __future__ import annotations

import argparse
import os
import socket
import sys
import tempfile
import time
from pathlib import Path
from typing import BinaryIO
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


TRANSIENT_STATUS_CODES = {408, 429, 500, 502, 503, 504}
DEFAULT_USER_AGENT = "Mozilla/5.0 (compatible; page-fetcher/1.0)"


class DownloadError(Exception):
    """Raised when a page cannot be downloaded safely."""


def positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("doit etre un entier positif") from exc

    if parsed <= 0:
        raise argparse.ArgumentTypeError("doit etre un entier positif")
    return parsed


def validate_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise DownloadError("URL invalide. Utilisez une URL complete en http:// ou https://.")


def build_request(url: str) -> Request:
    return Request(
        url,
        headers={
            "User-Agent": DEFAULT_USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )


def copy_limited(response: BinaryIO, destination: BinaryIO, max_bytes: int) -> int:
    downloaded = 0

    while True:
        chunk = response.read(64 * 1024)
        if not chunk:
            return downloaded

        downloaded += len(chunk)
        if downloaded > max_bytes:
            raise DownloadError(
                f"Telechargement interrompu: la page depasse la limite de {max_bytes} octets."
            )

        destination.write(chunk)


def save_atomic(data_file: BinaryIO, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            "wb",
            delete=False,
            dir=output_path.parent,
            prefix=f".{output_path.name}.",
            suffix=".tmp",
        ) as tmp_file:
            tmp_path = Path(tmp_file.name)
            data_file.seek(0)
            while True:
                chunk = data_file.read(64 * 1024)
                if not chunk:
                    break
                tmp_file.write(chunk)

        os.replace(tmp_path, output_path)
    except OSError as exc:
        raise DownloadError(f"Impossible d'ecrire le fichier '{output_path}': {exc}") from exc
    finally:
        if tmp_path and tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass


def download_page(url: str, output_path: Path, timeout: int, retries: int, max_bytes: int) -> int:
    validate_url(url)
    request = build_request(url)
    last_error: Exception | None = None

    for attempt in range(retries + 1):
        try:
            with urlopen(request, timeout=timeout) as response:
                content_length = response.headers.get("Content-Length")
                if content_length and int(content_length) > max_bytes:
                    raise DownloadError(
                        f"Telechargement refuse: Content-Length depasse {max_bytes} octets."
                    )

                with tempfile.TemporaryFile("w+b") as buffer:
                    bytes_written = copy_limited(response, buffer, max_bytes)
                    save_atomic(buffer, output_path)
                    return bytes_written

        except HTTPError as exc:
            last_error = exc
            if exc.code not in TRANSIENT_STATUS_CODES or attempt == retries:
                raise DownloadError(f"Erreur HTTP {exc.code}: {exc.reason}") from exc
        except (URLError, socket.timeout, TimeoutError, ConnectionError) as exc:
            last_error = exc
            if attempt == retries:
                raise DownloadError(f"Erreur reseau: {exc}") from exc
        except ValueError as exc:
            raise DownloadError("En-tete Content-Length invalide.") from exc

        time.sleep(2**attempt)

    raise DownloadError(f"Echec du telechargement: {last_error}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recupere les donnees d'une page web et les sauvegarde dans un fichier."
    )
    parser.add_argument("url", help="URL complete de la page a recuperer")
    parser.add_argument(
        "-o",
        "--output",
        default="page.html",
        type=Path,
        help="chemin du fichier de sortie (defaut: page.html)",
    )
    parser.add_argument(
        "--timeout",
        default=15,
        type=positive_int,
        help="delai maximum d'attente en secondes (defaut: 15)",
    )
    parser.add_argument(
        "--retries",
        default=2,
        type=positive_int,
        help="nombre de nouvelles tentatives apres une erreur temporaire (defaut: 2)",
    )
    parser.add_argument(
        "--max-bytes",
        default=10_000_000,
        type=positive_int,
        help="taille maximale acceptee en octets (defaut: 10000000)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        bytes_saved = download_page(
            url=args.url,
            output_path=args.output,
            timeout=args.timeout,
            retries=args.retries,
            max_bytes=args.max_bytes,
        )
    except DownloadError as exc:
        print(f"Erreur: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Erreur: operation interrompue par l'utilisateur.", file=sys.stderr)
        return 130

    print(f"Page sauvegardee dans '{args.output}' ({bytes_saved} octets).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
