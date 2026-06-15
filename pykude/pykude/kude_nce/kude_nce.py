from pykude.base import FOOTER_HEIGHT, KudeBase
from pykude.common_sections import draw_doc_asociado, draw_motivo_emision
from pykude.kude_fe.sections import (
    draw_header,
    draw_items,
    draw_operacion,
    draw_receptor,
    draw_test_watermark,
    draw_totales,
)
from pykude.kude_nce.config import KudeNceConfig
from pykude.xml_helpers import extract_de_data, parse_xml


class KudeNce(KudeBase):
    """
    Generate KuDE for Nota de Crédito Electrónica (Electronic Credit Note).

    Usage:
        kude = KudeNce(xml=xml_content)
        kude.output("kude_nce.pdf")
    """

    def __init__(self, xml, config=None):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.config = config or KudeNceConfig()

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
        draw_motivo_emision(self, self.data, self.config, self.data.get("cam_ncde"))
        draw_doc_asociado(self, self.data, self.config)
        draw_operacion(self, self.data, self.config)
        draw_items(self, self.data, self.config)
        draw_totales(self, self.data, self.config)
