from lxml import etree

NS = {"sifen": "http://ekuatia.set.gov.py/sifen/xsd"}


def parse_xml(xml_string):
    """Parse XML string, returning the root element."""
    if isinstance(xml_string, str):
        xml_string = xml_string.encode("utf-8")
    return etree.fromstring(xml_string)


def get_text(element, xpath, default="", ns=None):
    """Extract text from an XPath within the SIFEN namespace."""
    if ns is None:
        ns = NS
    node = element.find(xpath, ns)
    return node.text if node is not None and node.text else default


def get_all(element, xpath, ns=None):
    """Return all elements matching an XPath."""
    if ns is None:
        ns = NS
    return element.findall(xpath, ns)


def extract_de_data(root):
    """Extract structured data from the DE for KuDE generation."""
    de = root.find(".//sifen:DE", NS)
    if de is None:
        de = root

    data = {
        "cdc": de.get("Id", ""),
        "dv": get_text(de, "sifen:dDVId"),
        "fecha_firma": get_text(de, "sifen:dFecFirma"),
        # Operation
        "tipo_emision": get_text(de, "sifen:gOpeDE/sifen:iTipEmi"),
        "desc_tipo_emision": get_text(de, "sifen:gOpeDE/sifen:dDesTipEmi"),
        "codigo_seguridad": get_text(de, "sifen:gOpeDE/sifen:dCodSeg"),
        # Timbrado
        "tipo_de": get_text(de, "sifen:gTimb/sifen:iTiDE"),
        "desc_tipo_de": get_text(de, "sifen:gTimb/sifen:dDesTiDE"),
        "timbrado": get_text(de, "sifen:gTimb/sifen:dNumTim"),
        "establecimiento": get_text(de, "sifen:gTimb/sifen:dEst"),
        "punto_exp": get_text(de, "sifen:gTimb/sifen:dPunExp"),
        "num_doc": get_text(de, "sifen:gTimb/sifen:dNumDoc"),
        "fecha_ini_timbrado": get_text(de, "sifen:gTimb/sifen:dFeIniT"),
        "fecha_fin_timbrado": get_text(de, "sifen:gTimb/sifen:dFeFinT"),
        # General operation data
        "fecha_emision": get_text(
            de, "sifen:gDatGralOpe/sifen:dFeEmiDE"
        ),
        # Commercial operation
        "tipo_transaccion": get_text(
            de, "sifen:gDatGralOpe/sifen:gOpeCom/sifen:iTipTra"
        ),
        "desc_tipo_transaccion": get_text(
            de, "sifen:gDatGralOpe/sifen:gOpeCom/sifen:dDesTipTra"
        ),
        "tipo_impuesto": get_text(
            de, "sifen:gDatGralOpe/sifen:gOpeCom/sifen:iTImp"
        ),
        "moneda": get_text(
            de, "sifen:gDatGralOpe/sifen:gOpeCom/sifen:cMoneOpe"
        ),
        "desc_moneda": get_text(
            de, "sifen:gDatGralOpe/sifen:gOpeCom/sifen:dDesMoneOpe"
        ),
        # Emisor
        "emisor": _extract_emisor(de),
        # Receptor
        "receptor": _extract_receptor(de),
        # Condición de operación
        "condicion": _extract_condicion(de),
        # Items
        "items": _extract_items(de),
        # Totales
        "totales": _extract_totales(de),
        # Type-specific
        "cam_fe": _extract_cam_fe(de),
        "cam_ncde": _extract_cam_ncde(de),
        "cam_ae": _extract_cam_ae(de),
        "cam_nre": _extract_cam_nre(de),
        # Associated documents
        "doc_asociado": _extract_doc_asociado(de),
        # QR
        "qr_url": "",
    }

    # Extract QR from outside DE (gCamFuFD)
    qr_node = root.find(".//sifen:gCamFuFD/sifen:dCarQR", NS)
    if qr_node is not None and qr_node.text:
        data["qr_url"] = qr_node.text

    return data


