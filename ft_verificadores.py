import conceptos_factura as KEY
import ft_basicas as fb

def num_factura(factura):
	if factura[KEY.NUM_FACT] is None:
		return (f"Núm. {KEY.NUM_FACT} no encontrada")
	return False # No hay errores

def fecha(factura, is_eeuu=False):
    if factura[KEY.FECHA_FACT] is None:
        return (f"{KEY.FECHA_FACT} no encontrada")

    fecha = fb.validar_fecha(factura[KEY.FECHA_FACT], is_eeuu)
    if not fecha:
        return (f"{KEY.FECHA_FACT} incorrecta")

    factura[KEY.FECHA_FACT] = fecha
    factura[KEY.FECHA_OPER] = fecha
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
    if factura[KEY.BASE_IVA] is None:
        return (f"{KEY.BASE_IVA} no encontrada")

    base = fb.convertir_a_float(factura[KEY.BASE_IVA])
    if base is None:
        return (f"{KEY.BASE_IVA} incorrecta")
    
    factura[KEY.BASE_IVA] = base
    factura[KEY.BASE_IRPF] = base
    factura[KEY.BASE_RE] = base
    return False # No hay errores

def tipo_iva(factura, decimal=','):
    if factura[KEY.TIPO_IVA] is None:
        return (f"{KEY.TIPO_IVA} no encontrada")

    tipo = fb.convertir_a_float(factura[KEY.TIPO_IVA])
    if tipo is None:
        return (f"{KEY.TIPO_IVA} incorrecta")
    
    factura[KEY.TIPO_IVA] = tipo
    return False # No hay errores

def cuota_iva(factura, decimal=','):
    if factura[KEY.CUOTA_IVA] is None:
        return (f"{KEY.CUOTA_IVA} no encontrada")

    cuota = fb.convertir_a_float(factura[KEY.CUOTA_IVA])
    if cuota is None:
        factura[KEY.CUOTA_IVA] = None
        return (f"{KEY.CUOTA_IVA} incorrecta")
    
    factura[KEY.CUOTA_IVA] = cuota
    return False # No hay errores

def total_factura(factura, decimal=','):
    if factura[KEY.TOTAL_FACT] is None:
        return (f"{KEY.TOTAL_FACT} no encontrada")

    total = fb.convertir_a_float(factura[KEY.TOTAL_FACT])
    if total is None:
        return (f"{KEY.TOTAL_FACT} incorrecto")
    
    factura[KEY.TOTAL_FACT] = total
    return False # No hay errores

def nif(factura):
    if factura[KEY.NIF] is None:
        return (f"{KEY.NIF} no encontrado")

    if not fb.validar_nif(factura[KEY.NIF]):
        return (f"{KEY.NIF} incorrecto")
    return False # No hay errores

def nombre(factura):
    if factura[KEY.EMPRESA] is None:
        return (f"{KEY.EMPRESA} no encontrado")
    if len(factura[KEY.EMPRESA]) > 40:
        return (f"{KEY.EMPRESA} demasiado largo. Máximo 40 caracteres.")
    return False # No hay errores

def calculo_cuota(factura, concepto):
    if concepto == KEY.CUOTA_IVA:
        base = KEY.BASE_IVA
        tipo = KEY.TIPO_IVA
        cuota = KEY.CUOTA_IVA
    elif concepto == KEY.CUOTA_IRPF:
        base = KEY.BASE_IRPF
        tipo = KEY.TIPO_IRPF
        cuota = KEY.CUOTA_IRPF
    elif concepto == KEY.CUOTA_RE:
        base = KEY.BASE_RE
        tipo = KEY.TIPO_RE
        cuota = KEY.CUOTA_RE
    else:
        return (f'No se puede calcular la "{concepto}"')
    base = factura[base]
    tipo = factura[tipo]
    cuota = factura[cuota]
    if not (isinstance(base, float) and \
            isinstance(tipo, float) and \
            isinstance(cuota, float)):
        return (f"Cuota {concepto} no calculable")
    cuota_calculada = round(base * tipo / 100, 2)
    if abs(cuota_calculada - cuota) >= 0.015:
        return (f"{concepto}={cuota} != Calculado={cuota_calculada}")
    return False # No hay errores

def calculos_totales(factura):
    base = factura[KEY.BASE_IVA]
    cuota_iva = factura[KEY.CUOTA_IVA]
    cuota_irpf = factura[KEY.CUOTA_IRPF]
    cuota_re = factura[KEY.CUOTA_RE]
    total = factura[KEY.TOTAL_FACT]
    if not (isinstance(base, float) and \
            isinstance(cuota_iva, float) and \
           isinstance(cuota_irpf, float) and \
           isinstance(cuota_re, float) and \
            isinstance(total, float)):
        return "Total factura no calculable"
    total_calculado = round(base + cuota_iva + cuota_irpf + cuota_re, 2)
    if abs(total_calculado - total) >= 0.015:
        return (f"{KEY.TOTAL_FACT}={total} != Calculado={total_calculado}")
    return False # No hay errores

def corrige_por_total(factura):
    base = factura[KEY.BASE_IVA]
    tipo = factura[KEY.TIPO_IVA]
    cuota = factura[KEY.CUOTA_IVA]
    total = factura[KEY.TOTAL_FACT]
    if not (isinstance(total, float) and isinstance(tipo, float)):
        return "Correccion por Total no calculable"
    base_calculada = round(total / (1 + tipo / 100), 2)
    cuota_calculada = round(total - base_calculada, 2)
    factura[KEY.BASE_IVA] = base_calculada
    factura[KEY.CUOTA_IVA] = cuota_calculada
    factura[KEY.BASE_IRPF] = base_calculada
    factura[KEY.BASE_RE] = base_calculada
    return (f"Corregido: Base ({base}) y Cuota ({cuota})")

def corrige_por_base(factura):
    base = factura[KEY.BASE_IVA]
    tipo = factura[KEY.TIPO_IVA]
    cuota = factura[KEY.CUOTA_IVA]
    total = factura[KEY.TOTAL_FACT]
    cuota_calculada = round(base * tipo / 100, 2)
    total_calculado = round(base + cuota_calculada, 2)
    factura[KEY.CUOTA_IVA] = cuota_calculada
    factura[KEY.TOTAL_FACT] = total_calculado
    return (f"Corregido: Cuota ({cuota}) y Total ({total})") 
