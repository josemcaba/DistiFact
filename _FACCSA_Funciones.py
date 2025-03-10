import re
import ft_basicas as fb
import ft_verificadores as verificar

# El parámetro identificador es un texto que debe aparecer en la página
# del PDF para ser validada como factura.
# Las páginas que no contengan este texto son descartadas.

identificador="FACTURA"

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

    regex = r"FACTURA\s*(.+)"
    factura["Numero Factura"] = fb.re_search(regex, pagina)

    regex = r"FECHA\s*([\d.]+)"
    factura["Fecha Factura"] = fb.re_search(regex, pagina)
    factura["Fecha Operacion"] = factura["Fecha Factura"]
    
    factura["Concepto"] = 600

    regex = r"BASE\s*IMPONIB.\s*(.+)"
    factura["Base IVA"] = fb.re_search(regex, pagina)
    factura["Tipo IVA"] = 10
    regex = r"TOTAL\s*IVA\s*(.+)"
    factura["Cuota IVA"] = fb.re_search(regex, pagina)
    
    factura["Base IRPF"] = factura["Base IVA"]
    factura["Tipo IRPF"] = 0
    factura["Cuota IRPF"] = 0

    factura["Base R. Equiv."] = factura["Base IVA"]
    factura["Tipo R. Equiv."] = 1.4
    regex = r"TOTAL\s*R.E.\s*(.+)"
    factura["Cuota R. Equiv."] = fb.re_search(regex, pagina)

    factura["NIF"] = "A17001231"

    factura["Nombre"] = "FACCSA"

    regex = r"TOTAL\s*FACTURA.*?([\d]+\s*,\s*\d+)"
    factura["Total Factura"] = fb.re_search(regex, pagina)

    return(factura)     

def nif_cliente(pagina, empresa):
    '''
    De todos los NIF que aparezcan en la factura, devuelve el primero que sea
    distinto del NIF de la empresa.
    Los devuelve tal como están en la página de la factura
    '''
    regex = r"(?:NIF\s+|CIF\s+|CIF:\s+|TARJETA DE RESIDENCIA\s+)\b([a-zA-Z0-9](?:\s*)?\d{7}(?:\s*)?[a-zA-Z0-9])\b"
    match = re.findall(regex, pagina)
    # Filtrar para descartar el NIF de la empresa y seleccionar el correcto
    nif_cliente = [nif for nif in match if nif.replace(" ", "") != empresa["nif"]]
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

        # >>>>>>>>>> AJUSTES PERSONALIZADOS <<<<<<<<<< #
        if factura["Fecha Factura"]:
            factura["Fecha Factura"] = factura["Fecha Factura"].replace(".","/")
        error = verificar.fecha(factura)
        errores.append(error) if error else None

        conceptos = ["Base IVA", "Tipo IVA", "Cuota IVA",
                    "Base IRPF", "Tipo IRPF", "Cuota IRPF",
                    "Base R. Equiv.", "Tipo R. Equiv.", 
                    "Cuota R. Equiv.", "Total Factura"]
        for concepto in conceptos:
            error = verificar.importe(factura, concepto)
            if concepto == "Total Factura":
                observaciones.append(error) if error else None
            else:
                errores.append(error) if error else None
                
        error = verificar.nif(factura)
        errores.append(error) if error else None

        error = verificar.nombre(factura)
        errores.append(error) if error else None

        error = verificar.calculo_cuota_iva(factura)
        errores.append(error) if error else None

        error = verificar.calculo_cuota(factura, "R. Equiv.")
        errores.append(error) if error else None

        error = verificar.calculos_totales(factura)
        observaciones.append(error) if error else None

        if errores:
            factura["Errores"] = ", ".join(errores)
            facturas_con_errores.append(factura)
        else:
            factura["Observaciones"] = ", ".join(observaciones)
            facturas_correctas.append(factura)

    return facturas_correctas, facturas_con_errores