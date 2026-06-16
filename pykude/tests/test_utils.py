from pykude.utils import (
    format_cdc,
    format_documento,
    format_fecha,
    format_guaranies,
    format_number,
    format_ruc,
)


class TestFormatGuaranies:
    def test_basic(self):
        assert format_guaranies(1500000) == "Gs. 1.500.000"

    def test_zero(self):
        assert format_guaranies(0) == "Gs. 0"

    def test_string_input(self):
        assert format_guaranies("1150000") == "Gs. 1.150.000"

    def test_invalid(self):
        assert format_guaranies("abc") == "Gs. 0"

    def test_none(self):
        assert format_guaranies(None) == "Gs. 0"

    def test_custom_symbol(self):
        assert format_guaranies(1000, symbol="USD") == "USD 1.000"


class TestFormatNumber:
    def test_integer(self):
        assert format_number(1500000) == "1.500.000"

    def test_string(self):
        assert format_number("50") == "50"


class TestFormatRuc:
    def test_basic(self):
        assert format_ruc("80069563", "1") == "80069563-1"


class TestFormatDocumento:
    def test_basic(self):
        assert format_documento("1", "1", "1") == "001-001-0000001"

    def test_full(self):
        assert format_documento("001", "001", "0000001") == "001-001-0000001"


class TestFormatFecha:
    def test_datetime(self):
        assert format_fecha("2024-11-29T17:59:57") == "29/11/2024 17:59:57"

    def test_date_only(self):
        assert format_fecha("2024-01-01") == "01/01/2024"

    def test_empty(self):
        assert format_fecha("") == ""


class TestFormatCdc:
    def test_basic(self):
        cdc = "01800695631001001000000612024112917595714694"
        result = format_cdc(cdc)
        assert result.startswith("0180")
        assert " " in result

    def test_empty(self):
        assert format_cdc("") == ""
