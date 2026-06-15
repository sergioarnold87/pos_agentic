import os

from pykude.xml_helpers import extract_de_data, parse_xml

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


def read_fixture(name):
    with open(os.path.join(FIXTURES_DIR, name), "r", encoding="utf-8") as f:
        return f.read()


class TestParseXml:
    def test_parse_factura(self):
        xml = read_fixture("factura_electronica.xml")
        root = parse_xml(xml)
        assert root is not None

    def test_parse_nota_credito(self):
        xml = read_fixture("nota_credito.xml")
        root = parse_xml(xml)
        assert root is not None


class TestExtractDeData:
    def test_factura_electronica(self):
        xml = read_fixture("factura_electronica.xml")
        root = parse_xml(xml)
        data = extract_de_data(root)

        assert data["cdc"] == "01800695631001001000000612024112917595714694"
        assert data["dv"] == "9"
        assert data["tipo_de"] == "1"
        assert data["timbrado"] == "12345678"
        assert data["establecimiento"] == "001"
        assert data["punto_exp"] == "001"
        assert data["num_doc"] == "0000001"

        # Emisor
        assert data["emisor"]["ruc"] == "80069563"
        assert data["emisor"]["nombre"] == "Empresa Demo S.A."
        assert data["emisor"]["direccion"] == "Av. España 1234"

        # Receptor
        assert data["receptor"]["ruc"] == "4192083"
        assert data["receptor"]["nombre"] == "Cliente Demo S.A."

        # Items
        assert len(data["items"]) == 2
        assert data["items"][0]["codigo"] == "PROD001"
        assert data["items"][0]["descripcion"] == "Producto de prueba"
        assert data["items"][0]["cantidad"] == "2"
        assert data["items"][0]["precio_unitario"] == "500000"

        # Totales
        assert data["totales"]["total_general"] == "1150000"
        assert data["totales"]["total_gs"] == "1150000"
        assert data["totales"]["iva_10"] == "104545"

    def test_nota_credito(self):
        xml = read_fixture("nota_credito.xml")
        root = parse_xml(xml)
        data = extract_de_data(root)

        assert data["tipo_de"] == "5"
        assert data["cam_ncde"] is not None
        assert data["cam_ncde"]["motivo"] == "1"
        assert len(data["doc_asociado"]) == 1

    def test_autofactura(self):
        xml = read_fixture("autofactura.xml")
        root = parse_xml(xml)
        data = extract_de_data(root)

        assert data["tipo_de"] == "4"
        assert data["cam_ae"] is not None
        assert data["cam_ae"]["nombre_vendedor"] == "Juan Vendedor Pérez"

    def test_nota_remision(self):
        xml = read_fixture("nota_remision.xml")
        root = parse_xml(xml)
        data = extract_de_data(root)

        assert data["tipo_de"] == "7"
        assert data["cam_nre"] is not None
        assert data["cam_nre"]["motivo"] == "1"

    def test_nota_debito(self):
        xml = read_fixture("nota_debito.xml")
        root = parse_xml(xml)
        data = extract_de_data(root)

        assert data["tipo_de"] == "6"
        assert data["cam_ncde"] is not None  # NDE reuses gCamNCDE
        assert len(data["doc_asociado"]) == 1

    def test_comprobante_retencion(self):
        xml = read_fixture("comprobante_retencion.xml")
        root = parse_xml(xml)
        data = extract_de_data(root)

        assert data["tipo_de"] == "8"
        assert len(data["items"]) == 0  # CRE has no items
