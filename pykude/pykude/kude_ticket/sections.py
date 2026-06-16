"""Ticket (80mm) format sections — compact vertical layout."""

from io import BytesIO

from pykude.utils import (
    TIPO_DOCUMENTO,
    format_documento,
    format_fecha,
    format_guaranies,
    format_number,
    format_ruc,
)


def draw_ticket_header(pdf, data, config):
    """Draw compact header for ticket format."""
    page_width = config.paper_width - config.margins.left - config.margins.right
    emisor = data["emisor"]

    # Logo
    if config.logo:
        try:
            pdf.image(
                config.logo,
                x=config.margins.left + page_width / 2 - 10,
                y=pdf.get_y(),
                w=20,
                h=10,
                keep_aspect_ratio=True,
            )
            pdf.set_y(pdf.get_y() + 11)
        except Exception:
            pass

    # Issuer name centered
    pdf.set_font(config.font_type.value, "B", 8)
    pdf.cell(page_width, 4, emisor["nombre"], align="C", new_x="LEFT", new_y="NEXT")

    pdf.set_font(config.font_type.value, "", 6)
    ruc = f"RUC: {format_ruc(emisor['ruc'], emisor['dv_ruc'])}"
    pdf.cell(page_width, 3, ruc, align="C", new_x="LEFT", new_y="NEXT")

    pdf.cell(page_width, 3, emisor["direccion"], align="C", new_x="LEFT", new_y="NEXT")

    if emisor.get("telefono"):
        pdf.cell(
            page_width, 3, f"Tel: {emisor['telefono']}", align="C", new_x="LEFT", new_y="NEXT"
        )

    # Separator
    _draw_separator(pdf, config)

    # Document type and number
    tipo_de = data.get("desc_tipo_de", TIPO_DOCUMENTO.get(data["tipo_de"], ""))
    pdf.set_font(config.font_type.value, "B", 7)
    pdf.cell(page_width, 4, tipo_de.upper(), align="C", new_x="LEFT", new_y="NEXT")

    num_doc = format_documento(data["establecimiento"], data["punto_exp"], data["num_doc"])
    pdf.set_font(config.font_type.value, "B", 8)
    pdf.cell(page_width, 4, num_doc, align="C", new_x="LEFT", new_y="NEXT")

    pdf.set_font(config.font_type.value, "", 6)
    pdf.cell(
        page_width, 3,
        f"Timbrado: {data['timbrado']}",
        align="C", new_x="LEFT", new_y="NEXT",
    )

    fecha = format_fecha(data.get("fecha_emision", ""))
    pdf.cell(page_width, 3, f"Fecha: {fecha}", align="C", new_x="LEFT", new_y="NEXT")

    _draw_separator(pdf, config)


def draw_ticket_receptor(pdf, data, config):
    """Draw compact receiver info."""
    page_width = config.paper_width - config.margins.left - config.margins.right
    receptor = data["receptor"]

    pdf.set_font(config.font_type.value, "", 6)
    pdf.cell(page_width, 3, f"Cliente: {receptor['nombre']}", new_x="LEFT", new_y="NEXT")

    if receptor.get("ruc"):
        ruc_text = f"RUC: {format_ruc(receptor['ruc'], receptor.get('dv_ruc', ''))}"
        pdf.cell(page_width, 3, ruc_text, new_x="LEFT", new_y="NEXT")

    _draw_separator(pdf, config)


def draw_ticket_items(pdf, data, config):
    """Draw compact items list for ticket."""
    page_width = config.paper_width - config.margins.left - config.margins.right
    items = data.get("items", [])

    if not items:
        return

    pdf.set_font(config.font_type.value, "B", 6)
    # Header: Desc | Cant | P.U. | Subtotal
    desc_w = page_width * 0.40
    cant_w = page_width * 0.12
    pu_w = page_width * 0.24
    sub_w = page_width * 0.24

    pdf.cell(desc_w, 3, "Descripción", new_x="RIGHT")
    pdf.cell(cant_w, 3, "Cant.", align="R", new_x="RIGHT")
    pdf.cell(pu_w, 3, "P.Unit.", align="R", new_x="RIGHT")
    pdf.cell(sub_w, 3, "Subtotal", align="R", new_x="LEFT", new_y="NEXT")

    _draw_separator(pdf, config, char="-")

    pdf.set_font(config.font_type.value, "", 6)
    for item in items:
        pdf.cell(desc_w, 3, item.get("descripcion", "")[:20], new_x="RIGHT")
        pdf.cell(cant_w, 3, format_number(item.get("cantidad", "0")), align="R", new_x="RIGHT")
        pdf.cell(pu_w, 3, format_guaranies(item.get("precio_unitario", "0")), align="R", new_x="RIGHT")
        pdf.cell(sub_w, 3, format_guaranies(item.get("total_item", "0")), align="R", new_x="LEFT", new_y="NEXT")

    _draw_separator(pdf, config)


