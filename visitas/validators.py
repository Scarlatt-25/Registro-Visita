from django.core.exceptions import ValidationError

def validar_rut(valor):
    valor = valor.replace(".", "").replace("-", "").upper()

    if len(valor) < 8:
        raise ValidationError("El RUT es muy corto.")

    cuerpo = valor[:-1]
    dv = valor[-1]

    if not cuerpo.isdigit():
        raise ValidationError("El RUT debe tener solo números en el cuerpo.")

    suma = 0
    mul = 2

    for c in reversed(cuerpo):
        suma += int(c) * mul
        mul = 9 if mul == 7 else mul + 1

    res = 11 - (suma % 11)

    if res == 11:
        digito = "0"
    elif res == 10:
        digito = "K"
    else:
        digito = str(res)

    if dv != digito:
        raise ValidationError("El RUT no es válido.")

    return valor   # ← ❗ ESTO FALTABA
