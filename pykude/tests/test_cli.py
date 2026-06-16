import os
import subprocess
import sys

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "generated_pdfs")


def setup_module():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


class TestCli:
    def test_auto_command(self):
        xml_path = os.path.join(FIXTURES_DIR, "factura_electronica.xml")
        output_path = os.path.join(OUTPUT_DIR, "cli_auto.pdf")
        result = subprocess.run(
            [sys.executable, "-m", "pykude", "auto", xml_path, "-o", output_path],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert os.path.exists(output_path)

    def test_kude_fe_command(self):
        xml_path = os.path.join(FIXTURES_DIR, "factura_electronica.xml")
        output_path = os.path.join(OUTPUT_DIR, "cli_kude_fe.pdf")
        result = subprocess.run(
            [sys.executable, "-m", "pykude", "kude-fe", xml_path, "-o", output_path],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert os.path.exists(output_path)

    def test_ticket_format(self):
        xml_path = os.path.join(FIXTURES_DIR, "factura_electronica.xml")
        output_path = os.path.join(OUTPUT_DIR, "cli_ticket.pdf")
        result = subprocess.run(
            [
                sys.executable, "-m", "pykude",
                "kude-fe", xml_path, "--format", "ticket", "-o", output_path,
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert os.path.exists(output_path)

    def test_test_environment(self):
        xml_path = os.path.join(FIXTURES_DIR, "factura_electronica.xml")
        output_path = os.path.join(OUTPUT_DIR, "cli_test_env.pdf")
        result = subprocess.run(
            [
                sys.executable, "-m", "pykude",
                "kude-fe", xml_path, "--test", "-o", output_path,
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert os.path.exists(output_path)
