def calculate_dv_mod11(code):
    """Calculate check digit using modulo 11 as per SIFEN spec."""
    weights = [2, 3, 4, 5, 6, 7, 2, 3, 4, 5, 6, 7]
    total = 0
    for i, char in enumerate(reversed(code)):
        total += int(char) * weights[i % len(weights)]
    remainder = total % 11
    if remainder <= 1:
        return 0
    return 11 - remainder


def validate_cdc(cdc):
    """Validate a 44-digit CDC."""
    if not cdc or len(cdc) != 44:
        return False
    if not cdc.isdigit():
        return False
    code = cdc[:43]
    dv = int(cdc[43])
    return calculate_dv_mod11(code) == dv


def generate_cdc(
    tipo_doc,
    ruc_emisor,
    dv_emisor,
    establecimiento,
    punto_exp,
    numero_doc,
    tipo_contribuyente,
    fecha_emision,
    tipo_emision,
    codigo_seguridad,
):
    """
    Generate a 44-digit CDC as per Manual Técnico section 6.1.

    Format: TTRRRRRRRRDDEEEPPPNNNNNNNNCYYYYMMDDEEEEEEEEEDS
    """
    cdc_sin_dv = (
        f"{int(tipo_doc):02d}"
        f"{ruc_emisor:>08s}"
        f"{dv_emisor}"
        f"{establecimiento:>03s}"
        f"{punto_exp:>03s}"
        f"{numero_doc:>07s}"
        f"{tipo_contribuyente}"
        f"{fecha_emision}"
        f"{int(tipo_emision)}"
        f"{codigo_seguridad:>09s}"
    )

    dv = calculate_dv_mod11(cdc_sin_dv)
    return cdc_sin_dv + str(dv)
