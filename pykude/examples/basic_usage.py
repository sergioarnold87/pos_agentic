"""Basic usage example for ParaguayFiscalReport."""

import os

from pykude import auto_kude
from pykude.kude_fe import KudeFe, KudeFeConfig, Margins

# Path to sample XML
SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "..", "tests", "fixtures")


def example_basic():
    """Generate a basic KuDE from a factura XML."""
    xml_path = os.path.join(SAMPLES_DIR, "factura_electronica.xml")
    with open(xml_path, "r", encoding="utf-8") as f:
        xml = f.read()

    kude = KudeFe(xml=xml)
    kude.output("kude_factura.pdf")
    print("Generated: kude_factura.pdf")


def example_with_config():
    """Generate a KuDE with custom configuration."""
    xml_path = os.path.join(SAMPLES_DIR, "factura_electronica.xml")
    with open(xml_path, "r", encoding="utf-8") as f:
        xml = f.read()

    config = KudeFeConfig(
        margins=Margins(top=8, right=8, bottom=8, left=8),
        ambiente=2,  # Test environment (adds watermark)
        show_test_watermark=True,
    )

    kude = KudeFe(xml=xml, config=config)
    kude.output("kude_factura_configured.pdf")
    print("Generated: kude_factura_configured.pdf")


def example_auto_detect():
    """Auto-detect document type and generate KuDE."""
    for filename in os.listdir(SAMPLES_DIR):
        if not filename.endswith(".xml"):
            continue

        xml_path = os.path.join(SAMPLES_DIR, filename)
        with open(xml_path, "r", encoding="utf-8") as f:
            xml = f.read()

        kude = auto_kude(xml=xml)
        output_name = filename.replace(".xml", "_kude.pdf")
        kude.output(output_name)
        print(f"Generated: {output_name} (type: {type(kude).__name__})")


def example_ticket():
    """Generate a ticket format KuDE (80mm thermal printer)."""
    from pykude.kude_ticket import KudeTicket

    xml_path = os.path.join(SAMPLES_DIR, "factura_electronica.xml")
    with open(xml_path, "r", encoding="utf-8") as f:
        xml = f.read()

    kude = KudeTicket(xml=xml)
    kude.output("kude_ticket.pdf")
    print("Generated: kude_ticket.pdf")


def example_bytes_output():
    """Get PDF as bytes (useful for web frameworks)."""
    xml_path = os.path.join(SAMPLES_DIR, "factura_electronica.xml")
    with open(xml_path, "r", encoding="utf-8") as f:
        xml = f.read()

    kude = KudeFe(xml=xml)
    pdf_bytes = kude.output()
    print(f"PDF size: {len(pdf_bytes)} bytes")
    return pdf_bytes


if __name__ == "__main__":
    example_basic()
    example_with_config()
    example_auto_detect()
    example_ticket()
    example_bytes_output()
