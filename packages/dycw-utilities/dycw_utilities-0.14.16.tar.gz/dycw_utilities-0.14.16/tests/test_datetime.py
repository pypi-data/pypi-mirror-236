from __future__ import annotations

import datetime as dt
from collections.abc import Callable
from operator import eq
from operator import gt
from operator import lt
from re import search
from typing import Any

from hypothesis import HealthCheck
from hypothesis import assume
from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import DataObject
from hypothesis.strategies import SearchStrategy
from hypothesis.strategies import data
from hypothesis.strategies import dates
from hypothesis.strategies import datetimes
from hypothesis.strategies import integers
from hypothesis.strategies import just
from hypothesis.strategies import sampled_from
from hypothesis.strategies import timedeltas
from hypothesis.strategies import times
from pytest import mark
from pytest import param
from pytest import raises

from utilities.datetime import EPOCH_UTC
from utilities.datetime import UTC
from utilities.datetime import CallYieldWeekdaysError
from utilities.datetime import IsWeekendError
from utilities.datetime import ParseDateError
from utilities.datetime import ParseDateTimeError
from utilities.datetime import ParseTimeError
from utilities.datetime import TimedeltaError
from utilities.datetime import add_weekdays
from utilities.datetime import date_to_datetime
from utilities.datetime import ensure_date
from utilities.datetime import ensure_datetime
from utilities.datetime import ensure_time
from utilities.datetime import ensure_timedelta
from utilities.datetime import is_weekday
from utilities.datetime import local_timezone
from utilities.datetime import maybe_sub_pct_y
from utilities.datetime import parse_date
from utilities.datetime import parse_datetime
from utilities.datetime import parse_time
from utilities.datetime import parse_timedelta
from utilities.datetime import round_to_next_weekday
from utilities.datetime import round_to_prev_weekday
from utilities.datetime import serialize_date
from utilities.datetime import serialize_datetime
from utilities.datetime import serialize_time
from utilities.datetime import serialize_timedelta
from utilities.datetime import yield_weekdays
from utilities.hypothesis import assume_does_not_raise
from utilities.hypothesis import text_clean
from utilities.platform import SYSTEM
from utilities.platform import System


class TestAddWeekdays:
    @given(date=dates(), n=integers(-10, 10))
    @mark.parametrize("predicate", [param(gt), param(lt)])
    def test_add(
        self, date: dt.date, n: int, predicate: Callable[[Any, Any], bool]
    ) -> None:
        _ = assume(predicate(n, 0))
        with assume_does_not_raise(OverflowError):
            result = add_weekdays(date, n=n)
        assert is_weekday(result)
        assert predicate(result, date)

    @given(date=dates())
    def test_zero(self, date: dt.date) -> None:
        _ = assume(is_weekday(date))
        result = add_weekdays(date, n=0)
        assert result == date

    @given(date=dates())
    @settings(suppress_health_check={HealthCheck.filter_too_much})
    def test_error(self, date: dt.date) -> None:
        _ = assume(not is_weekday(date))
        with raises(IsWeekendError):
            _ = add_weekdays(date, n=0)

    @given(date=dates(), n1=integers(-10, 10), n2=integers(-10, 10))
    def test_two(self, date: dt.date, n1: int, n2: int) -> None:
        with assume_does_not_raise(IsWeekendError, OverflowError):
            weekday1, weekday2 = (add_weekdays(date, n=n) for n in [n1, n2])
        result = weekday1 <= weekday2
        expected = n1 <= n2
        assert result is expected


class TestDateToDatetime:
    @given(date=dates())
    def test_main(self, date: dt.date) -> None:
        result = date_to_datetime(date).date()
        assert result == date


class TestEnsure:
    @given(data=data())
    @mark.parametrize(
        ("strategy", "func"),
        [
            param(dates(), ensure_date),
            param(datetimes(timezones=just(UTC)), ensure_datetime),
            param(times(), ensure_time),
            param(timedeltas(), ensure_timedelta),
        ],
    )
    def test_main(
        self,
        data: DataObject,
        strategy: SearchStrategy[Any],
        func: Callable[[Any], Any],
    ) -> None:
        value = data.draw(strategy)
        maybe_value = data.draw(sampled_from([value, str(value)]))
        result = func(maybe_value)
        assert result == value


class TestIsWeekday:
    @given(date=dates())
    def test_is_weekday(self, date: dt.date) -> None:
        result = is_weekday(date)
        name = date.strftime("%A")
        expected = name in {
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
        }
        assert result is expected


