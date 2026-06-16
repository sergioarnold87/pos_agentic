import os

from pykude.kude_nce import KudeNce

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "generated_pdfs")


def read_fixture(name):
    with open(os.path.join(FIXTURES_DIR, name), "r", encoding="utf-8") as f:
        return f.read()


def setup_module():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


class TestKudeNce:
    def test_generate_basic(self):
        xml = read_fixture("nota_credito.xml")
        kude = KudeNce(xml=xml)
        output_path = os.path.join(OUTPUT_DIR, "kude_nce_basic.pdf")
        kude.output(output_path)
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0

    def test_data_extraction(self):
        xml = read_fixture("nota_credito.xml")
        kude = KudeNce(xml=xml)
        assert kude.data["tipo_de"] == "5"
        assert kude.data["cam_ncde"] is not None
        assert len(kude.data["doc_asociado"]) == 1

    def test_output_bytes(self):
        xml = read_fixture("nota_credito.xml")
        kude = KudeNce(xml=xml)
        pdf_bytes = kude.output()
        assert isinstance(pdf_bytes, (bytes, bytearray))
        assert len(pdf_bytes) > 0
