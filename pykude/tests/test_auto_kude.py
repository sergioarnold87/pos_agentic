import os

from pykude import auto_kude
from pykude.kude_afe import KudeAfe
from pykude.kude_cre import KudeCre
from pykude.kude_fe import KudeFe
from pykude.kude_nce import KudeNce
from pykude.kude_nde import KudeNde
from pykude.kude_nre import KudeNre

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "generated_pdfs")


def read_fixture(name):
    with open(os.path.join(FIXTURES_DIR, name), "r", encoding="utf-8") as f:
        return f.read()


def setup_module():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


class TestAutoKude:
    def test_auto_detect_factura(self):
        xml = read_fixture("factura_electronica.xml")
        kude = auto_kude(xml=xml)
        assert isinstance(kude, KudeFe)

    def test_auto_detect_nota_credito(self):
        xml = read_fixture("nota_credito.xml")
        kude = auto_kude(xml=xml)
        assert isinstance(kude, KudeNce)

    def test_auto_detect_nota_debito(self):
        xml = read_fixture("nota_debito.xml")
        kude = auto_kude(xml=xml)
        assert isinstance(kude, KudeNde)

    def test_auto_detect_autofactura(self):
        xml = read_fixture("autofactura.xml")
        kude = auto_kude(xml=xml)
        assert isinstance(kude, KudeAfe)

    def test_auto_detect_nota_remision(self):
        xml = read_fixture("nota_remision.xml")
        kude = auto_kude(xml=xml)
        assert isinstance(kude, KudeNre)

    def test_auto_detect_comprobante_retencion(self):
        xml = read_fixture("comprobante_retencion.xml")
        kude = auto_kude(xml=xml)
        assert isinstance(kude, KudeCre)

    def test_all_documents_generate_pdf(self):
        """Integration test: generate PDFs for all document types."""
        fixtures = [
            ("factura_electronica.xml", "auto_factura.pdf"),
            ("nota_credito.xml", "auto_nce.pdf"),
            ("nota_debito.xml", "auto_nde.pdf"),
            ("autofactura.xml", "auto_afe.pdf"),
            ("nota_remision.xml", "auto_nre.pdf"),
            ("comprobante_retencion.xml", "auto_cre.pdf"),
        ]
        for xml_file, pdf_file in fixtures:
            xml = read_fixture(xml_file)
            kude = auto_kude(xml=xml)
            output_path = os.path.join(OUTPUT_DIR, pdf_file)
            kude.output(output_path)
            assert os.path.exists(output_path), f"Failed to generate {pdf_file}"
            assert os.path.getsize(output_path) > 0, f"Empty PDF: {pdf_file}"
