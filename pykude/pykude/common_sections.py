"""Common drawing sections shared across multiple KuDE types."""

from pykude.utils import format_cdc


def draw_doc_asociado(pdf, data, config):
    """Draw associated document section (for NCE/NDE references)."""
    docs = data.get("doc_asociado", [])
    if not docs:
        return

    pdf.set_x(config.margins.left)
    y_start = pdf.get_y()
    page_width = pdf.w - config.margins.left - config.margins.right

    pdf.set_font(config.font_type.value, "B", 7)
    pdf.set_x(config.margins.left)
    pdf.cell(
        page_width, 4, "DOCUMENTO ASOCIADO", align="C", new_x="LEFT", new_y="NEXT"
    )

    pdf.set_font(config.font_type.value, "", 7)
    for doc in docs:
        pdf.set_x(config.margins.left)
        tipo = doc.get("desc_tipo", "")
        if doc.get("cdc_ref"):
            cdc = format_cdc(doc["cdc_ref"])
            pdf.cell(
                page_width, 4, f"Tipo: {tipo} - CDC: {cdc}", new_x="LEFT", new_y="NEXT"
            )
        elif doc.get("nro_doc"):
            pdf.cell(
                page_width,
                4,
                f"Tipo: {tipo} - Nro: {doc['nro_doc']}",
                new_x="LEFT",
                new_y="NEXT",
            )

    section_h = pdf.get_y() - y_start
    pdf.rect(config.margins.left, y_start, page_width, section_h)


def draw_motivo_emision(pdf, data, config, motivo_data, title="MOTIVO DE EMISIÓN"):
    """Draw emission reason section (for NCE/NDE)."""
    if not motivo_data:
        return

    pdf.set_x(config.margins.left)
    y_start = pdf.get_y()
    page_width = pdf.w - config.margins.left - config.margins.right

    pdf.set_font(config.font_type.value, "B", 7)
    pdf.set_x(config.margins.left)
    pdf.cell(page_width, 4, title, align="C", new_x="LEFT", new_y="NEXT")

    pdf.set_font(config.font_type.value, "", 7)
    pdf.set_x(config.margins.left)
    motivo = motivo_data.get("desc_motivo", "")
    pdf.cell(page_width, 4, f"Motivo: {motivo}", new_x="LEFT", new_y="NEXT")

    section_h = pdf.get_y() - y_start
    pdf.rect(config.margins.left, y_start, page_width, section_h)
