"""Base KuDE class with common footer for all A4 document types."""

from io import BytesIO

from fpdf import FPDF

from pykude.utils import format_cdc, format_fecha

# QR (25) + text padding (4) + disclaimer (8) = ~37mm
FOOTER_HEIGHT = 37


class KudeBase(FPDF):
    """Base class for all A4 KuDE types. Provides automatic page footer with QR + CDC."""

    _qr_cache = None

    def _get_qr(self):
        """Generate and cache QR code bytes + URL."""
        if self._qr_cache is None:
            from pykude.qr import generate_qr_from_data

            try:
                qr_bytes, qr_url = generate_qr_from_data(self.data, self.config)
                self._qr_cache = (qr_bytes, qr_url)
            except Exception:
                self._qr_cache = (None, self.data.get("qr_url", ""))
        return self._qr_cache

    def footer(self):
        """Draw footer on every page: QR code + CDC info + legal disclaimer."""
        page_width = self.w - self.config.margins.left - self.config.margins.right
        footer_y = self.h - self.config.margins.bottom - FOOTER_HEIGHT

        # --- QR + CDC section ---
        qr_bytes, qr_url = self._get_qr()
        qr_size = 25

        self.set_xy(self.config.margins.left, footer_y)
        y_start = footer_y

        if qr_bytes:
            self.image(
                BytesIO(qr_bytes),
                x=self.config.margins.left + 2,
                y=y_start + 2,
                w=qr_size,
                h=qr_size,
            )

        info_x = self.config.margins.left + qr_size + 5
        self.set_xy(info_x, y_start + 2)
        self.set_font(self.config.font_type.value, "", 6)
        self.cell(0, 3, f"CDC: {format_cdc(self.data['cdc'])}", new_x="LEFT", new_y="NEXT")

        self.set_x(info_x)
        self.cell(
            0, 3,
            f"Fecha de emisión: {format_fecha(self.data.get('fecha_emision', ''))}",
            new_x="LEFT", new_y="NEXT",
        )

        self.set_x(info_x)
        self.cell(
            0, 3,
            f"Código de seguridad: {self.data.get('codigo_seguridad', '')}",
            new_x="LEFT", new_y="NEXT",
        )

        self.set_x(info_x)
        display_url = qr_url if len(qr_url) <= 80 else qr_url[:77] + "..."
        self.cell(0, 3, f"Consulte en: {display_url}", new_x="LEFT", new_y="NEXT")

        self.set_x(info_x)
        tipo_emi = self.data.get("desc_tipo_emision", "Normal")
        self.cell(0, 3, f"Tipo emisión: {tipo_emi}", new_x="LEFT", new_y="NEXT")

        qr_section_h = max(self.get_y() - y_start, qr_size + 4)
        self.rect(self.config.margins.left, y_start, page_width, qr_section_h)

        # --- Legal disclaimer ---
        disclaimer_y = y_start + qr_section_h + 1
        self.set_xy(self.config.margins.left, disclaimer_y)
        self.set_font(self.config.font_type.value, "I", 6)
        self.cell(
            page_width, 3,
            "Este documento es la representación gráfica de un Documento Tributario Electrónico (DTE)",
            align="C", new_x="LEFT", new_y="NEXT",
        )
        self.set_x(self.config.margins.left)
        self.cell(
            page_width, 3,
            "Consulte la validez de este DTE en: https://ekuatia.set.gov.py/consultas",
            align="C",
        )
