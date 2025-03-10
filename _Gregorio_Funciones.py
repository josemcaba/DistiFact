import re
import ft_basicas as fb
import ft_verificadores as verificar

# El parámetro identificador es un texto que debe aparecer en la página
# del PDF para ser validada como factura.
# Las páginas que no contengan este texto son descartadas.

identificador = "Enlaza Soluciones"

#########################################################################
#
# EXTRACCION
#
# Se limita exclusivamente a extraer los datos tal como aparecen en las
# facturas. Sin ningún tipo de ajuste o manipulación. Eso se hace en la
# fase de verificación
#
def extraerDatosFactura(pagina, empresa):
    factura = {}

    regex = r"Número de Factura.*\s+(?:Fact-)?(\d+)"
    factura["Numero Factura"] = fb.re_search(regex, pagina)

    regex = r"Fecha de Facturación.*\s+([\d/]+)"
    factura["Fecha Factura"] = fb.re_search(regex, pagina)
    factura["Fecha Operacion"] = factura["Fecha Factura"]
    
    factura["Concepto"] = 700
    
    # regex = r"(?:Descuento\s*[-\d,]+\s*Total\s*|Subtotal\s*)([\d,]+)"
    regex = r"otal\s*([\d,.]+)\s+IVA"
    factura["Base IVA"] = fb.re_search(regex, pagina)
    
    regex = r"IVA\s+\((\d+)%\)"
    factura["Tipo IVA"] = fb.re_search(regex, pagina)

    regex = r"IVA\s+\(\d+%\)\s+([\d.,]+)"
    factura["Cuota IVA"] = fb.re_search(regex, pagina)

    factura["Base IRPF"] = factura["Base IVA"]
    factura["Tipo IRPF"] = 0.0
    factura["Cuota IRPF"] = 0.0
    factura["Base R. Equiv."] = factura["Base IVA"]
    factura["Tipo R. Equiv."] = 0.0
    factura["Cuota R. Equiv."] = 0.0

    factura["NIF"] = nif_cliente(pagina, empresa)

    regex = rf"(.*?)\s+Gregorio Aranda"
    factura["Nombre"] = fb.re_search(regex, pagina)

    regex = r"Envío\s+(?:[\d,]+\s+)?Total\s+([\d.,]+)"
    factura["Total Factura"] = fb.re_search(regex, pagina)

    return(factura)     

# De todos los NIF que aparezcan en la página devuelve el primero que sea
# distinto del NIF de la empresa
def nif_cliente(pagina, empresa):
    regex = r"\b([a-zA-Z0-9]\d{7}[a-zA-Z0-9])\b"
    match = re.findall(regex, pagina)
    # Filtrar para descartar el NIF de la empresa y seleccionar el correcto
    nif_cliente = [nif for nif in match if nif != empresa["nif"]]
    # Devuelve el primer NIF distinto o None
    return nif_cliente[0] if nif_cliente else None

#########################################################################
#
# VERIFICACION
#
def clasificar_facturas(facturas):
    """
    Clasifica las facturas en correctas y con errores.
    Retorna dos listas: facturas_correctas y facturas_con_errores.
    """
    facturas_correctas = []
    facturas_con_errores = []

    for factura in facturas:
        errores = []
        observaciones = []

        error = verificar.num_factura(factura)
        errores.append(error) if error else None

        error = verificar.fecha(factura)
        errores.append(error) if error else None

        error = verificar.base_iva(factura)
        errores.append(error) if error else None

        error = verificar.tipo_iva(factura)
        errores.append(error) if error else None

        error = verificar.cuota_iva(factura)
        errores.append(error) if error else None
        if factura["Cuota IVA"] == 0.0: 
            factura["Tipo IVA"] = 0.0
            observaciones.append("Factura sin IVA")
        
        error = verificar.total_factura(factura)
        errores.append(error) if error else None

        error = verificar.nif(factura)
        errores.append(error) if error else None

        error = verificar.nombre(factura)
        errores.append(error) if error else None

        error = verificar.calculo_cuota_iva(factura)
        errores.append(error) if error else None

        error = verificar.calculos_totales(factura)
        errores.append(error) if error else None

        if errores:
            factura["Errores"] = ", ".join(errores)
            facturas_con_errores.append(factura)
        else:
            factura["Observaciones"] = ", ".join(observaciones)
            facturas_correctas.append(factura)

    return facturas_correctas, facturas_con_errores