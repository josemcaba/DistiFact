#
# Verificadores
#

import ft_comunes as ft

def num_factura(factura):
	if factura["Numero Factura"] is None:
		return ("Numero Factura no encontrado")
	return False # No hay errores

def fecha(factura, is_eeuu=False):
    if factura["Fecha Factura"] is None:
        return ("Fecha Factura no encontrada")

    fecha = factura["Fecha Factura"].replace(",","")
    fecha = ft.validar_fecha(fecha, is_eeuu)
    if not fecha:
        return ("Fecha Factura incorrecta")

    factura["Fecha Factura"] = fecha
    factura["Fecha Operacion"] = fecha
    return False # No hay errores

def base_iva(factura):
    if factura["Base IVA"] is None:
        return ("Base IVA no encontrada")

    base = ft.convertir_a_float(factura["Base IVA"])
    if base is None:
        return ("Base IVA incorrecta")
    
    factura["Base IVA"] = base
    factura["Base IRPF"] = base
    factura["Base R. Equiv."] = base
    return False # No hay errores

def tipo_iva(factura):
    if factura["Tipo IVA"] is None:
        return ("Tipo IVA no encontrada")

    tipo = ft.convertir_a_float(factura["Tipo IVA"])
    if tipo is None:
        return ("Tipo IVA incorrecta")
    
    factura["Tipo IVA"] = tipo
    return False # No hay errores

def cuota_iva(factura):
    if factura["Cuota IVA"] is None:
        return ("Cuota IVA no encontrada")

    cuota = ft.convertir_a_float(factura["Cuota IVA"])
    if cuota is None:
        factura["Cuota IVA"] = None
        return ("Cuota IVA incorrecta")
    
    factura["Cuota IVA"] = cuota
    return False # No hay errores

def total_factura(factura):
    if factura["Total Factura"] is None:
        return ("Total Factura no encontrada")

    total = ft.convertir_a_float(factura["Total Factura"])
    if total is None:
        return ("Total Factura incorrecto")
    
    factura["Total Factura"] = total
    return False # No hay errores

def nif(factura):
    if factura["NIF"] is None:
        return ("NIF no encontrado")

    if not ft.validar_nif(factura["NIF"]):
        return ("NIF incorrecto")
    return False # No hay errores

def nombre_cliente(factura):
    if factura["Nombre Cliente"] is None:
        return ("Nombre Cliente no encontrado")
    if len(factura["Nombre Cliente"]) > 40:
        return ("Nombre Cliente demasiado largo. Máximo 40 caracteres.")
    return False # No hay errores

def calculo_cuota_iva(factura):
    base = factura["Base IVA"]
    tipo = factura["Tipo IVA"]
    cuota = factura["Cuota IVA"]
    if not (isinstance(base, float) and \
            isinstance(tipo, float) and \
            isinstance(cuota, float)):
        return ("Tipo de IVA no calculable")
    cuota_calculada = round(base * tipo / 100, 2)
    if abs(cuota_calculada - cuota) >= 0.015:
        return (f"Diferencia en cuota IVA ({cuota_calculada} != {cuota})")
    return False # No hay errores

def calculos_totales(factura):
    base = factura["Base IVA"]
    cuota = factura["Cuota IVA"]
    total = factura["Total Factura"]
    if not (isinstance(base, float) and \
            isinstance(cuota, float) and \
            isinstance(total, float)):
        return "Total factura no verificable"

    total_calculado = round(base + cuota, 2)
    if abs(total_calculado - total) >= 0.015:
        return (f"Diferencia en total factura ({total_calculado} != {total})")
    return False # No hay errores
