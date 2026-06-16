__version__ = "0.1.0"


def __getattr__(name):
    if name == "KudeFe":
        from pykude.kude_fe import KudeFe
        return KudeFe
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def auto_kude(xml: str, config=None):
    """Auto-detect DE type and return the appropriate KuDE instance."""
    from pykude.xml_helpers import get_text, parse_xml

    root = parse_xml(xml)
    ns = {"sifen": "http://ekuatia.set.gov.py/sifen/xsd"}
    de = root.find(".//sifen:DE", ns)
    if de is None:
        de = root

    tipo = get_text(de, "sifen:gTimb/sifen:iTiDE", ns=ns)

    if tipo == "1":
        from pykude.kude_fe import KudeFe

        return KudeFe(xml=xml, config=config)
    elif tipo == "4":
        from pykude.kude_afe import KudeAfe

        return KudeAfe(xml=xml, config=config)
    elif tipo == "5":
        from pykude.kude_nce import KudeNce

        return KudeNce(xml=xml, config=config)
    elif tipo == "6":
        from pykude.kude_nde import KudeNde

        return KudeNde(xml=xml, config=config)
    elif tipo == "7":
        from pykude.kude_nre import KudeNre

        return KudeNre(xml=xml, config=config)
    elif tipo == "8":
        from pykude.kude_cre import KudeCre

        return KudeCre(xml=xml, config=config)
    else:
        raise ValueError(f"Unknown document type: {tipo}")
