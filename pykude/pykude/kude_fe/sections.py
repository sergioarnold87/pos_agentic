from pykude.base import FOOTER_HEIGHT
from pykude.utils import (
    TIPO_DOCUMENTO,
    format_documento,
    format_fecha,
    format_guaranies,
    format_number,
    format_ruc,
)


def draw_header(pdf, data, config):
    """
    Draw header: Logo + Issuer data + Timbrado/Number.

    Three columns: Logo (22%) | Issuer (45%) | Document info (33%)
    """
    y_start = pdf.get_y()
    page_width = pdf.w - config.margins.left - config.margins.right

    logo_w = page_width * 0.22
    emisor_w = page_width * 0.45
    tim_w = page_width * 0.33

    header_h = 30

    # Column 1: Logo
    if config.logo:
        try:
            pdf.image(
                config.logo,
                x=config.margins.left + 2,
                y=y_start + 2,
                w=logo_w - 4,
                h=header_h - 4,
                keep_aspect_ratio=True,
            )
        except Exception:
            pass

    # Column 2: Issuer data
    emisor_x = config.margins.left + logo_w
    emisor = data["emisor"]

    pdf.set_xy(emisor_x, y_start + 2)
    pdf.set_font(config.font_type.value, "B", 10)
    pdf.cell(emisor_w, 5, emisor["nombre"], new_x="LEFT", new_y="NEXT")

    pdf.set_x(emisor_x)
    pdf.set_font(config.font_type.value, "", 7)
    ruc = f"RUC: {format_ruc(emisor['ruc'], emisor['dv_ruc'])}"
    pdf.cell(emisor_w, 3.5, ruc, new_x="LEFT", new_y="NEXT")

    pdf.set_x(emisor_x)
    direccion = emisor["direccion"]
    if emisor.get("num_casa"):
        direccion += f" Nro. {emisor['num_casa']}"
    pdf.cell(emisor_w, 3.5, direccion, new_x="LEFT", new_y="NEXT")

    pdf.set_x(emisor_x)
    location = " - ".join(
        filter(None, [emisor.get("ciudad"), emisor.get("departamento")])
    )
    pdf.cell(emisor_w, 3.5, location, new_x="LEFT", new_y="NEXT")

    if emisor.get("telefono"):
        pdf.set_x(emisor_x)
        pdf.cell(
            emisor_w, 3.5, f"Tel: {emisor['telefono']}", new_x="LEFT", new_y="NEXT"
        )

    if emisor.get("email"):
        pdf.set_x(emisor_x)
        pdf.cell(emisor_w, 3.5, emisor["email"], new_x="LEFT", new_y="NEXT")

    if emisor.get("actividades"):
        pdf.set_x(emisor_x)
        act_text = ", ".join(a["descripcion"] for a in emisor["actividades"])
        pdf.set_font(config.font_type.value, "", 6)
        pdf.cell(
            emisor_w, 3, f"Act. Econ.: {act_text}", new_x="LEFT", new_y="NEXT"
        )

    # Column 3: Document info
    tim_x = emisor_x + emisor_w
    pdf.set_xy(tim_x, y_start + 2)
    pdf.set_font(config.font_type.value, "B", 8)
    pdf.cell(
        tim_w, 4, f"Timbrado N\u00b0: {data['timbrado']}", new_x="LEFT", new_y="NEXT", align="C"
    )

    pdf.set_x(tim_x)
    pdf.set_font(config.font_type.value, "", 6)
    validity = (
        f"Inicio Vigencia: {format_fecha(data.get('fecha_ini_timbrado', ''))}"
    )
    pdf.cell(tim_w, 3.5, validity, new_x="LEFT", new_y="NEXT", align="C")

    pdf.set_x(tim_x)
    tipo_de = data.get("desc_tipo_de", TIPO_DOCUMENTO.get(data["tipo_de"], ""))
    # Shrink font if document type name is too wide for the column
    font_size = 9
    pdf.set_font(config.font_type.value, "B", font_size)
    while pdf.get_string_width(tipo_de.upper()) > tim_w - 2 and font_size > 5:
        font_size -= 0.5
        pdf.set_font(config.font_type.value, "B", font_size)
    pdf.cell(tim_w, 5, tipo_de.upper(), new_x="LEFT", new_y="NEXT", align="C")

    pdf.set_x(tim_x)
    num_doc = format_documento(
        data["establecimiento"], data["punto_exp"], data["num_doc"]
    )
    pdf.set_font(config.font_type.value, "B", 10)
    pdf.cell(tim_w, 5, num_doc, new_x="LEFT", new_y="NEXT", align="C")

    # CDC
    pdf.set_x(tim_x)
    pdf.set_font(config.font_type.value, "", 5)
    pdf.cell(
        tim_w, 3, f"CDC: {data['cdc']}", new_x="LEFT", new_y="NEXT", align="C"
    )

    # Draw border
    pdf.rect(config.margins.left, y_start, page_width, header_h)
    # Vertical lines
    pdf.line(emisor_x, y_start, emisor_x, y_start + header_h)
    pdf.line(tim_x, y_start, tim_x, y_start + header_h)

    pdf.set_xy(config.margins.left, y_start + header_h)