class TestLocalTimeZone:
    def test_main(self) -> None:
        tz = local_timezone()
        now = dt.datetime.now(tz=UTC)
        result = tz.tzname(now)
        expected = {"HKT", "JST", "UTC"}
        assert result in expected


class TestMaybeMaybeSubPctY:
    @given(text=text_clean())
    @mark.skipif(SYSTEM is not System.linux, reason="Linux only")
    def test_main(self, text: str) -> None:
        result = maybe_sub_pct_y(text)
        assert not search("%Y", result)


class TestParseDate:
    @given(date=dates())
    def test_str(self, date: dt.date) -> None:
        result = parse_date(str(date))
        assert result == date

    @given(date=dates())
    def test_isoformat(self, date: dt.date) -> None:
        result = parse_date(date.isoformat())
        assert result == date

    @given(date=dates())
    def test_yyyymmdd(self, date: dt.date) -> None:
        result = parse_date(date.strftime(maybe_sub_pct_y("%Y%m%d")))
        assert result == date

    def test_error(self) -> None:
        with raises(ParseDateError):
            _ = parse_date("error")


class TestParseDateTime:
    @given(datetime=datetimes(timezones=just(UTC)))
    def test_str(self, datetime: dt.datetime) -> None:
        result = parse_datetime(str(datetime))
        assert result == datetime

    @given(datetime=datetimes(timezones=just(UTC)))
    def test_isoformat(self, datetime: dt.datetime) -> None:
        result = parse_datetime(datetime.isoformat())
        assert result == datetime

    @given(
        datetime=datetimes(timezones=just(UTC)),
        fmt=sampled_from(["%Y%m%dT%H%M%S.%f%z", "%Y-%m-%d %H:%M:%S.%f%z"]).map(
            maybe_sub_pct_y
        ),
    )
    def test_yyyymmdd_hhmmss_fff_zzzz(
        self, datetime: dt.datetime, fmt: str
    ) -> None:
        result = parse_datetime(datetime.strftime(fmt))
        assert result == datetime

    @given(
        datetime=datetimes(timezones=just(UTC)),
        fmt=sampled_from(["%Y%m%dT%H%M%S.%f", "%Y-%m-%d %H:%M:%S.%f"]).map(
            maybe_sub_pct_y
        ),
    )
    def test_yyyymmdd_hhmmss_fff(self, datetime: dt.datetime, fmt: str) -> None:
        result = parse_datetime(datetime.strftime(fmt))
        assert result == datetime

    @given(
        datetime=datetimes(timezones=just(UTC)),
        fmt=sampled_from(
            ["%Y%m%dT%H%M%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"]
        ).map(maybe_sub_pct_y),
    )
    def test_yyyymmdd_hhmmss(self, datetime: dt.datetime, fmt: str) -> None:
        datetime = datetime.replace(microsecond=0)
        result = parse_datetime(datetime.strftime(fmt))
        assert result == datetime

    @given(
        datetime=datetimes(timezones=just(UTC)),
        fmt=sampled_from(
            ["%Y%m%dT%H%M", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M"]
        ).map(maybe_sub_pct_y),
    )
    def test_yyyymmdd_hhmm(self, datetime: dt.datetime, fmt: str) -> None:
        datetime = datetime.replace(second=0, microsecond=0)
        result = parse_datetime(datetime.strftime(fmt))
        assert result == datetime

    @given(
        datetime=datetimes(timezones=just(UTC)),
        fmt=sampled_from(["%Y%m%dT%H", "%Y-%m-%d %H", "%Y-%m-%dT%H"]).map(
            maybe_sub_pct_y
        ),
    )
    def test_yyyymmdd_hh(self, datetime: dt.datetime, fmt: str) -> None:
        datetime = datetime.replace(minute=0, second=0, microsecond=0)
        result = parse_datetime(datetime.strftime(fmt))
        assert result == datetime

    @given(
        datetime=datetimes(timezones=just(UTC)),
        fmt=sampled_from(["%Y%m%d", "%Y-%m-%d"]).map(maybe_sub_pct_y),
    )
    def test_yyyymmdd(self, datetime: dt.datetime, fmt: str) -> None:
        datetime = datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        result = parse_datetime(datetime.strftime(fmt))
        assert result == datetime

    def test_error(self) -> None:
        with raises(ParseDateTimeError):
            _ = parse_datetime("error")


class TestParseTime:
    @given(time=times())
    def test_str(self, time: dt.time) -> None:
        result = parse_time(str(time))
        assert result == time

    @given(time=times())
    def test_isoformat(self, time: dt.time) -> None:
        result = parse_time(time.isoformat())
        assert result == time

    @given(time=times(), fmt=sampled_from(["%H%M%S.%f", "%H:%M:%S.%f"]))
    def test_hhmmss_fff(self, time: dt.time, fmt: str) -> None:
        result = parse_time(time.strftime(fmt))
        assert result == time

    @given(time=times(), fmt=sampled_from(["%H%M%S", "%H:%M:%S"]))
    def test_hhmmss(self, time: dt.time, fmt: str) -> None:
        time = time.replace(microsecond=0)
        result = parse_time(time.strftime(fmt))
        assert result == time

    @given(time=times(), fmt=sampled_from(["%H%M", "%H:%M"]))
    def test_hhmm(self, time: dt.time, fmt: str) -> None:
        time = time.replace(second=0, microsecond=0)
        result = parse_time(time.strftime(fmt))
        assert result == time

    @given(time=times(), fmt=sampled_from(["%H", "%H"]))
    def test_hh(self, time: dt.time, fmt: str) -> None:
        time = time.replace(minute=0, second=0, microsecond=0)
        result = parse_time(time.strftime(fmt))
        assert result == time

    def test_error(self) -> None:
        with raises(ParseTimeError):
            _ = parse_time("error")


class TestParseTimedelta:
    @given(timedelta=timedeltas())
    def test_main(self, timedelta: dt.timedelta) -> None:
        result = parse_timedelta(str(timedelta))
        assert result == timedelta

    def test_error(self) -> None:
        with raises(TimedeltaError):
            _ = parse_timedelta("error")


class TestSerialize:
    @given(data=data())
    @mark.parametrize(
        ("strategy", "serialize", "parse"),
        [
            param(dates(), serialize_date, parse_date),
            param(
                datetimes(timezones=just(UTC)),
                serialize_datetime,
                parse_datetime,
            ),
            param(times(), serialize_time, parse_time),
            param(timedeltas(), str, parse_timedelta),
            param(timedeltas(), serialize_timedelta, parse_timedelta),
        ],
    )
    def test_main(
        self,
        data: DataObject,
        strategy: SearchStrategy[Any],
        serialize: Callable[[Any], Any],
        parse: Callable[[Any], Any],
    ) -> None:
        value = data.draw(strategy)
        result = parse(serialize(value))
        assert result == value

    @given(datetime=datetimes())
    def test_serialize_date(self, datetime: dt.datetime) -> None:
        result = parse_date(serialize_date(datetime))
        assert result == datetime.date()


class TestRoundToWeekday:
    @given(date=dates())
    @settings(suppress_health_check={HealthCheck.filter_too_much})
    @mark.parametrize(
        ("func", "predicate", "operator"),
        [
            param(round_to_next_weekday, True, eq),
            param(round_to_next_weekday, False, gt),
            param(round_to_prev_weekday, True, eq),
            param(round_to_prev_weekday, False, lt),
        ],
    )
    def test_main(
        self,
        date: dt.date,
        func: Callable[[dt.date], dt.date],
        predicate: bool,
        operator: Callable[[dt.date, dt.date], bool],
    ) -> None:
        _ = assume(is_weekday(date) is predicate)
        with assume_does_not_raise(OverflowError):
            result = func(date)
        assert operator(result, date)


class TestTimes:
    def test_main(self) -> None:
        assert isinstance(EPOCH_UTC, dt.datetime)
        assert EPOCH_UTC.tzinfo is UTC


class TestTimeZones:
    def test_main(self) -> None:
        assert isinstance(UTC, dt.tzinfo)


class TestYieldWeekdays:
    @given(start=dates(), days=integers(0, 365))
    def test_start_and_end(self, start: dt.date, days: int) -> None:
        with assume_does_not_raise(OverflowError):
            end = start + dt.timedelta(days=days)
        dates = list(yield_weekdays(start=start, end=end))
        assert all(start <= d <= end for d in dates)
        assert all(map(is_weekday, dates))

    @given(start=dates(), days=integers(0, 10))
    def test_start_and_days(self, start: dt.date, days: int) -> None:
        dates = list(yield_weekdays(start=start, days=days))
        assert len(dates) == days
        assert all(d >= start for d in dates)
        assert all(map(is_weekday, dates))

    @given(end=dates(), days=integers(0, 10))
    def test_end_and_days(self, end: dt.date, days: int) -> None:
        dates = list(yield_weekdays(end=end, days=days))
        assert len(dates) == days
        assert all(d <= end for d in dates)
        assert all(map(is_weekday, dates))

    def test_error(self) -> None:
        with raises(CallYieldWeekdaysError):
            _ = list(yield_weekdays())
