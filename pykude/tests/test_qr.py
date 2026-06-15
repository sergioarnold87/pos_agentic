from pykude.qr import generate_qr_image, generate_qr_url


class TestGenerateQrUrl:
    def test_basic(self):
        url = generate_qr_url(
            cdc="01800695631001001000000612024112917595714694",
            fecha_emision="2024-11-29T17:59:57",
            ruc_receptor="4192083",
            total_general="1150000",
            total_iva="104545",
            cant_items="2",
        )
        assert "ekuatia.set.gov.py" in url
        assert "nVersion=150" in url
        assert "01800695631001001000000612024112917595714694" in url

    def test_with_csc(self):
        url = generate_qr_url(
            cdc="01800695631001001000000612024112917595714694",
            id_csc="0001",
            csc="ABCD1234",
        )
        assert "IdCSC=0001" in url
        assert "cHashQR=" in url


class TestGenerateQrImage:
    def test_generates_png(self):
        url = "https://ekuatia.set.gov.py/consultas/qr?nVersion=150"
        img_bytes = generate_qr_image(url)
        assert isinstance(img_bytes, bytes)
        assert len(img_bytes) > 0
        # PNG magic bytes
        assert img_bytes[:4] == b"\x89PNG"
