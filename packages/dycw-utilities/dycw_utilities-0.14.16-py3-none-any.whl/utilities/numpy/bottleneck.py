from __future__ import annotations

from typing import cast

from bottleneck import push
from numpy import errstate
from numpy import flip
from numpy import isfinite
from numpy import nan
from numpy import where

from .numpy import NDArrayF  # noqa: TID252
from .numpy import NDArrayI  # noqa: TID252
from .numpy import shift  # noqa: TID252


def ffill(
    array: NDArrayF, /, *, limit: int | None = None, axis: int = -1
) -> NDArrayF:
    """Forward fill the elements in an array."""
    return push(array, n=limit, axis=axis)


def pct_change(
    array: NDArrayF | NDArrayI,
    /,
    *,
    limit: int | None = None,
    n: int = 1,
    axis: int = -1,
) -> NDArrayF:
    """Compute the percentage change in an array."""
    if n == 0:
        msg = f"{n=}"
        raise ZeroPercentageChangeSpanError(msg)
    if n > 0:
        filled = ffill(array.astype(float), limit=limit, axis=axis)
        shifted = shift(filled, n=n, axis=axis)
        with errstate(all="ignore"):
            ratio = (filled / shifted) if n >= 0 else (shifted / filled)
        return where(isfinite(array), ratio - 1.0, nan)
    flipped = cast(NDArrayF | NDArrayI, flip(array, axis=axis))
    result = pct_change(flipped, limit=limit, n=-n, axis=axis)
    return flip(result, axis=axis)


class ZeroPercentageChangeSpanError(Exception):
    """Raised when the percentage change span is zero."""
