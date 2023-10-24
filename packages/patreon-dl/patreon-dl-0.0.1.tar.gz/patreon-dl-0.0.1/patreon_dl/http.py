import asyncio
import click
import logging
import re
import shutil

from aiohttp import ClientResponse, ClientResponseError, ClientSession, CookieJar, TraceConfig
from aiohttp.tracing import TraceRequestEndParams, TraceRequestStartParams
from os import path
from patreon_dl.cache import get_session_path
from types import SimpleNamespace
from yt_dlp import YoutubeDL


logger = logging.getLogger(__name__)


def load_cookie_jar() -> CookieJar:
    cookie_jar = CookieJar()

    path = get_session_path()
    if path.exists():
        logger.debug(f"Loading session from {path}")
        cookie_jar.load(path)
    else:
        logger.debug(f"Session not found at {path}, not authenticated")

    return cookie_jar


def save_cookie_jar(cookie_jar: CookieJar):
    path = get_session_path()
    logger.debug("Saving session to {path}")
    cookie_jar.save(path)


def logger_trace_config() -> TraceConfig:
    async def on_request_start(_: ClientSession, context: SimpleNamespace, params: TraceRequestStartParams):
        context.start = asyncio.get_event_loop().time()
        logger.debug(f"--> {params.method} {params.url}")

    async def on_request_end(_: ClientSession, context: SimpleNamespace, params: TraceRequestEndParams):
        elapsed = round(100 * (asyncio.get_event_loop().time() - context.start))
        logger.debug(f"<-- {params.method} {params.url} HTTP {params.response.status} {elapsed}ms")

    trace_config = TraceConfig()
    trace_config.on_request_start.append(on_request_start)
    trace_config.on_request_end.append(on_request_end)
    return trace_config


def make_session():
    return ClientSession(
        cookie_jar=load_cookie_jar(),
        trace_configs=[logger_trace_config()],
        headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"},
    )


async def download_file(
    session: ClientSession,
    url: str,
    target_dir: str,
    *,
    default_filename: str | None = None,
    force: bool = False,
):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            filename = extract_filename(response) or default_filename
            if not filename:
                raise Exception("Cannot determine file name")

            target_path = path.join(target_dir, filename)
            if path.exists(target_path) and not force:
                click.echo(f"<-- {filename} - Already downloaded")
                return

            click.echo(f"<-- {filename} - Downloading")
            tmp_path = f"{target_path}.tmp"
            with open(tmp_path, "wb") as fd:
                async for chunk in response.content.iter_chunked(1024 * 1024):
                    fd.write(chunk)
            shutil.move(tmp_path, target_path)
    except ClientResponseError as ex:
        click.secho(f"Download failed: {ex.status} {ex.message}", fg="red")
    except Exception as ex:
        click.secho(f"Download failed: {ex}", fg="red")


def extract_filename(response: ClientResponse) -> str | None:
    content_disposition = response.headers.get('Content-Disposition')
    if content_disposition:
        match = re.search(r'filename=["\'](.*?)["\']', content_disposition)
        if match:
            return match.group(1)


def ytdlp_download(url: str, target_dir: str):
    click.echo(f"<-- Video: {url}")

    # redirect output to target dir via output template
    default_template = "%(title)s [%(id)s].%(ext)s"
    options = {
        "outtmpl": {
            "default": path.join(target_dir, default_template)
        }
    }

    try:
        with YoutubeDL(options) as ydl:
            ydl.download([url])
    except Exception:
        click.secho("Failed downloading video", fg="red")
