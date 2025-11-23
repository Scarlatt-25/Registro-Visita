import re
from django.core.exceptions import ValidationError

def validar_rut(value):
    rut = value.upper().replace(".", "").replace("-", "")

    # Debe tener mínimo 2 caracteres (cuerpo + DV)
    if len(rut) < 2:
        raise ValidationError("RUT inválido.")

    cuerpo = rut[:-1]
    dv = rut[-1]

    # El cuerpo debe ser solo números
    if not cuerpo.isdigit():
        raise ValidationError("RUT inválido.")

    # El DV puede ser número o K
    if not re.match(r'^[0-9K]$', dv):
        raise ValidationError("RUT inválido.")

    # Algoritmo de cálculo
    suma = 0
    multiplo = 2

    for c in reversed(cuerpo):
        suma += int(c) * multiplo
        multiplo = multiplo + 1 if multiplo < 7 else 2

    resto = suma % 11
    dv_calculado = 11 - resto

    if dv_calculado == 11:
        dv_calculado = '0'
    elif dv_calculado == 10:
        dv_calculado = 'K'
    else:
        dv_calculado = str(dv_calculado)

    if dv != dv_calculado:
        raise ValidationError("RUT incorrecto.")
