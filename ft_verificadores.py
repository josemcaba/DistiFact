import ft_basicas as fb

def num_factura(factura):
	if factura["Numero Factura"] is None:
		return ("Numero Factura no encontrado")
	return False # No hay errores

def fecha(factura, is_eeuu=False):
    if factura["Fecha Factura"] is None:
        return ("Fecha Factura no encontrada")

    fecha = fb.validar_fecha(factura["Fecha Factura"], is_eeuu)
    if not fecha:
        return ("Fecha Factura incorrecta")

    factura["Fecha Factura"] = fecha
    factura["Fecha Operacion"] = fecha
    return False # No hay errores

def importe(factura, concepto, decimal=','):
    if factura[concepto] is None:
        return (f"{concepto} no encontrado")

    tipo = fb.convertir_a_float(factura[concepto])
    if tipo is None:
        return (f"{concepto} incorrecto")
    
    factura[concepto] = tipo
    return False # No hay errores

def base_iva(factura, decimal=','):
    if factura["Base IVA"] is None:
        return ("Base IVA no encontrada")

    base = fb.convertir_a_float(factura["Base IVA"])
    if base is None:
        return ("Base IVA incorrecta")
    
    factura["Base IVA"] = base
    factura["Base IRPF"] = base
    factura["Base R. Equiv."] = base
    return False # No hay errores

def tipo_iva(factura, decimal=','):
    if factura["Tipo IVA"] is None:
        return ("Tipo IVA no encontrada")

    tipo = fb.convertir_a_float(factura["Tipo IVA"])
    if tipo is None:
        return ("Tipo IVA incorrecta")
    
    factura["Tipo IVA"] = tipo
    return False # No hay errores

def cuota_iva(factura, decimal=','):
    if factura["Cuota IVA"] is None:
        return ("Cuota IVA no encontrada")

    cuota = fb.convertir_a_float(factura["Cuota IVA"])
    if cuota is None:
        factura["Cuota IVA"] = None
        return ("Cuota IVA incorrecta")
    
    factura["Cuota IVA"] = cuota
    return False # No hay errores

def total_factura(factura, decimal=','):
    if factura["Total Factura"] is None:
        return ("Total Factura no encontrada")

    total = fb.convertir_a_float(factura["Total Factura"])
    if total is None:
        return ("Total Factura incorrecto")
    
    factura["Total Factura"] = total
    return False # No hay errores

def nif(factura):
    if factura["NIF"] is None:
        return ("NIF no encontrado")

    if not fb.validar_nif(factura["NIF"]):
        return ("NIF incorrecto")
    return False # No hay errores

def nombre(factura):
    if factura["Nombre"] is None:
        return ("Nombre no encontrado")
    if len(factura["Nombre"]) > 40:
        return ("Nombre demasiado largo. Máximo 40 caracteres.")
    return False # No hay errores

def calculo_cuota_iva(factura):
    base = factura["Base IVA"]
    tipo = factura["Tipo IVA"]
    cuota = factura["Cuota IVA"]
    if not (isinstance(base, float) and \
            isinstance(tipo, float) and \
            isinstance(cuota, float)):
        return ("Cuota de IVA no calculable")
    cuota_calculada = round(base * tipo / 100, 2)
    if abs(cuota_calculada - cuota) >= 0.015:
        return (f"Diferencia en cuota IVA ({cuota_calculada} != {cuota})")
    return False # No hay errores

def calculo_cuota(factura, concepto):
    base = "Base " + concepto
    tipo = "Tipo " + concepto
    cuota = "Cuota " + concepto
    base = factura[base]
    tipo = factura[tipo]
    cuota = factura[cuota]
    if not (isinstance(base, float) and \
            isinstance(tipo, float) and \
            isinstance(cuota, float)):
        return (f"Cuota {concepto} no calculable")
    cuota_calculada = round(base * tipo / 100, 2)
    if abs(cuota_calculada - cuota) >= 0.015:
        return (f"Diferencia en {concepto} ({cuota_calculada} != {cuota})")
    return False # No hay errores

def calculos_totales(factura):
    base = factura["Base IVA"]
    cuota_iva = factura["Cuota IVA"]
    cuota_irpf = factura["Cuota IRPF"]
    cuota_re = factura["Cuota R. Equiv."]
    total = factura["Total Factura"]
    if not (isinstance(base, float) and \
            isinstance(cuota_iva, float) and \
           isinstance(cuota_irpf, float) and \
           isinstance(cuota_re, float) and \
            isinstance(total, float)):
        return "Total factura no calculable"
    total_calculado = round(base + cuota_iva + cuota_irpf + cuota_re, 2)
    if abs(total_calculado - total) >= 0.015:
        return (f"Diferencia en total factura ({total_calculado} != {total})")
    return False # No hay errores

def corrige_por_total(factura):
    base = factura["Base IVA"]
    tipo = factura["Tipo IVA"]
    cuota = factura["Cuota IVA"]
    total = factura["Total Factura"]
    base_calculada = round(total / (1 + tipo / 100), 2)
    cuota_calculada = round(total - base_calculada, 2)
    factura["Base IVA"] = base_calculada
    factura["Cuota IVA"] = cuota_calculada
    factura["Base IRPF"] = base_calculada
    factura["Base R. Equiv."] = base_calculada
    return (f"Corregido: Base ({base}) y Cuota ({cuota})")

def corrige_por_base(factura):
    base = factura["Base IVA"]
    tipo = factura["Tipo IVA"]
    cuota = factura["Cuota IVA"]
    total = factura["Total Factura"]
    cuota_calculada = round(base * tipo / 100, 2)
    total_calculado = round(base + cuota_calculada, 2)
    factura["Cuota IVA"] = cuota_calculada
    factura["Total Factura"] = total_calculado
    return (f"Corregido: Cuota ({cuota}) y Total ({total})") 
