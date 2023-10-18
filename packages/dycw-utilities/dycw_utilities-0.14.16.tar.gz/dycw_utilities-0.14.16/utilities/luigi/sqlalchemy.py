from __future__ import annotations

from typing import Any

from luigi import Parameter
from luigi import Target
from sqlalchemy import Engine
from sqlalchemy import Select
from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError
from sqlalchemy.exc import NoSuchTableError
from typing_extensions import override

from utilities.sqlalchemy import get_table_name
from utilities.sqlalchemy import redirect_to_no_such_table_error


class DatabaseTarget(Target):
    """A target point to a set of rows in a database."""

    def __init__(self, sel: Select[Any], engine: Engine, /) -> None:
        super().__init__()
        self._sel = sel.limit(1)
        self._engine = engine

    def exists(self) -> bool:  # type: ignore
        try:
            with self._engine.begin() as conn:
                res = conn.execute(self._sel).one_or_none()
        except DatabaseError as error:
            try:
                redirect_to_no_such_table_error(self._engine, error)
            except NoSuchTableError:
                return False
        else:
            return res is not None


class EngineParameter(Parameter):
    """Parameter taking the value of a SQLAlchemy engine."""

    @override
    def normalize(self, x: Engine) -> Engine:
        """Normalize an `Engine` argument."""
        return x

    @override
    def parse(self, x: str) -> Engine:
        """Parse an `Engine` argument."""
        return create_engine(x)

    @override
    def serialize(self, x: Engine) -> str:
        """Serialize an `Engine` argument."""
        return x.url.render_as_string()


class TableParameter(Parameter):
    """Parameter taking the value of a SQLAlchemy table."""

    @override
    def normalize(self, x: Any) -> Any:
        """Normalize a `Table` or model argument."""
        return x

    @override
    def serialize(self, x: Any) -> str:
        """Serialize a `Table` or model argument."""
        return get_table_name(x)
