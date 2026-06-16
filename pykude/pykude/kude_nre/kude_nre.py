from pykude.base import FOOTER_HEIGHT, KudeBase
from pykude.kude_fe.sections import (
    draw_header,
    draw_items,
    draw_receptor,
    draw_test_watermark,
)
from pykude.kude_nre.config import KudeNreConfig
from pykude.kude_nre.sections import draw_remision_info
from pykude.xml_helpers import extract_de_data, parse_xml


class KudeNre(KudeBase):
    """
    Generate KuDE for Nota de Remisión Electrónica.

    Usage:
        kude = KudeNre(xml=xml_content)
        kude.output("kude_nre.pdf")
    """

    def __init__(self, xml, config=None):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.config = config or KudeNreConfig()

        root = parse_xml(xml)
        self.data = extract_de_data(root)

        self.set_auto_page_break(auto=True, margin=self.config.margins.bottom + FOOTER_HEIGHT)
        self.set_margins(
            self.config.margins.left,
            self.config.margins.top,
            self.config.margins.right,
        )

        self.add_page()
        self._draw()

    def _draw(self):
        if self.config.ambiente == 2:
            draw_test_watermark(self, self.config)

        draw_header(self, self.data, self.config)
        draw_receptor(self, self.data, self.config)
        draw_remision_info(self, self.data, self.config)
        draw_items(self, self.data, self.config)