def _extract_emisor(de):
    base = "sifen:gDatGralOpe/sifen:gEmis"
    act_eco_nodes = get_all(de, f"{base}/sifen:gActEco")
    actividades = []
    for node in act_eco_nodes:
        actividades.append({
            "codigo": get_text(node, "sifen:cActEco"),
            "descripcion": get_text(node, "sifen:dDesActEco"),
        })

    return {
        "ruc": get_text(de, f"{base}/sifen:dRucEm"),
        "dv_ruc": get_text(de, f"{base}/sifen:dDVEmi"),
        "tipo_contribuyente": get_text(de, f"{base}/sifen:iTipCont"),
        "nombre": get_text(de, f"{base}/sifen:dNomEmi"),
        "nombre_fantasia": get_text(de, f"{base}/sifen:dNomFanEmi"),
        "direccion": get_text(de, f"{base}/sifen:dDirEmi"),
        "num_casa": get_text(de, f"{base}/sifen:dNumCas"),
        "departamento": get_text(de, f"{base}/sifen:dDesDepEmi"),
        "distrito": get_text(de, f"{base}/sifen:dDesDisEmi"),
        "ciudad": get_text(de, f"{base}/sifen:dDesCiuEmi"),
        "telefono": get_text(de, f"{base}/sifen:dTelEmi"),
        "email": get_text(de, f"{base}/sifen:dEmailE"),
        "actividades": actividades,
    }


def _extract_receptor(de):
    base = "sifen:gDatGralOpe/sifen:gDatRec"
    return {
        "naturaleza": get_text(de, f"{base}/sifen:iNatRec"),
        "tipo_operacion": get_text(de, f"{base}/sifen:iTiOpe"),
        "pais": get_text(de, f"{base}/sifen:dDesPaisRe"),
        "tipo_contribuyente": get_text(de, f"{base}/sifen:iTiContRec"),
        "ruc": get_text(de, f"{base}/sifen:dRucRec"),
        "dv_ruc": get_text(de, f"{base}/sifen:dDVRec"),
        "nombre": get_text(de, f"{base}/sifen:dNomRec"),
        "direccion": get_text(de, f"{base}/sifen:dDirRec"),
        "telefono": get_text(de, f"{base}/sifen:dTelRec"),
        "email": get_text(de, f"{base}/sifen:dEmailRec"),
        "num_doc_id": get_text(de, f"{base}/sifen:dNumIDRec"),
    }


def _extract_condicion(de):
    base = "sifen:gDtipDE/sifen:gCamCond"
    cond = {
        "tipo": get_text(de, f"{base}/sifen:iCondOpe"),
        "descripcion": get_text(de, f"{base}/sifen:dDCondOpe"),
        "pagos": [],
    }
    pagos = get_all(de, f"{base}/sifen:gPaConEIni")
    for pago in pagos:
        cond["pagos"].append({
            "tipo": get_text(pago, "sifen:iTiPago"),
            "descripcion": get_text(pago, "sifen:dDesTiPag"),
            "monto": get_text(pago, "sifen:dMonTiPag"),
            "moneda": get_text(pago, "sifen:cMoneTiPag"),
        })
    return cond


def _extract_items(de):
    items = []
    for item_node in get_all(de, "sifen:gDtipDE/sifen:gCamItem"):
        item = {
            "codigo": get_text(item_node, "sifen:dCodInt"),
            "descripcion": get_text(item_node, "sifen:dDesProSer"),
            "unidad_medida": get_text(item_node, "sifen:cUniMed"),
            "desc_unidad": get_text(item_node, "sifen:dDesUniMed"),
            "cantidad": get_text(item_node, "sifen:dCantProSer"),
            "precio_unitario": get_text(
                item_node, "sifen:gValorItem/sifen:dPUniProSer"
            ),
            "descuento": get_text(
                item_node, "sifen:gValorItem/sifen:dDescItem"
            ),
            "total_item": get_text(
                item_node, "sifen:gValorItem/sifen:dTotOpeItem"
            ),
            "total_gs": get_text(
                item_node, "sifen:gValorItem/sifen:dTotOpeGs"
            ),
            "afec_iva": get_text(
                item_node, "sifen:gCamIVA/sifen:iAfecIVA"
            ),
            "desc_afec_iva": get_text(
                item_node, "sifen:gCamIVA/sifen:dDesAfecIVA"
            ),
            "prop_iva": get_text(
                item_node, "sifen:gCamIVA/sifen:dPropIVA"
            ),
            "tasa_iva": get_text(
                item_node, "sifen:gCamIVA/sifen:dTasaIVA"
            ),
            "base_grav_iva": get_text(
                item_node, "sifen:gCamIVA/sifen:dBasGravIVA"
            ),
            "liq_iva": get_text(
                item_node, "sifen:gCamIVA/sifen:dLiqIVAItem"
            ),
        }
        items.append(item)
    return items


