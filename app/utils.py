import datetime

def numero_a_texto(n):
    unidades = ["", "UNO", "DOS", "TRES", "CUATRO", "CINCO", "SEIS", "SIETE", "OCHO", "NUEVE"]
    decenas = ["", "DIEZ", "VEINTE", "TREINTA", "CUARENTA", "CINCUENTA", "SESENTA", "SETENTA", "OCHENTA", "NOVENTA"]
    especiales = ["ONCE", "DOCE", "TRECE", "CATORCE", "QUINCE", "DIECI", "VEINTI"]
    centenas = ["", "CIEN", "DOSCIENTOS", "TRESCIENTOS", "CUATROCIENTOS", "QUINIENTOS", "SEISCIENTOS", "SETECIENTOS", "OCHOCIENTOS", "NOVECIENTOS"]

    if n < 10:
        return unidades[n]
    elif n < 20:
        return especiales[n - 11] if n <= 15 else especiales[0] + unidades[n % 10].lower()
    elif n < 30:
        return especiales[6] + unidades[n % 10].lower() if n < 30 else decenas[n // 10] + (unidades[n % 10].lower() if n % 10 != 0 else "")
    elif n < 100:
        return decenas[n // 10] + (unidades[n % 10].lower() if n % 10 != 0 else "")
    elif n < 1000:
        return centenas[n // 100] + (" " + numero_a_texto(n % 100).lower() if n % 100 != 0 else "")
    else:
        miles = numero_a_texto(n // 1000) + " MIL"
        if n % 1000 == 0:
            return miles
        else:
            cientos = numero_a_texto(n % 1000)
            return f"{miles} {cientos.lower()}"

def convertir_fecha_a_texto(fecha):
    meses = ["", "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
    
    dia = fecha.day
    mes = fecha.month
    anio = fecha.year

    dia_texto = numero_a_texto(dia)
    mes_texto = meses[mes]
    anio_texto = numero_a_texto(anio)

    return f"{dia_texto} DÍAS DE {mes_texto} DEL AÑO {anio_texto.upper()}"


def numero_a_ordinal(n):
    ordinales = [
        "", "PRIMERO", "SEGUNDO", "TERCERO", "CUARTO", "QUINTO", "SEXTO", "SÉPTIMO", "OCTAVO", "NOVENO", "DÉCIMO",
        "UNDÉCIMO", "DUODÉCIMO", "DECIMOTERCERO", "DECIMOCUARTO", "DECIMOQUINTO", "DECIMOSEXTO", "DECIMOSÉPTIMO", "DECIMOOCTAVO", "DECIMONOVENO", "VIGÉSIMO",
        "VIGÉSIMO PRIMERO", "VIGÉSIMO SEGUNDO", "VIGÉSIMO TERCERO", "VIGÉSIMO CUARTO", "VIGÉSIMO QUINTO", "VIGÉSIMO SEXTO", "VIGÉSIMO SÉPTIMO", "VIGÉSIMO OCTAVO", "VIGÉSIMO NOVENO", "TRIGÉSIMO",
        "TRIGÉSIMO PRIMERO", "TRIGÉSIMO SEGUNDO", "TRIGÉSIMO TERCERO", "TRIGÉSIMO CUARTO", "TRIGÉSIMO QUINTO", "TRIGÉSIMO SEXTO", "TRIGÉSIMO SÉPTIMO", "TRIGÉSIMO OCTAVO", "TRIGÉSIMO NOVENO", "CUADRAGÉSIMO",
        "CUADRAGÉSIMO PRIMERO", "CUADRAGÉSIMO SEGUNDO", "CUADRAGÉSIMO TERCERO", "CUADRAGÉSIMO CUARTO", "CUADRAGÉSIMO QUINTO", "CUADRAGÉSIMO SEXTO", "CUADRAGÉSIMO SÉPTIMO", "CUADRAGÉSIMO OCTAVO", "CUADRAGÉSIMO NOVENO", "QUINCUAGÉSIMO"
    ]
    return ordinales[n]
