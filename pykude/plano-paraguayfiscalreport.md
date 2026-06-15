# Plano de Desenvolvimento: ParaguayFiscalReport

**Biblioteca Python para geração de KuDE (representação gráfica em PDF) dos Documentos Eletrônicos do SIFEN — no estilo BrazilFiscalReport**

---

## 1. Visão Geral

### O que é

A **ParaguayFiscalReport** (ou `paraguayfiscalreport`) será uma biblioteca Python para gerar os **KuDE** (Kuatia Documento Electrónico) em PDF a partir dos XMLs do SIFEN do Paraguai. Segue a mesma arquitetura do [BrazilFiscalReport](https://github.com/Engenere/BrazilFiscalReport): recebe XML → extrai dados → desenha PDF com fpdf2.

### O que é o KuDE

KuDE é a **representação gráfica** do Documento Electrónico (DE) em formato PDF ou impresso. Conforme definido pela SET (Subsecretaría de Estado de Tributación):

- Tem validez tributária desde que coincida com o DTE no SIFEN
- Obrigatório quando o receptor não é facturador electrónico
- Não pode ser impresso em impressora matricial
- Deve ser legível por no mínimo 6 meses
- Inclui QR Code para verificação online

### Documentos suportados (equivalência)

| KuDE Paraguay (SIFEN) | Equivalente Brasil | BrazilFiscalReport |
|------------------------|--------------------|--------------------|
| KuDE Factura Electrónica (FE) | DANFE (NF-e) | `Danfe` |
| KuDE Nota de Crédito Electrónica (NCE) | — | — |
| KuDE Nota de Débito Electrónica (NDE) | — | — |
| KuDE Autofactura Electrónica (AFE) | — | — |
| KuDE Nota de Remisión Electrónica (NRE) | DAMDFE (MDF-e) | `Damdfe` |
| KuDE Comprobante de Retención (CRE) | — | — |
| KuDE Factura Exportación (FEX) | — | — |

### Formatos do KuDE (Manual Técnico v150)

O Manual Técnico define dois formatos de KuDE:

- **Formato 1 — Papel Carta** (ou similar): Layout completo tipo A4/Carta, para impressoras laser/jato de tinta
- **Formato 2 — Cinta de papel** (ticket): Layout compacto para impressoras térmicas de 80mm

---

## 2. Análise da Arquitetura do BrazilFiscalReport

### Padrão de design (a replicar)

```
brazilfiscalreport/
├── __init__.py          # __version__
├── __main__.py          # CLI (click)
├── utils.py             # Funções utilitárias (format_cpf, get_tag_text, etc.)
├── danfe/
│   ├── __init__.py      # re-exports: Danfe, DanfeConfig, ...
│   ├── config.py        # DanfeConfig (dataclass com opções de customização)
│   ├── danfe.py         # Classe principal Danfe(FPDF) — herda de FPDF
│   ├── danfe_conf.py    # Constantes do layout (larguras, alturas, margens)
│   └── generate.py      # Funções de desenho (draw_header, draw_items, etc.)
├── dacte/
│   ├── __init__.py
│   ├── config.py
│   ├── dacte.py         # Classe Dacte(FPDF)
│   └── ...
├── damdfe/
│   └── ...
└── dacce/
    └── ...
```

### Padrão de cada documento

1. **Config (dataclass)**: Contém opções de personalização (logo, margens, fonte, etc.)
2. **Classe principal (herda de FPDF)**: `__init__` recebe XML string + config, parseia o XML, e chama métodos de desenho
3. **Métodos de desenho**: Cada seção do documento é um método (cabeçalho, emitente, destinatário, itens, totais, QR code, etc.)
4. **Output**: `.output("arquivo.pdf")` ou `.output()` retorna bytes

### Dependências-chave

| Lib | Uso |
|-----|-----|
| `fpdf2` | Geração do PDF (core) |
| `python-barcode` | Código de barras |
| `qrcode` | QR Code |
| `phonenumbers` | Formatação de telefones |
| `lxml` ou `xml.etree` | Parsing do XML |

---

## 3. Estrutura do Projeto

```
paraguayfiscalreport/
├── pyproject.toml
├── README.md
├── LICENSE                              # LGPL-3.0 (mesmo do BrazilFiscalReport)
├── .gitignore
├── .pre-commit-config.yaml
├── requirements.txt
├── paraguayfiscalreport/
│   ├── __init__.py                      # __version__ = "0.1.0"
│   ├── __main__.py                      # CLI com click
│   ├── utils.py                         # Utilitários compartilhados
│   ├── xml_helpers.py                   # Helpers para extração de dados do XML SIFEN
│   ├── cdc.py                           # Geração/validação do CDC (44 dígitos)
│   ├── qr.py                            # Geração da URL do QR Code conforme MT 13.7.2
│   ├── fonts/                           # Fontes TTF embutidas (se necessário)
│   │   └── ...
│   ├── kude_fe/                         # KuDE Factura Electrónica
│   │   ├── __init__.py
│   │   ├── config.py                    # KudeFeConfig
│   │   ├── kude_fe.py                   # Classe KudeFe(FPDF)
│   │   ├── layout.py                    # Constantes de layout
│   │   └── sections.py                  # Funções de desenho por seção
│   ├── kude_nce/                        # KuDE Nota de Crédito Electrónica
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── kude_nce.py
│   │   └── sections.py
│   ├── kude_nde/                        # KuDE Nota de Débito Electrónica
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── kude_nde.py
│   │   └── sections.py
│   ├── kude_afe/                        # KuDE Autofactura Electrónica
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── kude_afe.py
│   │   └── sections.py
│   ├── kude_nre/                        # KuDE Nota de Remisión Electrónica
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── kude_nre.py
│   │   └── sections.py
│   ├── kude_cre/                        # KuDE Comprobante de Retención
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── kude_cre.py
│   │   └── sections.py
│   └── kude_ticket/                     # KuDE formato cinta/ticket (80mm)
│       ├── __init__.py
│       ├── config.py
│       ├── kude_ticket.py
│       └── sections.py
├── tests/
│   ├── __init__.py
│   ├── fixtures/                        # XMLs de exemplo para testes
│   │   ├── factura_electronica.xml
│   │   ├── nota_credito.xml
│   │   ├── nota_debito.xml
│   │   ├── autofactura.xml
│   │   ├── nota_remision.xml
│   │   └── comprobante_retencion.xml
│   ├── expected_pdfs/                   # PDFs esperados para comparação visual
│   ├── test_kude_fe.py
│   ├── test_kude_nce.py
│   ├── test_qr.py
│   ├── test_cdc.py
│   └── test_utils.py
├── docs/
│   ├── assets/
│   │   └── banner.svg
│   ├── index.md
│   ├── kude_fe.md
│   └── ...
├── mkdocs.yml
├── streamlit_app.py                     # App demo "Try it Online"
└── .github/
    └── workflows/
        └── tests.yml
```

---

## 4. Layout do KuDE — Seções Obrigatórias

Baseado no Manual Técnico v150, seções 13.6 e 13.7, o KuDE tem as seguintes seções:

### 4.1 KuDE Factura Electrónica — Formato 1 (Papel Carta)

(Gráfica Nº 09 do Manual Técnico v150)

```
┌──────────────────────────────────────────────────┐
│  LOGO │ DATOS DEL EMISOR      │ TIMBRADO / NRO   │
│       │ RUC, Nombre, Dirección│ Tipo Documento    │
│       │ Teléfono, Email       │ Nro. Factura      │
│       │ Actividades Económicas│ CDC (44 dígitos)  │
├──────────────────────────────────────────────────┤
│              DATOS DEL RECEPTOR                   │
│  RUC/CI, Nombre, Dirección, Teléfono, Email       │
├──────────────────────────────────────────────────┤
│              DATOS DE LA OPERACIÓN                │
│  Tipo transacción, Moneda, Condición (Contado/    │
│  Crédito), Forma de pago                          │
├──────────────────────────────────────────────────┤
│  DETALLE DE ITEMS                                 │
│  Código │ Descripción │ Unidad │ Cant. │ P.Unit │ │
│         │             │        │       │ Subtotal│ │
│  ───────┼─────────────┼────────┼───────┼─────────│ │
│  001    │ Producto A  │ UNI    │ 10    │ 50.000  │ │
│  ...    │ ...         │ ...    │ ...   │ ...     │ │
├──────────────────────────────────────────────────┤
│              SUBTOTALES / TOTALES                 │
│  Subtotal IVA 10%    │ Subtotal IVA 5%  │ Exento │
│  Liquidación IVA 10% │ Liquidación IVA 5%│        │
│  TOTAL GENERAL:  Gs. XXX.XXX.XXX                 │
├──────────────────────────────────────────────────┤
│  QR CODE │ INFO COMPLEMENTARIA                    │
│  ┌─────┐ │ CDC: 0180069563...                     │
│  │ QR  │ │ Fecha/Hora emisión                     │
│  │     │ │ URL de consulta SIFEN                  │
│  └─────┘ │ Código de Seguridad                    │
├──────────────────────────────────────────────────┤
│  INFORMACIÓN ADICIONAL DE INTERÉS                 │
│  (Observaciones del emisor)                       │
└──────────────────────────────────────────────────┘
```

### 4.2 KuDE Formato 2 — Cinta de Papel (Ticket 80mm)

Layout compacto, vertical, para impressoras térmicas. Todas as informações obrigatórias, mas com largura fixa de 80mm (~302 pts fpdf2).

### 4.3 Campos obrigatórios por tipo de KuDE (MT v150, seção 13.6)

| Campo | FE | NCE | NDE | AFE | NRE | CRE |
|-------|----|-----|-----|-----|-----|-----|
| Timbrado (dNumTim) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Nro. Documento (dEst-dPunExp-dNumDoc) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| CDC (Id, 44 dígitos) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Dígito verificador (dDVId) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Datos Emisor (gEmis) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Datos Receptor (gDest) | ✓ | ✓ | ✓ | ✓ | — | ✓ |
| Condición de operación | ✓ | — | — | ✓ | — | — |
| Detalle de ítems (gCamItem) | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| Subtotales IVA | ✓ | ✓ | ✓ | ✓ | — | — |
| Total general | ✓ | ✓ | ✓ | ✓ | — | ✓ |
| QR Code | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Datos del transporte (gTransp) | — | — | — | — | ✓ | — |
| Doc. asociado (NCE/NDE ref.) | — | ✓ | ✓ | — | — | — |

---

## 5. Implementação Técnica

### 5.1 Parsing do XML

O XML do SIFEN usa o namespace `http://ekuatia.set.gov.py/sifen/xsd`. O helper de parsing abstrai isso:

```python
# xml_helpers.py
from lxml import etree

NS = {"sifen": "http://ekuatia.set.gov.py/sifen/xsd"}

def get_text(element, xpath, default=""):
    """Extrai texto de um XPath dentro do namespace SIFEN."""
    node = element.find(xpath, NS)
    return node.text if node is not None and node.text else default

def get_all(element, xpath):
    """Retorna todos os elementos de um XPath."""
    return element.findall(xpath, NS)

def parse_xml(xml_string):
    """Parseia XML string, retornando o root element."""
    return etree.fromstring(xml_string.encode("utf-8"))

def extract_de_data(root):
    """Extrai dados estruturados do DE para geração do KuDE."""
    de = root.find(".//sifen:DE", NS)
    if de is None:
        de = root  # o próprio root pode ser o DE

    data = {
        "cdc": de.get("Id", ""),
        "dv": get_text(de, "sifen:dDVId"),
        # Operação
        "tipo_emision": get_text(de, "sifen:gOpeDE/sifen:iTipEmi"),
        "fecha_emision": get_text(de, "sifen:gDatGralOpe/sifen:dFeEmiDE"),
        # Emisor
        "emisor": {
            "ruc": get_text(de, "sifen:gDatGralOpe/sifen:gEmis/sifen:dRucEm"),
            "dv_ruc": get_text(de, "sifen:gDatGralOpe/sifen:gEmis/sifen:dDVEmi"),
            "nombre": get_text(de, "sifen:gDatGralOpe/sifen:gEmis/sifen:dNomEm"),
            "direccion": get_text(de, "sifen:gDatGralOpe/sifen:gEmis/sifen:dDirEm"),
            "telefono": get_text(de, "sifen:gDatGralOpe/sifen:gEmis/sifen:dTelEm"),
            "email": get_text(de, "sifen:gDatGralOpe/sifen:gEmis/sifen:dEmailE"),
            "timbrado": get_text(de, "sifen:gDatGralOpe/sifen:gEmis/sifen:dNumTim"),
            "establecimiento": get_text(de, "sifen:gDatGralOpe/sifen:gEmis/sifen:dEst"),
            "punto_exp": get_text(de, "sifen:gDatGralOpe/sifen:gEmis/sifen:dPunExp"),
            "num_doc": get_text(de, "sifen:gDatGralOpe/sifen:gEmis/sifen:dNumDoc"),
        },
        # Receptor
        "receptor": { ... },
        # Items
        "items": [ ... ],
        # Totales
        "totales": { ... },
    }
    return data
```

### 5.2 Geração do QR Code (MT v150, seção 13.7.2)

```python
# qr.py
import hashlib

def generate_qr_url(cdc: str, dv: str, ambiente: int = 1) -> str:
    """
    Gera a URL do QR Code conforme Manual Técnico seção 13.7.2.

    Formato: https://ekuatia.set.gov.py/consultas/qr?nVersion=150
             &Id={CDC}&dFeEmiDE={fecha}&dRucRec={ruc_receptor}
             &dTotGralOpe={total}&dTotIVA={total_iva}
             &cItems={cant_items}&DigestValue={hash}
             &IdCSC={id_csc}&cHashQR={hash_qr}
    """
    base_url = "https://ekuatia.set.gov.py/consultas/qr"
    # Montar parâmetros conforme MT
    # ...
    return f"{base_url}?{params}"

def generate_qr_image(url: str, box_size: int = 4) -> bytes:
    """Gera imagem QR a partir da URL."""
    import qrcode
    from io import BytesIO

    qr = qrcode.QRCode(box_size=box_size, border=1)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
```

### 5.3 CDC — Código de Control del Documento Electrónico

```python
# cdc.py

def generate_cdc(
    tipo_doc: int,       # 01-08
    ruc_emisor: str,     # 8 dígitos
    dv_emisor: str,      # 1 dígito
    establecimiento: str,# 3 dígitos
    punto_exp: str,      # 3 dígitos
    numero_doc: str,     # 7 dígitos
    tipo_contribuyente: str,  # 1 dígito (1=Persona Física, 2=Persona Jurídica)
    fecha_emision: str,  # formato YYYYMMDD
    tipo_emision: int,   # 1=Normal, 2=Contingencia
    codigo_seguridad: str,  # 9 dígitos aleatorios
) -> str:
    """
    Gera o CDC de 44 dígitos conforme Manual Técnico seção 6.1.

    Formato: TTRRRRRRRRDDEEEPPPNNNNNNNNCAAAAAAAAAAMMDDDDDDDDDS
    """
    cdc_sin_dv = (
        f"{tipo_doc:02d}"
        f"{ruc_emisor:>08s}"
        f"{dv_emisor}"
        f"{establecimiento:>03s}"
        f"{punto_exp:>03s}"
        f"{numero_doc:>07s}"
        f"{tipo_contribuyente}"
        f"{fecha_emision}"
        f"{tipo_emision}"
        f"{codigo_seguridad:>09s}"
    )

    dv = calculate_dv_mod11(cdc_sin_dv)
    return cdc_sin_dv + str(dv)


def calculate_dv_mod11(code: str) -> int:
    """Calcula dígito verificador módulo 11 conforme MT."""
    weights = [2, 3, 4, 5, 6, 7, 2, 3, 4, 5, 6, 7]  # cíclico
    total = 0
    for i, char in enumerate(reversed(code)):
        total += int(char) * weights[i % len(weights)]
    remainder = total % 11
    if remainder <= 1:
        return 0
    return 11 - remainder
```

### 5.4 Classe KudeFe — Padrão BrazilFiscalReport

```python
# kude_fe/kude_fe.py
from fpdf import FPDF
from ..xml_helpers import parse_xml, extract_de_data
from ..qr import generate_qr_url, generate_qr_image
from .config import KudeFeConfig
from .sections import (
    draw_header,
    draw_emisor,
    draw_receptor,
    draw_operacion,
    draw_items,
    draw_totales,
    draw_qr_section,
    draw_info_adicional,
)

class KudeFe(FPDF):
    """
    Gera o KuDE de Factura Electrónica em PDF.

    Uso:
        kude = KudeFe(xml=xml_content)
        kude.output("kude_factura.pdf")
    """

    def __init__(self, xml: str, config: KudeFeConfig = None):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.config = config or KudeFeConfig()

        # Parsear XML
        root = parse_xml(xml)
        self.data = extract_de_data(root)

        # Configurar
        self.set_auto_page_break(auto=True, margin=self.config.margins.bottom)
        self.set_margins(
            self.config.margins.left,
            self.config.margins.top,
            self.config.margins.right,
        )

        # Adicionar fonte (se customizada)
        if self.config.font_type:
            self._setup_fonts()

        # Gerar
        self.add_page()
        self._draw()

    def _draw(self):
        """Desenha todas as seções do KuDE."""
        draw_header(self, self.data, self.config)
        draw_emisor(self, self.data, self.config)
        draw_receptor(self, self.data, self.config)
        draw_operacion(self, self.data, self.config)
        draw_items(self, self.data, self.config)
        draw_totales(self, self.data, self.config)
        draw_qr_section(self, self.data, self.config)
        draw_info_adicional(self, self.data, self.config)
```

### 5.5 Config (dataclass)

```python
# kude_fe/config.py
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Union


class FontType(Enum):
    HELVETICA = "Helvetica"
    COURIER = "Courier"
    TIMES = "Times"


class PaperFormat(Enum):
    CARTA = "A4"           # Formato 1 - Papel carta
    TICKET = "TICKET"      # Formato 2 - Cinta 80mm


@dataclass
class Margins:
    top: float = 5.0
    right: float = 5.0
    bottom: float = 5.0
    left: float = 5.0


@dataclass
class KudeFeConfig:
    """Configuração do KuDE de Factura Electrónica."""

    # Logo do emissor (path ou bytes)
    logo: Optional[Union[str, bytes]] = None

    # Margens
    margins: Margins = field(default_factory=Margins)

    # Fonte
    font_type: FontType = FontType.HELVETICA

    # Formato do papel
    paper_format: PaperFormat = PaperFormat.CARTA

    # CSC (Código de Seguridad del Contribuyente) para QR
    csc: Optional[str] = None
    csc_id: Optional[str] = None

    # Ambiente (1=Producción, 2=Test)
    ambiente: int = 1

    # Mostrar marca d'água "SIN VALIDEZ TRIBUTARIA" em ambiente test
    show_test_watermark: bool = True

    # Idioma das labels (es=español, gn=guaraní)
    language: str = "es"
```

### 5.6 Funções de Desenho (sections.py)

```python
# kude_fe/sections.py
from fpdf import FPDF


def draw_header(pdf: FPDF, data: dict, config):
    """
    Desenha o cabeçalho: Logo + Dados Emissor + Timbrado/Número.

    ┌─────────┬──────────────────────┬───────────────────┐
    │  LOGO   │  Nombre Emisor       │  Timbrado: XXXXX  │
    │         │  RUC: XXX-X          │  FACTURA ELECTR.  │
    │         │  Dirección           │  001-001-0000001  │
    │         │  Tel / Email         │  CDC: 44 dígitos  │
    └─────────┴──────────────────────┴───────────────────┘
    """
    y_start = pdf.get_y()
    page_width = pdf.w - config.margins.left - config.margins.right

    # Coluna 1: Logo (25% da largura)
    logo_w = page_width * 0.22
    if config.logo:
        pdf.image(config.logo, x=config.margins.left, y=y_start,
                  w=logo_w - 2, h=25)

    # Coluna 2: Dados emissor (45% da largura)
    emisor_x = config.margins.left + logo_w
    emisor_w = page_width * 0.45
    pdf.set_xy(emisor_x, y_start)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(emisor_w, 5, data["emisor"]["nombre"], ln=True)
    pdf.set_x(emisor_x)
    pdf.set_font("Helvetica", "", 8)
    ruc = f"RUC: {data['emisor']['ruc']}-{data['emisor']['dv_ruc']}"
    pdf.cell(emisor_w, 4, ruc, ln=True)
    # ... mais campos do emisor

    # Coluna 3: Timbrado e Número (30% da largura)
    tim_x = emisor_x + emisor_w
    tim_w = page_width * 0.33
    pdf.set_xy(tim_x, y_start)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(tim_w, 4, f"Timbrado: {data['emisor']['timbrado']}", ln=True, align="C")
    # ... tipo documento, número, CDC

    # Borda do cabeçalho
    header_h = pdf.get_y() - y_start + 2
    pdf.rect(config.margins.left, y_start, page_width, header_h)


def draw_receptor(pdf: FPDF, data: dict, config):
    """Desenha a seção de dados do receptor."""
    # ...

def draw_operacion(pdf: FPDF, data: dict, config):
    """Desenha condição de operação (contado/crédito), moeda, etc."""
    # ...

def draw_items(pdf: FPDF, data: dict, config):
    """
    Desenha a tabela de itens com quebra de página automática.

    Cabeçalho: Cód | Descripción | Unid. | Cant. | P.Unit | % IVA | Subtotal
    """
    # Cabeçalho da tabela
    cols = [
        ("Cód", 15), ("Descripción", 65), ("Unid.", 15),
        ("Cant.", 18), ("P. Unit.", 25), ("IVA", 12), ("Subtotal", 25),
    ]
    pdf.set_font("Helvetica", "B", 7)
    for label, w in cols:
        pdf.cell(w, 5, label, border=1, align="C")
    pdf.ln()

    # Linhas de itens
    pdf.set_font("Helvetica", "", 7)
    for item in data["items"]:
        # Verificar quebra de página
        if pdf.get_y() + 5 > pdf.h - config.margins.bottom - 30:
            draw_page_footer(pdf, data, config)
            pdf.add_page()
            draw_items_header(pdf, cols)  # Re-desenhar cabeçalho

        pdf.cell(15, 5, item["codigo"], border=1)
        pdf.cell(65, 5, item["descripcion"][:40], border=1)
        pdf.cell(15, 5, item["unidad"], border=1, align="C")
        pdf.cell(18, 5, format_number(item["cantidad"]), border=1, align="R")
        pdf.cell(25, 5, format_guaranies(item["precio_unitario"]), border=1, align="R")
        pdf.cell(12, 5, f"{item['iva']}%", border=1, align="C")
        pdf.cell(25, 5, format_guaranies(item["subtotal"]), border=1, align="R")
        pdf.ln()


def draw_totales(pdf: FPDF, data: dict, config):
    """
    Desenha seção de totais: subtotais por faixa IVA + total geral.

    ┌──────────────────────────────────────────────────┐
    │ Subtotal IVA 10%: Gs. X.XXX │ Liq. IVA 10%: XXX │
    │ Subtotal IVA 5%:  Gs. X.XXX │ Liq. IVA 5%:  XXX │
    │ Subtotal Exento:  Gs. X.XXX │                    │
    │ TOTAL GENERAL: Gs. XX.XXX.XXX                    │
    │ (En letras: Guaraníes ...)                       │
    └──────────────────────────────────────────────────┘
    """
    # ...


def draw_qr_section(pdf: FPDF, data: dict, config):
    """
    Desenha QR Code + informações de consulta.

    ┌──────────┬────────────────────────────────────────┐
    │  ┌────┐  │ CDC: 01800695631001001000000312024...   │
    │  │ QR │  │ Fecha/Hora: 2024-11-29T17:59:57       │
    │  │    │  │ Consulte en: https://ekuatia.set...    │
    │  └────┘  │ Código de Seguridad: XXXXXXXXX         │
    └──────────┴────────────────────────────────────────┘
    """
    from ..qr import generate_qr_url, generate_qr_image
    from io import BytesIO

    qr_url = generate_qr_url(
        cdc=data["cdc"],
        dv=data["dv"],
        ambiente=config.ambiente,
    )
    qr_bytes = generate_qr_image(qr_url)

    # Desenhar QR
    qr_size = 25  # mm
    y_start = pdf.get_y() + 2
    pdf.image(BytesIO(qr_bytes), x=config.margins.left + 2,
              y=y_start, w=qr_size, h=qr_size)

    # Info ao lado do QR
    info_x = config.margins.left + qr_size + 5
    pdf.set_xy(info_x, y_start)
    pdf.set_font("Helvetica", "", 6)
    pdf.cell(0, 3, f"CDC: {data['cdc']}", ln=True)
    pdf.set_x(info_x)
    pdf.cell(0, 3, f"Fecha emisión: {data['fecha_emision']}", ln=True)
    pdf.set_x(info_x)
    pdf.cell(0, 3, f"Consulte en: {qr_url[:60]}...", ln=True)


def draw_info_adicional(pdf: FPDF, data: dict, config):
    """Desenha informações adicionais de interesse do emisor."""
    # ...
```

---

## 6. Formatação de Valores (Guaraníes)

```python
# utils.py

def format_guaranies(value, symbol="Gs.") -> str:
    """Formata valor em Guaraníes: Gs. 1.500.000"""
    try:
        num = int(float(value))
        formatted = f"{num:,}".replace(",", ".")
        return f"{symbol} {formatted}"
    except (ValueError, TypeError):
        return f"{symbol} 0"


def format_ruc(ruc: str, dv: str) -> str:
    """Formata RUC: 80069563-1"""
    return f"{ruc}-{dv}"


def format_documento(est: str, punto: str, num: str) -> str:
    """Formata número de documento: 001-001-0000001"""
    return f"{est.zfill(3)}-{punto.zfill(3)}-{num.zfill(7)}"


def number_to_words_es(number: int) -> str:
    """Converte número para extenso em espanhol."""
    # Implementar ou usar lib como num2words
    pass


TIPO_DOCUMENTO = {
    1: "Factura Electrónica",
    2: "Factura Electrónica de Exportación",
    3: "Factura Electrónica de Importación",
    4: "Autofactura Electrónica",
    5: "Nota de Crédito Electrónica",
    6: "Nota de Débito Electrónica",
    7: "Nota de Remisión Electrónica",
    8: "Comprobante de Retención Electrónico",
}
```

---

## 7. API de Uso Final

### Uso básico (idêntico ao BrazilFiscalReport)

```python
from paraguayfiscalreport.kude_fe import KudeFe

# Ler XML
with open("factura.xml", "r", encoding="utf-8") as f:
    xml_content = f.read()

# Gerar KuDE
kude = KudeFe(xml=xml_content)
kude.output("kude_factura.pdf")
```

### Uso com configuração

```python
from paraguayfiscalreport.kude_fe import KudeFe, KudeFeConfig, FontType, Margins

config = KudeFeConfig(
    logo="path/to/logo.png",
    margins=Margins(top=8, right=8, bottom=8, left=8),
    font_type=FontType.TIMES,
    csc="ABCD0000000000000000000000000000",
    csc_id="0001",
    ambiente=2,  # Test
    show_test_watermark=True,
)

kude = KudeFe(xml=xml_content, config=config)
kude.output("kude_factura.pdf")
```

### Todos os tipos de KuDE

```python
from paraguayfiscalreport.kude_fe import KudeFe
from paraguayfiscalreport.kude_nce import KudeNce
from paraguayfiscalreport.kude_nde import KudeNde
from paraguayfiscalreport.kude_afe import KudeAfe
from paraguayfiscalreport.kude_nre import KudeNre
from paraguayfiscalreport.kude_cre import KudeCre
from paraguayfiscalreport.kude_ticket import KudeTicket  # formato cinta 80mm

# Cada um segue o mesmo padrão:
kude = KudeXxx(xml=xml_string, config=config)
kude.output("arquivo.pdf")
```

### CLI

```bash
# Gerar KuDE de factura
pfr kude-fe factura.xml -o kude.pdf

# Gerar KuDE de nota de crédito
pfr kude-nce nota_credito.xml -o kude_nc.pdf

# Gerar em formato ticket
pfr kude-fe factura.xml --format ticket -o ticket.pdf

# Com logo e configuração
pfr kude-fe factura.xml --logo logo.png --config config.yaml
```

### Integração com sifenlib

```python
from sifenlib.de.bindings.v150.si_recep_de_v150 import Rde
from paraguayfiscalreport.kude_fe import KudeFe

# Ler DE com sifenlib
rde = Rde.from_path("factura.xml")

# Gerar KuDE a partir do XML
xml = rde.to_xml()
kude = KudeFe(xml=xml)
kude.output("kude.pdf")

# Ou se sifenlib tiver integração to_pdf():
# pdf_bytes = rde.to_pdf()  # usando paraguayfiscalreport como engine
```

---

## 8. Plano de Execução em Sprints

### Sprint 0 — Setup e Infraestrutura (1-2 dias)

- [ ] Criar repositório GitHub `paraguayfiscalreport`
- [ ] Configurar `pyproject.toml` com extras: `[qrcode]`, `[cli]`, `[all]`
- [ ] Criar estrutura de diretórios
- [ ] Instalar dependências: `fpdf2`, `lxml`, `python-barcode`, `qrcode`
- [ ] Configurar pre-commit, ruff, pytest

**Verificação:** `pip install -e .[all]` funciona.

---

### Sprint 1 — Utilitários e Parsing XML (2-3 dias)

- [ ] Implementar `xml_helpers.py` com extração de dados do DE
- [ ] Implementar `utils.py` com formatação de Guaraníes, RUC, etc.
- [ ] Implementar `cdc.py` com geração e validação do CDC
- [ ] Implementar `qr.py` com geração da URL do QR conforme MT 13.7.2
- [ ] Testes unitários para cada módulo

**Verificação:** Todos os testes em `test_utils.py`, `test_cdc.py`, `test_qr.py` passam.

---

### Sprint 2 — KuDE Factura Electrónica — Formato Carta (5-7 dias)

**Este é o sprint mais extenso e crítico.**

- [ ] Implementar `KudeFeConfig` (config.py)
- [ ] Implementar `KudeFe(FPDF)` (kude_fe.py)
- [ ] Implementar seções de desenho (sections.py):
  - [ ] `draw_header` — Logo + Emissor + Timbrado/Número
  - [ ] `draw_receptor` — Dados do receptor
  - [ ] `draw_operacion` — Condição (contado/crédito), moeda
  - [ ] `draw_items` — Tabela de itens com quebra de página
  - [ ] `draw_totales` — Subtotais IVA + Total geral
  - [ ] `draw_qr_section` — QR Code + CDC + info consulta
  - [ ] `draw_info_adicional` — Observações
- [ ] Tratar marca d'água "SIN VALIDEZ TRIBUTARIA" em ambiente test
- [ ] Testar com múltiplos XMLs de exemplo
- [ ] Comparação visual do PDF gerado vs. modelos do Manual Técnico

**Verificação:** `KudeFe(xml=xml).output("test.pdf")` gera PDF legível e completo.

---

### Sprint 3 — KuDE NCE e NDE (3-4 dias)

- [ ] Implementar `KudeNce` (Nota de Crédito)
- [ ] Implementar `KudeNde` (Nota de Débito)
- [ ] Seção extra: referência ao documento original (FE associada)
- [ ] Testes com XMLs de exemplo

**Nota:** NCE e NDE compartilham ~80% do layout com FE. Refatorar seções comuns para um módulo `common_sections.py`.

---

### Sprint 4 — KuDE AFE, NRE, CRE (4-5 dias)

- [ ] Implementar `KudeAfe` (Autofactura)
- [ ] Implementar `KudeNre` (Nota de Remisión) — layout diferente, inclui dados de transporte
- [ ] Implementar `KudeCre` (Comprobante de Retención) — layout diferente, sem itens
- [ ] Testes para cada tipo

---

### Sprint 5 — KuDE Formato Ticket / Cinta 80mm (3-4 dias)

- [ ] Implementar `KudeTicket` — formato compacto para impressoras térmicas
- [ ] Papel: 80mm largura, comprimento variável
- [ ] Layout vertical compacto com todas as informações obrigatórias
- [ ] QR Code menor (mas legível)
- [ ] Testar com diferentes quantidades de itens

---

### Sprint 6 — CLI e Demo Online (2-3 dias)

- [ ] Implementar CLI com `click` (idêntico ao `bfrep` do BrazilFiscalReport)
- [ ] Suporte a config via YAML
- [ ] Implementar app Streamlit para demo online ("Try it Online")
- [ ] Documentação com mkdocs

---

### Sprint 7 — Testes Visuais, CI/CD e Publicação (2-3 dias)

- [ ] Testes de comparação visual (gerar PDF → converter para imagem → diff)
- [ ] GitHub Actions para CI (testes + lint)
- [ ] Publicar no PyPI: `pip install paraguayfiscalreport`
- [ ] Criar release v0.1.0

---

### Sprint 8 — Integração com sifenlib (1-2 dias)

- [ ] Implementar método `to_pdf()` no `CommonMixin` da sifenlib
- [ ] Engine padrão: `paraguayfiscalreport`
- [ ] Auto-detectar tipo de DE para escolher KuDE correto

```python
# No CommonMixin da sifenlib:
def to_pdf(self, config=None, engine="paraguayfiscalreport"):
    """Gera o KuDE em PDF a partir do objeto."""
    from paraguayfiscalreport import auto_kude
    xml = self.to_xml()
    kude = auto_kude(xml, config=config)
    return kude.output()  # retorna bytes
```

---

## 9. Dependências

```toml
[project]
dependencies = [
    "fpdf2>=2.7.0",
    "lxml",
    "python-barcode",
    "phonenumbers",
]

[project.optional-dependencies]
qrcode = ["qrcode[pil]"]
cli = ["click", "PyYAML"]
all = ["qrcode[pil]", "click", "PyYAML"]
test = [
    "pytest",
    "pytest-cov",
    "Pillow",        # para comparação visual
    "pdf2image",     # para converter PDF→imagem nos testes
]
```

---

## 10. Estimativa de Esforço

| Sprint | Descrição | Esforço |
|--------|-----------|---------|
| 0 | Setup e infraestrutura | 1-2 dias |
| 1 | Utilitários e parsing XML | 2-3 dias |
| 2 | **KuDE Factura Electrónica (core)** | **5-7 dias** |
| 3 | KuDE NCE + NDE | 3-4 dias |
| 4 | KuDE AFE + NRE + CRE | 4-5 dias |
| 5 | KuDE Formato Ticket 80mm | 3-4 dias |
| 6 | CLI + Demo Streamlit | 2-3 dias |
| 7 | Testes visuais + CI/CD + PyPI | 2-3 dias |
| 8 | Integração com sifenlib | 1-2 dias |
| **Total** | | **~23-33 dias úteis** |

### Recomendação de prioridade

O **MVP mínimo** são os Sprints 0-2 (~8-12 dias): com o KuDE de Factura Electrónica funcionando, a biblioteca já tem valor real. O Sprint 2 é onde está o trabalho mais pesado de desenho com fpdf2 — é o coração do projeto. Os demais tipos de KuDE reutilizam grande parte do código.

---

## 11. Referências

| Recurso | URL |
|---------|-----|
| Manual Técnico SIFEN v150 (PDF) | https://www.dnit.gov.py/documents/20123/420592/Manual+T%C3%A9cnico+Versi%C3%B3n+150.pdf |
| Portal e-Kuatia | https://ekuatia.set.gov.py |
| XSD oficiais SIFEN | https://ekuatia.set.gov.py/sifen/xsd/ |
| BrazilFiscalReport (referência) | https://github.com/Engenere/BrazilFiscalReport |
| fpdf2 (lib PDF) | https://py-pdf.github.io/fpdf2/ |
| jsifenlib (Java, ref.) | https://github.com/roshkadev/rshk-jsifenlib |
| FacturaSend (API SIFEN) | https://docs.facturasend.com.py/ |
| Gráficas KuDE (MT v150, p.198+) | Seções 13.6 e 13.7 do Manual Técnico |