def draw_receptor(pdf, data, config):
    """Draw receiver data section."""
    pdf.set_x(config.margins.left)
    y_start = pdf.get_y()
    page_width = pdf.w - config.margins.left - config.margins.right
    receptor = data["receptor"]

    pdf.set_font(config.font_type.value, "B", 7)
    pdf.set_x(config.margins.left)
    pdf.cell(page_width, 4, "DATOS DEL RECEPTOR", align="C", new_x="LEFT", new_y="NEXT")

    col_w = page_width / 2
    pdf.set_font(config.font_type.value, "", 7)

    # Row 1: Name and RUC
    pdf.set_x(config.margins.left)
    nombre = f"Nombre/Raz\u00f3n Social: {receptor['nombre']}"
    pdf.cell(col_w, 4, nombre, new_x="RIGHT")

    if receptor.get("ruc"):
        ruc_text = f"RUC: {format_ruc(receptor['ruc'], receptor.get('dv_ruc', ''))}"
    elif receptor.get("num_doc_id"):
        ruc_text = f"Doc. ID: {receptor['num_doc_id']}"
    else:
        ruc_text = ""
    pdf.cell(col_w, 4, ruc_text, new_x="LEFT", new_y="NEXT")

    # Row 2: Address and phone
    pdf.set_x(config.margins.left)
    if receptor.get("direccion"):
        pdf.cell(col_w, 4, f"Direcci\u00f3n: {receptor['direccion']}", new_x="RIGHT")
    else:
        pdf.cell(col_w, 4, "", new_x="RIGHT")

    if receptor.get("telefono"):
        pdf.cell(col_w, 4, f"Tel: {receptor['telefono']}", new_x="LEFT", new_y="NEXT")
    elif receptor.get("email"):
        pdf.cell(col_w, 4, f"Email: {receptor['email']}", new_x="LEFT", new_y="NEXT")
    else:
        pdf.cell(col_w, 4, "", new_x="LEFT", new_y="NEXT")

    section_h = pdf.get_y() - y_start
    pdf.rect(config.margins.left, y_start, page_width, section_h)


