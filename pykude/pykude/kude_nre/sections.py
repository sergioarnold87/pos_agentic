"""Nota de Remisión-specific sections."""


def draw_remision_info(pdf, data, config):
    """Draw remission-specific info (motivo, responsable)."""
    cam_nre = data.get("cam_nre")
    if not cam_nre:
        return

    pdf.set_x(config.margins.left)
    y_start = pdf.get_y()
    page_width = pdf.w - config.margins.left - config.margins.right

    pdf.set_font(config.font_type.value, "B", 7)
    pdf.set_x(config.margins.left)
    pdf.cell(
        page_width, 4, "DATOS DE REMISIÓN", align="C", new_x="LEFT", new_y="NEXT"
    )

    pdf.set_font(config.font_type.value, "", 7)
    col_w = page_width / 2

    pdf.set_x(config.margins.left)
    pdf.cell(
        col_w, 4,
        f"Motivo: {cam_nre.get('desc_motivo', '')}",
        new_x="RIGHT",
    )

    resp_map = {"1": "Emisor", "2": "Receptor", "3": "Tercero"}
    resp = resp_map.get(cam_nre.get("responsable", ""), "")
    pdf.cell(col_w, 4, f"Responsable: {resp}", new_x="LEFT", new_y="NEXT")

    section_h = pdf.get_y() - y_start
    pdf.rect(config.margins.left, y_start, page_width, section_h)
