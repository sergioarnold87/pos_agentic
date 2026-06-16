# pykude

Python library for generating KuDE (Kuatia Documento Electrónico) PDF representations
from SIFEN XML documents (Paraguay electronic invoicing system).

## Project Overview

- **Architecture**: Follows BrazilFiscalReport pattern — XML → parse → draw PDF with fpdf2
- **Namespace**: `http://ekuatia.set.gov.py/sifen/xsd`
- **Manual Técnico**: SIFEN v150 (sections 13.6 and 13.7 for KuDE layout)
- **Sister project**: sifenlib (XML bindings at /home/mileo/agents/sifenlib)

## Key Conventions

- Each KuDE type lives in its own subpackage: `kude_fe/`, `kude_nce/`, etc.
- Each subpackage has: `__init__.py`, `config.py`, `kude_*.py` (main class inheriting FPDF), `sections.py`
- Config uses Python dataclasses
- XML parsing via lxml with namespace-aware helpers in `xml_helpers.py`
- Values formatted in Guaraníes (Gs.) with dot separators: `Gs. 1.500.000`
- CDC is 44-digit control code, validated with módulo 11

## Document Types

| Type | iTiDE | Class | Description |
|------|-------|-------|-------------|
| FE | 1 | KudeFe | Factura Electrónica |
| NCE | 5 | KudeNce | Nota de Crédito Electrónica |
| NDE | 6 | KudeNde | Nota de Débito Electrónica |
| AFE | 4 | KudeAfe | Autofactura Electrónica |
| NRE | 7 | KudeNre | Nota de Remisión Electrónica |
| CRE | 8 | KudeCre | Comprobante de Retención Electrónico |

## Development

```bash
pip install -e ".[all,test]"
pytest
ruff check .
```

## Testing

- Test fixtures in `tests/fixtures/` (XML samples from sifenlib)
- Visual PDF output tests generate to `tests/generated_pdfs/`
- Run: `pytest -v`

## File Structure

```
pykude/
├── __init__.py          # version + auto_kude()
├── __main__.py          # CLI (click)
├── utils.py             # format_guaranies, format_ruc, format_documento, etc.
├── xml_helpers.py       # parse_xml, get_text, extract_de_data
├── cdc.py               # CDC generation/validation (mod 11)
├── qr.py                # QR code URL + image generation
├── kude_fe/             # Factura Electrónica
├── kude_nce/            # Nota de Crédito
├── kude_nde/            # Nota de Débito
├── kude_afe/            # Autofactura
├── kude_nre/            # Nota de Remisión
├── kude_cre/            # Comprobante de Retención
└── kude_ticket/         # Formato ticket 80mm
```

## Author & License

- Author: mileo (mileo@kmee.com.br)
- Copyright: KMEE
- License: MIT
