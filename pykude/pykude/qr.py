import hashlib
from io import BytesIO


def generate_qr_url(
    cdc,
    fecha_emision="",
    ruc_receptor="",
    total_general="0",
    total_iva="0",
    cant_items="0",
    digest_value="",
    id_csc="",
    csc="",
    ambiente=1,
):
    """
    Generate the QR code URL as per Manual Técnico section 13.7.2.

    If CSC is provided, generates the cHashQR verification hash.
    """
    base_url = "https://ekuatia.set.gov.py/consultas/qr"

    params = f"nVersion=150&Id={cdc}&dFeEmiDE={fecha_emision}"
    params += f"&dRucRec={ruc_receptor}"
    params += f"&dTotGralOpe={total_general}"
    params += f"&dTotIVA={total_iva}"
    params += f"&cItems={cant_items}"
    params += f"&DigestValue={digest_value}"

    if id_csc and csc:
        params += f"&IdCSC={id_csc}"
        hash_input = f"{cdc}{csc}"
        hash_qr = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()
        params += f"&cHashQR={hash_qr}"

    return f"{base_url}?{params}"


def generate_qr_image(url, box_size=4):
    """Generate a QR code image from URL, returning PNG bytes."""
    try:
        import qrcode
    except ImportError:
        raise ImportError(
            "qrcode package required. Install with: pip install pykude[qrcode]"
        )

    qr = qrcode.QRCode(box_size=box_size, border=1)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def generate_qr_from_data(data, config=None):
    """Generate QR code image from extracted DE data."""
    csc = getattr(config, "csc", "") or "" if config else ""
    csc_id = getattr(config, "csc_id", "") or "" if config else ""

    url = data.get("qr_url", "")
    if not url or url == "https://ekuatia.set.gov.py/consultas/qr?nVersion=150":
        url = generate_qr_url(
            cdc=data.get("cdc", ""),
            fecha_emision=data.get("fecha_emision", ""),
            ruc_receptor=data.get("receptor", {}).get("ruc", ""),
            total_general=data.get("totales", {}).get("total_general", "0"),
            total_iva=data.get("totales", {}).get("total_iva", "0"),
            cant_items=str(len(data.get("items", []))),
            id_csc=csc_id,
            csc=csc,
        )

    return generate_qr_image(url), url