def draw_ticket_totales(pdf, data, config):
    """Draw compact totals for ticket."""
    page_width = config.paper_width - config.margins.left - config.margins.right
    totales = data.get("totales", {})

    label_w = page_width * 0.5
    val_w = page_width * 0.5

    pdf.set_font(config.font_type.value, "", 6)

    sub10 = totales.get("sub_10", "0")
    if int(float(sub10)) > 0:
        pdf.cell(label_w, 3, "Subtotal IVA 10%:", new_x="RIGHT")
        pdf.cell(val_w, 3, format_guaranies(sub10), align="R", new_x="LEFT", new_y="NEXT")

    sub5 = totales.get("sub_5", "0")
    if int(float(sub5)) > 0:
        pdf.cell(label_w, 3, "Subtotal IVA 5%:", new_x="RIGHT")
        pdf.cell(val_w, 3, format_guaranies(sub5), align="R", new_x="LEFT", new_y="NEXT")

    sub_exe = totales.get("sub_exento", "0")
    if int(float(sub_exe)) > 0:
        pdf.cell(label_w, 3, "Subtotal Exento:", new_x="RIGHT")
        pdf.cell(val_w, 3, format_guaranies(sub_exe), align="R", new_x="LEFT", new_y="NEXT")

    total_iva = totales.get("total_iva", "0")
    if int(float(total_iva)) > 0:
        pdf.cell(label_w, 3, "Total IVA:", new_x="RIGHT")
        pdf.cell(val_w, 3, format_guaranies(total_iva), align="R", new_x="LEFT", new_y="NEXT")

    pdf.set_font(config.font_type.value, "B", 7)
    pdf.cell(label_w, 4, "TOTAL:", new_x="RIGHT")
    pdf.cell(
        val_w, 4,
        format_guaranies(totales.get("total_general", "0")),
        align="R", new_x="LEFT", new_y="NEXT",
    )

    _draw_separator(pdf, config)


def draw_ticket_qr(pdf, data, config):
    """Draw compact QR code for ticket."""
    from pykude.qr import generate_qr_from_data

    page_width = config.paper_width - config.margins.left - config.margins.right

    try:
        qr_bytes, qr_url = generate_qr_from_data(data, config)
        qr_size = 20
        x_center = config.margins.left + (page_width - qr_size) / 2
        pdf.image(BytesIO(qr_bytes), x=x_center, y=pdf.get_y(), w=qr_size, h=qr_size)
        pdf.set_y(pdf.get_y() + qr_size + 1)
    except Exception:
        pass

    pdf.set_font(config.font_type.value, "", 4)
    cdc = data.get("cdc", "")
    pdf.cell(page_width, 2, f"CDC: {cdc}", align="C", new_x="LEFT", new_y="NEXT")

    pdf.set_font(config.font_type.value, "I", 5)
    pdf.cell(
        page_width, 3,
        "Consulte en: https://ekuatia.set.gov.py/consultas",
        align="C", new_x="LEFT", new_y="NEXT",
    )


def draw_ticket_watermark(pdf, config):
    """Draw test watermark for ticket format."""
    if config.ambiente == 2 and config.show_test_watermark:
        pdf.set_font(config.font_type.value, "B", 12)
        pdf.set_text_color(200, 200, 200)
        page_width = config.paper_width - config.margins.left - config.margins.right
        pdf.cell(
            page_width, 5,
            "SIN VALIDEZ TRIBUTARIA",
            align="C", new_x="LEFT", new_y="NEXT",
        )
        pdf.set_text_color(0, 0, 0)


def _draw_separator(pdf, config, char="="):
    """Draw a separator line using characters."""
    page_width = config.paper_width - config.margins.left - config.margins.right
    chars = int(page_width / 1.5)
    pdf.set_font(config.font_type.value, "", 5)
    pdf.cell(page_width, 2, char * chars, align="C", new_x="LEFT", new_y="NEXT")
