import os

from pykude.kude_fe import KudeFe, KudeFeConfig, Margins

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "generated_pdfs")


def read_fixture(name):
    with open(os.path.join(FIXTURES_DIR, name), "r", encoding="utf-8") as f:
        return f.read()


def setup_module():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


class TestKudeFe:
    def test_generate_basic(self):
        xml = read_fixture("factura_electronica.xml")
        kude = KudeFe(xml=xml)
        output_path = os.path.join(OUTPUT_DIR, "kude_fe_basic.pdf")
        kude.output(output_path)
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0

    def test_generate_with_config(self):
        xml = read_fixture("factura_electronica.xml")
        config = KudeFeConfig(
            margins=Margins(top=8, right=8, bottom=8, left=8),
        )
        kude = KudeFe(xml=xml, config=config)
        output_path = os.path.join(OUTPUT_DIR, "kude_fe_configured.pdf")
        kude.output(output_path)
        assert os.path.exists(output_path)

    def test_generate_test_environment(self):
        xml = read_fixture("factura_electronica.xml")
        config = KudeFeConfig(ambiente=2, show_test_watermark=True)
        kude = KudeFe(xml=xml, config=config)
        output_path = os.path.join(OUTPUT_DIR, "kude_fe_test_env.pdf")
        kude.output(output_path)
        assert os.path.exists(output_path)

    def test_output_bytes(self):
        xml = read_fixture("factura_electronica.xml")
        kude = KudeFe(xml=xml)
        pdf_bytes = kude.output()
        assert isinstance(pdf_bytes, (bytes, bytearray))
        assert len(pdf_bytes) > 0

    def test_data_extraction(self):
        xml = read_fixture("factura_electronica.xml")
        kude = KudeFe(xml=xml)
        assert kude.data["emisor"]["nombre"] == "Empresa Demo S.A."
        assert len(kude.data["items"]) == 2
        assert kude.data["totales"]["total_general"] == "1150000"

    def test_generate_many_items_multipage(self):
        """Test PDF generation with 35 items spanning multiple pages."""
        xml = read_fixture("factura_many_items.xml")
        kude = KudeFe(xml=xml)
        output_path = os.path.join(OUTPUT_DIR, "kude_fe_many_items.pdf")
        kude.output(output_path)
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
        assert len(kude.data["items"]) == 35
        assert kude.pages_count >= 2
