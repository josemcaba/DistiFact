#
# Verificadores
#

import ft_comunes as ft

def num_factura(factura):
	if factura["Num. Factura"] is None:
		return ("Num. Factura no encontrado")
	return False # No hay errores

def fecha(factura, is_eeuu=False):
    if factura["Fecha Fact."] is None:
        return ("Fecha no encontrada")

    fecha = factura["Fecha Fact."].replace(",","")
    fecha = ft.validar_fecha(fecha, is_eeuu)
    if not fecha:
        return ("Fecha incorrecta")

    factura["Fecha Fact."] = fecha
    factura["Fecha Oper."] = fecha
    return False # No hay errores

def base_iva(factura):
    if factura["Base I.V.A."] is None:
        return ("Base I.V.A. no encontrada")

    base = ft.convertir_a_float(factura["Base I.V.A."])
    if base is None:
        return ("Base I.V.A. incorrecta")
    
    factura["Base I.V.A."] = base
    factura["Base I.R.P.F."] = base
    factura["Base R. Equiv."] = base
    return False # No hay errores

def tipo_iva(factura):
    if factura["% I.V.A."] is None:
        return ("% I.V.A. no encontrada")

    tipo = ft.convertir_a_float(factura["% I.V.A."])
    if tipo is None:
        return ("% I.V.A. incorrecta")
    
    factura["% I.V.A."] = tipo
    return False # No hay errores

def cuota_iva(factura):
    if factura["Cuota I.V.A."] is None:
        return ("Cuota I.V.A. no encontrada")

    cuota = ft.convertir_a_float(factura["Cuota I.V.A."])
    if cuota is None:
        factura["Cuota I.V.A."] = None
        return ("Cuota I.V.A. incorrecta")
    
    factura["Cuota I.V.A."] = cuota
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
    if factura["NIF/DNI"] is None:
        return ("NIF/DNI no encontrado")

    if not ft.validar_nif(factura["NIF/DNI"]):
        return ("NIF/DNI incorrecto")
    return False # No hay errores

def nombre_cliente(factura):
    if factura["Nombre"] is None:
        return ("Nombre del cliente no encontrado")
    if len(factura["Nombre"]) > 40:
        return ("Nombre del cliente demasiado largo. Máximo 40 caracteres.")
    return False # No hay errores

def calculo_cuota_iva(factura):
    base = factura["Base I.V.A."]
    tipo = factura["% I.V.A."]
    cuota = factura["Cuota I.V.A."]
    if not (isinstance(base, float) and \
            isinstance(tipo, float) and \
            isinstance(cuota, float)):
        return ("Tipo de IVA no calculable")
    cuota_calculada = round(base * tipo / 100, 2)
    if abs(cuota_calculada - cuota) >= 0.015:
        return (f"Diferencia en cuota IVA ({cuota_calculada} != {cuota})")
    return False # No hay errores

def calculos_totales(factura):
    base = factura["Base I.V.A."]
    cuota = factura["Cuota I.V.A."]
    total = factura["Total Factura"]
    if not (isinstance(base, float) and \
            isinstance(cuota, float) and \
            isinstance(total, float)):
        return "Total factura no verificable"


    total_calculado = round(base + cuota, 2)
    if abs(total_calculado - total) >= 0.015:
        return (f"Diferencia en total factura ({total_calculado} != {total})")
    return False # No hay errores
