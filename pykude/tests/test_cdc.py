from pykude.cdc import calculate_dv_mod11, generate_cdc, validate_cdc


class TestCalculateDvMod11:
    def test_basic(self):
        result = calculate_dv_mod11("123456789")
        assert isinstance(result, int)
        assert 0 <= result <= 10

    def test_known_value(self):
        # The CDC from the factura sample minus the last digit
        code = "0180069563100100100000061202411291759571469"
        dv = calculate_dv_mod11(code)
        assert isinstance(dv, int)


class TestValidateCdc:
    def test_wrong_length(self):
        assert validate_cdc("123") is False

    def test_non_digits(self):
        assert validate_cdc("A" * 44) is False

    def test_empty(self):
        assert validate_cdc("") is False

    def test_none(self):
        assert validate_cdc(None) is False


class TestGenerateCdc:
    def test_generates_44_digits(self):
        cdc = generate_cdc(
            tipo_doc=1,
            ruc_emisor="80069563",
            dv_emisor="1",
            establecimiento="001",
            punto_exp="001",
            numero_doc="0000006",
            tipo_contribuyente="1",
            fecha_emision="20241129",
            tipo_emision=1,
            codigo_seguridad="175957146",
        )
        assert len(cdc) == 44
        assert cdc.isdigit()

    def test_validates(self):
        cdc = generate_cdc(
            tipo_doc=1,
            ruc_emisor="80069563",
            dv_emisor="1",
            establecimiento="001",
            punto_exp="001",
            numero_doc="0000001",
            tipo_contribuyente="1",
            fecha_emision="20241129",
            tipo_emision=1,
            codigo_seguridad="000000001",
        )
        assert validate_cdc(cdc) is True
