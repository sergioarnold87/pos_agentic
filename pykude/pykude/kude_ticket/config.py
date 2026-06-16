from dataclasses import dataclass, field
from typing import Optional, Union

from pykude.kude_fe.config import FontType, Margins


@dataclass
class KudeTicketConfig:
    """Configuration for KuDE in ticket format (80mm thermal printer)."""

    logo: Optional[Union[str, bytes]] = None
    margins: Margins = field(default_factory=lambda: Margins(top=3, right=3, bottom=3, left=3))
    font_type: FontType = FontType.HELVETICA
    csc: Optional[str] = None
    csc_id: Optional[str] = None
    ambiente: int = 1
    show_test_watermark: bool = True
    # Paper width in mm (80mm standard thermal)
    paper_width: float = 80.0