def draw_operacion(pdf, data, config):
    """Draw operation condition section (cash/credit, currency, etc.)."""
    pdf.set_x(config.margins.left)
    y_start = pdf.get_y()
    page_width = pdf.w - config.margins.left - config.margins.right
    condicion = data.get("condicion", {})

    pdf.set_font(config.font_type.value, "B", 7)
    pdf.set_x(config.margins.left)
    pdf.cell(
        page_width, 4, "DATOS DE LA OPERACI\u00d3N", align="C", new_x="LEFT", new_y="NEXT"
    )

    pdf.set_font(config.font_type.value, "", 7)
    pdf.set_x(config.margins.left)

    col_w = page_width / 3

    # Condition
    cond_text = f"Condici\u00f3n: {condicion.get('descripcion', '')}"
    pdf.cell(col_w, 4, cond_text, new_x="RIGHT")

    # Currency
    moneda = data.get("desc_moneda", data.get("moneda", ""))
    pdf.cell(col_w, 4, f"Moneda: {moneda}", new_x="RIGHT")

    # Transaction type
    tipo_trans = data.get("desc_tipo_transaccion", "")
    pdf.cell(col_w, 4, f"Tipo Trans.: {tipo_trans}", new_x="LEFT", new_y="NEXT")

    # Payment details
    if condicion.get("pagos"):
        pdf.set_x(config.margins.left)
        pagos_text = []
        for pago in condicion["pagos"]:
            monto = format_guaranies(pago.get("monto", "0"))
            pagos_text.append(f"{pago.get('descripcion', '')} - {monto}")
        pdf.cell(
            page_width, 4, f"Forma de Pago: {'; '.join(pagos_text)}", new_x="LEFT", new_y="NEXT"
        )

    # Fecha de emisión
    pdf.set_x(config.margins.left)
    fecha = format_fecha(data.get("fecha_emision", ""))
    pdf.cell(page_width, 4, f"Fecha de Emisi\u00f3n: {fecha}", new_x="LEFT", new_y="NEXT")

    section_h = pdf.get_y() - y_start
    pdf.rect(config.margins.left, y_start, page_width, section_h)


def draw_items(pdf, data, config):
    """Draw items table with automatic page break."""
    pdf.set_x(config.margins.left)
    page_width = pdf.w - config.margins.left - config.margins.right

    pdf.set_font(config.font_type.value, "B", 7)
    pdf.set_x(config.margins.left)
    pdf.cell(page_width, 4, "DETALLE DE ITEMS", align="C", new_x="LEFT", new_y="NEXT")

    cols = [
        ("C\u00f3d.", 18),
        ("Descripci\u00f3n", page_width - 18 - 15 - 18 - 25 - 12 - 25),
        ("Unid.", 15),
        ("Cant.", 18),
        ("P. Unit.", 25),
        ("IVA", 12),
        ("Subtotal", 25),
    ]

    _draw_items_header(pdf, cols, config)

    pdf.set_font(config.font_type.value, "", 7)
    items = data.get("items", [])

    for item in items:
        # Check page break — reserve space for totals (~30mm) within footer area
        if pdf.get_y() + 5 > pdf.h - config.margins.bottom - FOOTER_HEIGHT - 30:
            pdf.add_page()
            _draw_items_header(pdf, cols, config)
            pdf.set_font(config.font_type.value, "", 7)

        x = config.margins.left
        pdf.set_x(x)
        pdf.cell(cols[0][1], 5, item.get("codigo", "")[:8], border=1)
        pdf.cell(
            cols[1][1], 5, item.get("descripcion", "")[:50], border=1
        )
        pdf.cell(cols[2][1], 5, item.get("desc_unidad", ""), border=1, align="C")
        pdf.cell(
            cols[3][1], 5, format_number(item.get("cantidad", "0")), border=1, align="R"
        )
        pdf.cell(
            cols[4][1],
            5,
            format_guaranies(item.get("precio_unitario", "0")),
            border=1,
            align="R",
        )
        tasa = item.get("tasa_iva", "0")
        pdf.cell(cols[5][1], 5, f"{tasa}%", border=1, align="C")
        pdf.cell(
            cols[6][1],
            5,
            format_guaranies(item.get("total_item", "0")),
            border=1,
            align="R",
        )
        pdf.ln()

    # If no items, add empty row
    if not items:
        pdf.set_x(config.margins.left)
        pdf.cell(page_width, 5, "Sin items", border=1, align="C")
        pdf.ln()


