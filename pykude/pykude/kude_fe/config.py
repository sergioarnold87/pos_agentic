from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Union


class FontType(Enum):
    HELVETICA = "Helvetica"
    COURIER = "Courier"
    TIMES = "Times"


class PaperFormat(Enum):
    CARTA = "A4"
    TICKET = "TICKET"


@dataclass
class Margins:
    top: float = 5.0
    right: float = 5.0
    bottom: float = 5.0
    left: float = 5.0


@dataclass
class KudeFeConfig:
    """Configuration for KuDE Factura Electrónica."""

    logo: Optional[Union[str, bytes]] = None
    margins: Margins = field(default_factory=Margins)
    font_type: FontType = FontType.HELVETICA
    paper_format: PaperFormat = PaperFormat.CARTA
    csc: Optional[str] = None
    csc_id: Optional[str] = None
    ambiente: int = 1
    show_test_watermark: bool = True
    language: str = "es"
