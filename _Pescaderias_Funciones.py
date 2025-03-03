import re
import ft_comunes as ft
import ft_verificadores as verificar

def extraerFacturas(path, empresa):
    # Extrae facturas de PDF tipo texto
    paginas = ft.extraerPaginasPDF_tipoTexto(path, separador="Fecha emisión")

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

    regex = r"Nº factura\s*(\d+)"
    factura["Numero Factura"] = ft.re_search(regex, pagina)

    regex = r"Fecha emisión\s*(.*)"
    factura["Fecha Factura"] = ft.re_search(regex, pagina)
    factura["Fecha Operacion"] = factura["Fecha Factura"]
    
    factura["Concepto"] = 700
 
    regex = r"Base\s*([\d,\.]+)"
    factura["Base IVA"] = ft.re_search(regex, pagina)

    factura["Tipo IVA"] = 10.0

    regex = r"IVA\s*([\d,\.]+)"
    factura["Cuota IVA"] = ft.re_search(regex, pagina)

    factura["Base IRPF"] = factura["Base IVA"]
    factura["Tipo IRPF"] = 0
    factura["Cuota IRPF"] = 0
    factura["Base R. Equiv."] = factura["Base IVA"]
    factura["Tipo R. Equiv."] = 0
    factura["Cuota R. Equiv."] = 0

    nif_empresa = empresa["nif"][:8] + "-" + empresa["nif"][-1]
    regex = rf"{nif_empresa}\s*(.+)"
    factura["NIF"] = ft.re_search(regex, pagina)

    regex = rf"{empresa['nombre']}\s*(.+)"
    factura["Nombre Cliente"] = ft.re_search(regex, pagina)

    regex = r"Total\s*([\d,\.]+)\s*€?"
    factura["Total Factura"] = ft.re_search(regex, pagina)

    return(factura) 


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

        # >>>>>>>>>> AJUSTES PROVISIONALES <<<<<<<<<< #
        factura["Fecha Factura"] = re.sub(r"[-,]","", factura["Fecha Factura"])
        error = verificar.fecha(factura, is_eeuu=True)
        errores.append(error) if error else None

        error = verificar.base_iva(factura, decimal=',')
        errores.append(error) if error else None

        error = verificar.cuota_iva(factura, decimal=',')
        errores.append(error) if error else None
        
        error = verificar.total_factura(factura, decimal=',')
        errores.append(error) if error else None

        # >>>>>>>>>> AJUSTES PROVISIONALES <<<<<<<<<< #
        nif = re.sub(r"[^a-zA-Z0-9]","",factura["NIF"]).upper() if factura["NIF"] else None
        if nif == "X3581661W":
            nif = "X3586116W"
            observaciones.append("Corregido NIF erroneo que aparece en factura: X3581661W")
        factura["NIF"] = nif
        error = verificar.nif(factura)
        errores.append(error) if error else None
 
        # >>>>>>>>>> AJUSTES PROVISIONALES <<<<<<<<<< #
        if factura["Nombre Cliente"] and len(factura["Nombre Cliente"]) > 40:
            factura["Nombre Cliente"] = acorta_nombre_cliente(factura)
            observaciones.append("Acortado el nombre del cliente a un máximo de 40 caracteres")
        error = verificar.nombre_cliente(factura)
        errores.append(error) if error else None

        error = verificar.calculo_cuota_iva(factura)
        # >>>>>>>>>> AJUSTES PROVISIONALES <<<<<<<<<< #
        if error == "Cuota de IVA no calculable":
            errores.append(error) if error else None
        elif error:
            observacion = verificar.corrige_por_total(factura)
            observaciones.append(observacion)
        
        error = verificar.calculos_totales(factura)
        # >>>>>>>>>> AJUSTES PROVISIONALES <<<<<<<<<< #
        if error == "Total factura no calculable":
            errores.append(error) if error else None
        elif error:
            observacion = verificar.corrige_por_total(factura)
            observaciones.append(observacion)

        if errores:
            factura["Errores"] = ", ".join(errores)
            facturas_con_errores.append(factura)
        else:
            factura["Observaciones"] = ", ".join(observaciones)
            facturas_correctas.append(factura)

    return facturas_correctas, facturas_con_errores

def acorta_nombre_cliente(factura):
    nombre = factura["Nombre Cliente"]
    if nombre[:20] == "Ramírez Sánchez S.L.":
        nombre = "Ramírez Sánchez S.L. 'Rest Refrectorium'"
    elif nombre[:21] == "Luis Gaspar Rodríguez":
        nombre = "Luis Gaspar Rodríguez 'Rest. El Rengue'"
    return nombre


