from __future__ import annotations

from locale import CRNCYSTR
from locale import LC_ALL
from locale import LC_MONETARY
from locale import nl_langinfo
from locale import setlocale

from pytest import mark
from pytest import param

from utilities.locale import atof
from utilities.locale import get_locale_for_platform
from utilities.locale import override_locale


class TestAToF:
    @mark.parametrize(
        ("text", "expected"),
        [
            param("0.00", 0.0),
            param("1.23", 1.23),
            param("12.34", 12.34),
            param("123.45", 123.45),
            param("1,234.56", 1234.56),
        ],
    )
    def test_main(self, *, text: str, expected: float) -> None:
        plat_locale = get_locale_for_platform("en_US")
        assert atof(text, locale=plat_locale) == expected


class TestGetLocaleForPlatform:
    def test_main(self) -> None:
        plat_locale = get_locale_for_platform("en_US")
        _ = setlocale(LC_ALL, locale=plat_locale)


class TestOverrideLocale:
    def test_main(self) -> None:
        plat_locale = get_locale_for_platform("en_US")
        with override_locale(LC_MONETARY, locale=plat_locale):
            assert nl_langinfo(CRNCYSTR) == "-$"