def _draw_items_header(pdf, cols, config):
    """Draw items table header."""
    pdf.set_font(config.font_type.value, "B", 7)
    pdf.set_x(config.margins.left)
    for label, w in cols:
        pdf.cell(w, 5, label, border=1, align="C")
    pdf.ln()


def draw_totales(pdf, data, config):
    """Draw totals section: IVA subtotals + grand total."""
    # Ensure enough space for totals (~25mm)
    if pdf.get_y() + 25 > pdf.h - config.margins.bottom - FOOTER_HEIGHT:
        pdf.add_page()
    pdf.set_x(config.margins.left)
    y_start = pdf.get_y()
    page_width = pdf.w - config.margins.left - config.margins.right
    totales = data.get("totales", {})

    pdf.set_font(config.font_type.value, "B", 7)
    pdf.set_x(config.margins.left)
    pdf.cell(
        page_width, 4, "SUBTOTALES / TOTALES", align="C", new_x="LEFT", new_y="NEXT"
    )

    col_w = page_width / 3
    pdf.set_font(config.font_type.value, "", 7)

    # Row 1: Subtotals by IVA rate
    pdf.set_x(config.margins.left)
    sub10 = format_guaranies(totales.get("sub_10", "0"))
    sub5 = format_guaranies(totales.get("sub_5", "0"))
    sub_exe = format_guaranies(totales.get("sub_exento", "0"))
    pdf.cell(col_w, 4, f"Subtotal IVA 10%: {sub10}", new_x="RIGHT")
    pdf.cell(col_w, 4, f"Subtotal IVA 5%: {sub5}", new_x="RIGHT")
    pdf.cell(col_w, 4, f"Subtotal Exento: {sub_exe}", new_x="LEFT", new_y="NEXT")

    # Row 2: IVA liquidation
    pdf.set_x(config.margins.left)
    iva10 = format_guaranies(totales.get("iva_10", "0"))
    iva5 = format_guaranies(totales.get("iva_5", "0"))
    total_iva = format_guaranies(totales.get("total_iva", "0"))
    pdf.cell(col_w, 4, f"Liq. IVA 10%: {iva10}", new_x="RIGHT")
    pdf.cell(col_w, 4, f"Liq. IVA 5%: {iva5}", new_x="RIGHT")
    pdf.cell(col_w, 4, f"Total IVA: {total_iva}", new_x="LEFT", new_y="NEXT")

    # Row 3: Discounts
    desc = totales.get("total_descuento", "0")
    if int(float(desc)) > 0:
        pdf.set_x(config.margins.left)
        pdf.cell(
            page_width, 4, f"Total Descuento: {format_guaranies(desc)}", new_x="LEFT", new_y="NEXT"
        )

    # Grand total
    pdf.set_x(config.margins.left)
    pdf.set_font(config.font_type.value, "B", 9)
    total = format_guaranies(totales.get("total_general", "0"))
    pdf.cell(page_width, 6, f"TOTAL GENERAL: {total}", align="R", new_x="LEFT", new_y="NEXT")

    section_h = pdf.get_y() - y_start
    pdf.rect(config.margins.left, y_start, page_width, section_h)


def draw_test_watermark(pdf, config):
    """Draw 'SIN VALIDEZ TRIBUTARIA' watermark for test environment."""
    if config.ambiente == 2 and config.show_test_watermark:
        pdf.set_font(config.font_type.value, "B", 40)
        pdf.set_text_color(220, 220, 220)
        # Draw diagonally across the page
        x = pdf.w / 2 - 60
        y = pdf.h / 2
        with pdf.rotation(45, x + 60, y):
            pdf.text(x, y, "SIN VALIDEZ TRIBUTARIA")
        pdf.set_text_color(0, 0, 0)
