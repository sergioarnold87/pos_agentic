from fpdf import FPDF

from pykude.kude_ticket.config import KudeTicketConfig
from pykude.kude_ticket.sections import (
    draw_ticket_header,
    draw_ticket_items,
    draw_ticket_qr,
    draw_ticket_receptor,
    draw_ticket_totales,
    draw_ticket_watermark,
)
from pykude.xml_helpers import extract_de_data, parse_xml


class KudeTicket(FPDF):
    """
    Generate KuDE in ticket format (80mm thermal printer).

    Usage:
        kude = KudeTicket(xml=xml_content)
        kude.output("ticket.pdf")
    """

    def __init__(self, xml, config=None):
        self.config = config or KudeTicketConfig()

        # 80mm width, variable height (we'll use a tall page and trim)
        super().__init__(
            orientation="P",
            unit="mm",
            format=(self.config.paper_width, 297),
        )

        root = parse_xml(xml)
        self.data = extract_de_data(root)

        self.set_auto_page_break(auto=False)
        self.set_margins(
            self.config.margins.left,
            self.config.margins.top,
            self.config.margins.right,
        )

        self.add_page()
        self._draw()

    def _draw(self):
        if self.config.ambiente == 2:
            draw_ticket_watermark(self, self.config)

        draw_ticket_header(self, self.data, self.config)
        draw_ticket_receptor(self, self.data, self.config)
        draw_ticket_items(self, self.data, self.config)
        draw_ticket_totales(self, self.data, self.config)
        draw_ticket_qr(self, self.data, self.config)
