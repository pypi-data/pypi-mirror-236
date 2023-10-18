from __future__ import annotations

import datetime as dt
from collections.abc import Callable
from collections.abc import Iterable
from contextlib import suppress
from functools import wraps
from os import environ
from pathlib import Path
from typing import Any

from utilities.atomicwrites import writer
from utilities.datetime import UTC
from utilities.git import get_repo_root
from utilities.pathlib import PathLike
from utilities.re import NoMatchesError
from utilities.re import extract_group
from utilities.typing import IterableStrs

try:  # WARNING: this package cannot use unguarded `pytest` imports
    from _pytest.config import Config
    from _pytest.config.argparsing import Parser
    from _pytest.python import Function
    from pytest import mark
    from pytest import skip
except ModuleNotFoundError:  # pragma: no cover
    from typing import Any as Config
    from typing import Any as Function
    from typing import Any as Parser

    mark = skip = None


def add_pytest_addoption(parser: Parser, options: IterableStrs, /) -> None:
    """Add the `--slow`, etc options to pytest.

    Usage:

        def pytest_addoption(parser):
            add_pytest_addoption(parser, ["slow"])
    """
    for opt in options:
        _ = parser.addoption(
            f"--{opt}",
            action="store_true",
            default=False,
            help=f"run tests marked {opt!r}",
        )


def add_pytest_collection_modifyitems(
    config: Config, items: Iterable[Function], options: IterableStrs, /
) -> None:
    """Add the @mark.skips as necessary.

    Usage:

        def pytest_collection_modifyitems(config, items):
            add_pytest_collection_modifyitems(config, items, ["slow"])
    """
    options = list(options)
    missing = {opt for opt in options if not config.getoption(f"--{opt}")}
    for item in items:
        opts_on_item = [opt for opt in options if opt in item.keywords]
        if len(missing & set(opts_on_item)) >= 1:
            flags = [f"--{opt}" for opt in opts_on_item]
            joined = " ".join(flags)
            if mark is not None:  # pragma: no cover
                _ = item.add_marker(mark.skip(reason=f"pass {joined}"))


def add_pytest_configure(
    config: Config, options: Iterable[tuple[str, str]], /
) -> None:
    """Add the `--slow`, etc markers to pytest.

    Usage:
        def pytest_configure(config):
            add_pytest_configure(config, [("slow", "slow to run")])
    """
    for opt, desc in options:
        _ = config.addinivalue_line("markers", f"{opt}: mark test as {desc}")


def is_pytest() -> bool:
    """Check if pytest is currently running."""
    return "PYTEST_CURRENT_TEST" in environ


def throttle(*, root: PathLike | None = None, duration: float = 1.0) -> Any:
    """Throttle a test."""

    root_use = (
        get_repo_root().joinpath(".pytest_cache")
        if root is None
        else Path(root)
    )

    def wrapper(func: Callable[..., Any], /) -> Callable[..., Any]:
        """Decorator to throttle a test function/method."""

        @wraps(func)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            """The throttled test function/method."""
            test = environ["PYTEST_CURRENT_TEST"]
            with suppress(NoMatchesError):
                test = extract_group(r"^(.+) \(.+\)$", test)
            path = root_use.joinpath(*test.split("::"))
            if path.exists():
                with path.open(mode="r") as fh:
                    contents = fh.read()
                prev = float(contents)
            else:
                prev = None
            now = dt.datetime.now(tz=UTC).timestamp()
            if (
                (skip is not None)
                and (prev is not None)
                and ((now - prev) < duration)
            ):
                skip(reason=f"{test} throttled")
            with writer(path, overwrite=True) as temp, temp.open(
                mode="w"
            ) as fh:
                _ = fh.write(str(now))
            return func(*args, **kwargs)

        return wrapped

    return wrapper
