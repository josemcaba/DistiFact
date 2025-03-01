#
# Verificadores
#

import ft_comunes as ft

def num_factura(factura):
	if factura["Num. Factura"] is None:
		return ("Num. Factura no encontrado")
	return False # No hay errores

def fecha(factura):
    if factura["Fecha Fact."] is None:
        return ("Fecha no encontrada")

    fecha = factura["Fecha Fact."].replace(",","")
    fecha = ft.validar_fecha(fecha, is_eeuu=True)
    if not fecha:
        return ("Fecha incorrecta")

    factura["Fecha Fact."] = fecha
    factura["Fecha Oper."] = fecha
    return False # No hay errores

def iva(factura):
    if factura["Base I.V.A."] is None:
        return ("Base I.V.A. no encontrada")

    base = ft.convertir_a_float(factura["Base I.V.A."])
    if base is None:
        return ("Base I.V.A. incorrecta")
    
    factura["Base I.V.A."] = base
    factura["Base I.R.P.F."] = base
    factura["Base R. Equiv."] = base
    return False # No hay errores