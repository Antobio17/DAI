import re

def ExpresionesRegulares(cadena):
    if ApellidoInicial(cadena):
        return f"La cadena {cadena} es un palabra seguida de un espacio y una única letra mayúscula."
    elif Email(cadena):
        return f"La cadena {cadena} es un email."
    elif TarjetaCredito(cadena):
        return f"La cadena {cadena} es una tarjeta de crédito."
    else:
        return f"No se ha identificado la cadena {cadena}"
    
def ApellidoInicial(cadena):
	a = re.compile(r'([A-Za-z]+) ([A-Z])')
	return a.match(cadena)

def Email(cadena):
	a = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b')
	return a.match(cadena)

def TarjetaCredito(cadena):
	a = re.compile(r'([0-9]{4}) ([0-9]{4}) ([0-9]{4}) ([0-9]{4})|([0-9]{4})-([0-9]{4})-([0-9]{4})-([0-9]{4})')
	return a.match(cadena)