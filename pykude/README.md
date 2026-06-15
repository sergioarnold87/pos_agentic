# pykude

Python library for generating **KuDE** (Kuatia Documento Electrónico) PDF representations from SIFEN XML documents (Paraguay electronic invoicing system).

Inspired by [BrazilFiscalReport](https://github.com/Engenere/BrazilFiscalReport).

## Installation

```bash
pip install pykude[all]
```

## Quick Start

```python
from pykude import KudeFe

with open("factura.xml", "r", encoding="utf-8") as f:
    xml = f.read()

kude = KudeFe(xml=xml)
kude.output("kude_factura.pdf")
```

## Auto-detect Document Type

```python
from pykude import auto_kude

kude = auto_kude(xml=xml_content)
kude.output("kude.pdf")
```

## Supported Document Types

| KuDE Type | Class | Description |
|-----------|-------|-------------|
| Factura Electrónica (FE) | `KudeFe` | Electronic Invoice |
| Nota de Crédito (NCE) | `KudeNce` | Credit Note |
| Nota de Débito (NDE) | `KudeNde` | Debit Note |
| Autofactura (AFE) | `KudeAfe` | Self-Invoice |
| Nota de Remisión (NRE) | `KudeNre` | Remission Note |
| Comprobante de Retención (CRE) | `KudeCre` | Withholding Certificate |

## Configuration

```python
from pykude.kude_fe import KudeFe, KudeFeConfig, Margins

config = KudeFeConfig(
    logo="path/to/logo.png",
    margins=Margins(top=8, right=8, bottom=8, left=8),
)

kude = KudeFe(xml=xml_content, config=config)
kude.output("kude.pdf")
```

## Ticket Format (80mm thermal printer)

```python
from pykude.kude_ticket import KudeTicket

kude = KudeTicket(xml=xml_content)
kude.output("ticket.pdf")
```

## CLI

```bash
# Generate KuDE from XML
pfr kude-fe factura.xml -o kude.pdf

# With logo
pfr kude-fe factura.xml --logo logo.png -o kude.pdf

# Ticket format
pfr kude-fe factura.xml --format ticket -o ticket.pdf
```

## Development

```bash
git clone https://github.com/KMEE/pykude.git
cd pykude
pip install -e ".[all,test]"
pytest
```

## License

MIT License - Copyright (c) 2024-2026 KMEE

## Author

mileo (mileo@kmee.com.br)
