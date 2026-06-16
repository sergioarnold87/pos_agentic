"""Autofactura-specific sections."""


def draw_vendedor(pdf, data, config):
    """Draw vendor/supplier data section specific to Autofactura."""
    cam_ae = data.get("cam_ae")
    if not cam_ae:
        return

    pdf.set_x(config.margins.left)
    y_start = pdf.get_y()
    page_width = pdf.w - config.margins.left - config.margins.right

    pdf.set_font(config.font_type.value, "B", 7)
    pdf.set_x(config.margins.left)
    pdf.cell(
        page_width, 4, "DATOS DEL VENDEDOR", align="C", new_x="LEFT", new_y="NEXT"
    )

    col_w = page_width / 2
    pdf.set_font(config.font_type.value, "", 7)

    pdf.set_x(config.margins.left)
    pdf.cell(col_w, 4, f"Nombre: {cam_ae.get('nombre_vendedor', '')}", new_x="RIGHT")
    id_text = f"{cam_ae.get('desc_tipo_id_vendedor', '')}: {cam_ae.get('num_id_vendedor', '')}"
    pdf.cell(col_w, 4, id_text, new_x="LEFT", new_y="NEXT")

    pdf.set_x(config.margins.left)
    pdf.cell(
        page_width, 4,
        f"Dirección: {cam_ae.get('direccion_vendedor', '')}",
        new_x="LEFT", new_y="NEXT",
    )

    pdf.set_x(config.margins.left)
    pdf.cell(
        col_w, 4,
        f"Tipo: {cam_ae.get('desc_tipo_consulta', '')}",
        new_x="RIGHT",
    )
    pdf.cell(
        col_w, 4,
        f"Nro. Consulta: {cam_ae.get('num_consulta', '')}",
        new_x="LEFT", new_y="NEXT",
    )

    section_h = pdf.get_y() - y_start
    pdf.rect(config.margins.left, y_start, page_width, section_h)
