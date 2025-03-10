import re
import ft_basicas as fb
import ft_verificadores as verificar

# El parámetro identificador es un texto que debe aparecer en la página
# del PDF para ser validada como factura.
# Las páginas que no contengan este texto son descartadas.

identificador = "Fecha emisión"

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

    regex = r"Nº factura\s*(\d+)"
    factura["Numero Factura"] = fb.re_search(regex, pagina)

    regex = r"Fecha emisión\s*(.*)"
    factura["Fecha Factura"] = fb.re_search(regex, pagina)
    factura["Fecha Operacion"] = factura["Fecha Factura"]
    
    factura["Concepto"] = 700
 
    regex = r"Base\s*([\d,\.]+)"
    factura["Base IVA"] = fb.re_search(regex, pagina)

    factura["Tipo IVA"] = 10.0

    regex = r"IVA\s*([\d,\.]+)"
    factura["Cuota IVA"] = fb.re_search(regex, pagina)

    factura["Base IRPF"] = factura["Base IVA"]
    factura["Tipo IRPF"] = 0.0
    factura["Cuota IRPF"] = 0.0
    factura["Base R. Equiv."] = factura["Base IVA"]
    factura["Tipo R. Equiv."] = 0.0
    factura["Cuota R. Equiv."] = 0.0

    nif_empresa = empresa["nif"][:8] + "-" + empresa["nif"][-1]
    regex = rf"{nif_empresa}\s*(.+)"
    factura["NIF"] = fb.re_search(regex, pagina)

    regex = rf"{empresa['nombre']}\s*(.+)"
    factura["Nombre"] = fb.re_search(regex, pagina)

    regex = r"Total\s*([\d,\.]+)\s*€?"
    factura["Total Factura"] = fb.re_search(regex, pagina)

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

        # >>>>>>>>>> AJUSTES PERSONALIZADOS <<<<<<<<<< #
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
        if factura["Nombre"] and len(factura["Nombre"]) > 40:
            factura["Nombre"] = acorta_nombre_cliente(factura)
            observaciones.append("Acortado el nombre del nombre a un máximo de 40 caracteres")
        error = verificar.nombre(factura)
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
    nombre = factura["Nombre"]
    if nombre[:20] == "Ramírez Sánchez S.L.":
        nombre = "Ramírez Sánchez S.L. 'Rest Refrectorium'"
    elif nombre[:21] == "Luis Gaspar Rodríguez":
        nombre = "Luis Gaspar Rodríguez 'Rest. El Rengue'"
    return nombre
