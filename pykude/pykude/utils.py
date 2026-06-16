def format_guaranies(value, symbol="Gs."):
    """Format value in Guaranies: Gs. 1.500.000"""
    try:
        num = int(float(value))
        formatted = f"{num:,}".replace(",", ".")
        return f"{symbol} {formatted}"
    except (ValueError, TypeError):
        return f"{symbol} 0"


def format_number(value, decimals=0):
    """Format a number with dot separators."""
    try:
        num = float(value)
        if decimals == 0:
            return f"{int(num):,}".replace(",", ".")
        return f"{num:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return "0"


def format_ruc(ruc, dv):
    """Format RUC: 80069563-1"""
    return f"{ruc}-{dv}"


def format_documento(est, punto, num):
    """Format document number: 001-001-0000001"""
    return f"{str(est).zfill(3)}-{str(punto).zfill(3)}-{str(num).zfill(7)}"


def format_fecha(fecha_iso):
    """Format ISO date to display: 29/11/2024 17:59:57"""
    if not fecha_iso:
        return ""
    try:
        if "T" in fecha_iso:
            date_part, time_part = fecha_iso.split("T")
        else:
            date_part = fecha_iso
            time_part = ""

        parts = date_part.split("-")
        if len(parts) == 3:
            formatted = f"{parts[2]}/{parts[1]}/{parts[0]}"
            if time_part:
                formatted += f" {time_part}"
            return formatted
    except (ValueError, IndexError):
        pass
    return fecha_iso


def format_cdc(cdc):
    """Format CDC in groups of 4 digits for readability."""
    if not cdc:
        return ""
    return " ".join(cdc[i:i + 4] for i in range(0, len(cdc), 4))


TIPO_DOCUMENTO = {
    "1": "Factura electrónica",
    "2": "Factura electrónica de exportación",
    "3": "Factura electrónica de importación",
    "4": "Autofactura electrónica",
    "5": "Nota de crédito electrónica",
    "6": "Nota de débito electrónica",
    "7": "Nota de remisión electrónica",
    "8": "Comprobante de retención electrónico",
}

CONDICION_OPERACION = {
    "1": "Contado",
    "2": "Crédito",
}

TIPO_PAGO = {
    "1": "Efectivo",
    "2": "Cheque",
    "3": "Tarjeta de crédito",
    "4": "Tarjeta de débito",
    "5": "Transferencia",
    "6": "Giro",
    "7": "Billetera electrónica",
    "8": "Tarjeta empresarial",
    "9": "Vale",
    "10": "Retención",
    "11": "Pago por anticipo",
    "12": "Valor fiscal",
    "13": "Valor comercial",
    "99": "Otro",
}
