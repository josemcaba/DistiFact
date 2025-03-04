import re
import ft_comunes as ft
import ft_verificadores as verificar

def extraerFacturas(path, empresa):
    # Extrae facturas de PDF tipo texto indicando el texto que marca el 
    # inicio/separacion de cada factura
    paginas = ft.extraerPaginasPDF_tipoTexto(path, separador="25042336")

    facturas = []
    for pagina in paginas:
        factura = extraerDatosFactura(pagina, empresa)
        if factura:
            facturas.append(factura)
    return facturas

#########################################################################
#
# EXTRACCION
#
def extraerDatosFactura(pagina, empresa):
    factura = {}

    regex = r"FRA.\s*NÚMERO:\s+(.+)"
    factura["Numero Factura"] = ft.re_search(regex, pagina)

    regex = r"FECHA\s*FACTURA:\s+(.+)"
    factura["Fecha Factura"] = ft.re_search(regex, pagina)
    factura["Fecha Operacion"] = factura["Fecha Factura"]
    
    factura["Concepto"] = 700

    regex = r"BASE\s*IMPONIBLE\s+(.+)"
    factura["Base IVA"] = ft.re_search(regex, pagina)
    
    regex = r"IVA\s+(.+)\s+%"
    factura["Tipo IVA"] = ft.re_search(regex, pagina)

    regex = rf"IVA\s+{factura['Tipo IVA']}\s*%\s+(.+)"
    factura["Cuota IVA"] = ft.re_search(regex, pagina)
    
    factura["Base IRPF"] = factura["Base IVA"]
    factura["Tipo IRPF"] = 0
    factura["Cuota IRPF"] = 0
    factura["Base R. Equiv."] = factura["Base IVA"]
    factura["Tipo R. Equiv."] = 0
    factura["Cuota R. Equiv."] = 0

    regex = r"NIF\s+(.*)"
    factura["NIF"] = ft.re_search(regex, pagina)
    factura["NIF"] = factura["NIF"].replace(" ", "") if factura["NIF"] else None

    regex = r"FECHA\s*FACTURA:\s*.+\s*(?:\nReferencia\s*[^\n]+)?\n([^\n]+)"
    factura["Nombre Cliente"] = ft.re_search(regex, pagina)

    regex = r"TOTAL\s+(.+)"
    factura["Total Factura"] = ft.re_search(regex, pagina)

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

        error = verificar.nombre_cliente(factura)
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