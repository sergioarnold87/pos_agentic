import os

from pykude.kude_ticket import KudeTicket, KudeTicketConfig

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "generated_pdfs")


def read_fixture(name):
    with open(os.path.join(FIXTURES_DIR, name), "r", encoding="utf-8") as f:
        return f.read()


def setup_module():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


class TestKudeTicket:
    def test_generate_factura_ticket(self):
        xml = read_fixture("factura_electronica.xml")
        kude = KudeTicket(xml=xml)
        output_path = os.path.join(OUTPUT_DIR, "kude_ticket_factura.pdf")
        kude.output(output_path)
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0

    def test_generate_nota_credito_ticket(self):
        xml = read_fixture("nota_credito.xml")
        kude = KudeTicket(xml=xml)
        output_path = os.path.join(OUTPUT_DIR, "kude_ticket_nce.pdf")
        kude.output(output_path)
        assert os.path.exists(output_path)

    def test_generate_test_environment(self):
        xml = read_fixture("factura_electronica.xml")
        config = KudeTicketConfig(ambiente=2)
        kude = KudeTicket(xml=xml, config=config)
        output_path = os.path.join(OUTPUT_DIR, "kude_ticket_test_env.pdf")
        kude.output(output_path)
        assert os.path.exists(output_path)

    def test_output_bytes(self):
        xml = read_fixture("factura_electronica.xml")
        kude = KudeTicket(xml=xml)
        pdf_bytes = kude.output()
        assert isinstance(pdf_bytes, (bytes, bytearray))
        assert len(pdf_bytes) > 0