def _extract_totales(de):
    base = "sifen:gTotSub"
    return {
        "sub_exento": get_text(de, f"{base}/sifen:dSubExe", "0"),
        "sub_exonerado": get_text(de, f"{base}/sifen:dSubExo", "0"),
        "sub_5": get_text(de, f"{base}/sifen:dSub5", "0"),
        "sub_10": get_text(de, f"{base}/sifen:dSub10", "0"),
        "total_operacion": get_text(de, f"{base}/sifen:dTotOpe", "0"),
        "total_descuento": get_text(de, f"{base}/sifen:dTotDesc", "0"),
        "anticipo": get_text(de, f"{base}/sifen:dAnticipo", "0"),
        "redondeo": get_text(de, f"{base}/sifen:dRedon", "0"),
        "total_general": get_text(de, f"{base}/sifen:dTotGralOpe", "0"),
        "iva_5": get_text(de, f"{base}/sifen:dIVA5", "0"),
        "iva_10": get_text(de, f"{base}/sifen:dIVA10", "0"),
        "base_grav_5": get_text(de, f"{base}/sifen:dBaseGrav5", "0"),
        "base_grav_10": get_text(de, f"{base}/sifen:dBaseGrav10", "0"),
        "total_base_grav": get_text(de, f"{base}/sifen:dTBasGraIVA", "0"),
        "total_iva": get_text(de, f"{base}/sifen:dTotIVA", "0"),
        "total_gs": get_text(de, f"{base}/sifen:dTotalGs", "0"),
    }


def _extract_cam_fe(de):
    base = "sifen:gDtipDE/sifen:gCamFE"
    node = de.find(base, NS)
    if node is None:
        return None
    return {
        "ind_presencia": get_text(node, "sifen:iIndPres"),
        "desc_ind_presencia": get_text(node, "sifen:dDesIndPres"),
    }


def _extract_cam_ncde(de):
    base = "sifen:gDtipDE/sifen:gCamNCDE"
    node = de.find(base, NS)
    if node is None:
        return None
    return {
        "motivo": get_text(node, "sifen:iMotEmi"),
        "desc_motivo": get_text(node, "sifen:dDesMotEmi"),
    }


def _extract_cam_ae(de):
    base = "sifen:gDtipDE/sifen:gCamAE"
    node = de.find(base, NS)
    if node is None:
        return None
    return {
        "tipo_consulta": get_text(node, "sifen:iTipCons"),
        "desc_tipo_consulta": get_text(node, "sifen:dDesTipCons"),
        "num_consulta": get_text(node, "sifen:dNumCons"),
        "num_control": get_text(node, "sifen:dNumControl"),
        "tipo_id_vendedor": get_text(node, "sifen:iTipIDVen"),
        "desc_tipo_id_vendedor": get_text(node, "sifen:dDTipIDVen"),
        "num_id_vendedor": get_text(node, "sifen:dNumIDVen"),
        "nombre_vendedor": get_text(node, "sifen:dNomVen"),
        "direccion_vendedor": get_text(node, "sifen:dDirVen"),
    }


def _extract_cam_nre(de):
    base = "sifen:gDtipDE/sifen:gCamNRE"
    node = de.find(base, NS)
    if node is None:
        return None
    return {
        "motivo": get_text(node, "sifen:iMotEmiNR"),
        "desc_motivo": get_text(node, "sifen:dDesMotEmiNR"),
        "responsable": get_text(node, "sifen:iRespEmiNR"),
    }


def _extract_doc_asociado(de):
    docs = []
    for node in get_all(de, "sifen:gCamDEAsoc"):
        docs.append({
            "tipo": get_text(node, "sifen:iTipDocAso"),
            "desc_tipo": get_text(node, "sifen:dDesTipDocAso"),
            "cdc_ref": get_text(node, "sifen:dCdCDERef"),
            "nro_timbrado": get_text(node, "sifen:dNTimDI"),
            "nro_doc": get_text(node, "sifen:dNumDocAso"),
        })
    return docs
