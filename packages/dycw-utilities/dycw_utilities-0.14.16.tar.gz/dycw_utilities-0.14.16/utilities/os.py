from __future__ import annotations

from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import Mapping
from contextlib import contextmanager
from contextlib import suppress
from os import cpu_count
from os import environ
from os import getenv


def _get_cpu_count() -> int:
    """Get the CPU count."""
    count = cpu_count()
    if count is None:  # pragma: no cover
        raise UnableToDetermineCPUCountError
    return count


class UnableToDetermineCPUCountError(ValueError):
    """Raised when unable to determine the CPU count."""


CPU_COUNT = _get_cpu_count()


@contextmanager
def temp_environ(
    env: Mapping[str, str | None] | None = None, **env_kwargs: str | None
) -> Iterator[None]:
    """Context manager with temporary environment variable set."""
    all_env: dict[str, str | None] = (
        {} if env is None else dict(env)
    ) | env_kwargs
    prev = list(zip(all_env, map(getenv, all_env), strict=True))
    _apply_environment(all_env.items())
    try:
        yield
    finally:
        _apply_environment(prev)


def _apply_environment(items: Iterable[tuple[str, str | None]], /) -> None:
    for key, value in items:
        if value is None:
            with suppress(KeyError):
                del environ[key]
        else:
            environ[key] = value
