import os
import sys

from pathlib import Path


def get_session_path() -> Path:
    return Path(get_cache_dir(), "session.jar")


def get_cache_dir() -> Path:
    path = _get_cache_dir()
    path.mkdir(parents=True, exist_ok=True)
    return path


def _get_cache_dir() -> Path:
    """Returns the path to the cache directory"""

    # Windows
    if sys.platform == "win32" and "APPDATA" in os.environ:
        return Path(os.environ["APPDATA"], "patreon-dl", "cache")

    # Mac OS
    if sys.platform == "darwin":
        return Path(Path.home(), "Library", "Caches", "patreon-dl")

    # Respect XDG_CONFIG_HOME env variable if set
    # https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
    if "XDG_CACHE_HOME" in os.environ:
        return Path(os.environ["XDG_CACHE_HOME"], "patreon-dl")

    return Path(Path.home(), ".cache", "patreon-dl")
