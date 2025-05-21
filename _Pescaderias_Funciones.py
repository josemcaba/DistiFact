import conceptos_factura as KEY
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
    num_pag = pagina[0]
    pagina = pagina[1]

    factura = {}

    regex = r"Nº factura\s*(.+)"
    factura[KEY.NUM_FACT] = fb.re_search(regex, pagina)

    regex = r"Fecha emisión\s*(.*)"
    factura[KEY.FECHA_FACT] = fb.re_search(regex, pagina)
    factura[KEY.FECHA_OPER] = factura[KEY.FECHA_FACT]
    
    factura[KEY.CONCEPTO] = 700
 
    regex = r"Base\s*([\d,\.]+)"
    factura[KEY.BASE_IVA] = fb.re_search(regex, pagina)

    factura[KEY.TIPO_IVA] = 10.0

    regex = r"IVA\s*([\d,\.]+)"
    factura[KEY.CUOTA_IVA] = fb.re_search(regex, pagina)

    factura[KEY.BASE_IRPF] = factura[KEY.BASE_IVA]
    factura[KEY.TIPO_IRPF] = 0.0
    factura[KEY.CUOTA_IRPF] = 0.0
    factura[KEY.BASE_RE] = factura[KEY.BASE_IVA]
    factura[KEY.TIPO_RE] = 0.0
    factura[KEY.CUOTA_RE] = 0.0

    nif_empresa = empresa["nif"][:8] + "-" + empresa["nif"][-1]
    regex = rf"{nif_empresa}\s*(.+)"
    factura[KEY.NIF] = fb.re_search(regex, pagina)

    regex = rf"{empresa['nombre']}\s*(.+)"
    factura[KEY.EMPRESA] = fb.re_search(regex, pagina)

    regex = r"Total\s*([\d,\.]+)\s*€?"
    factura[KEY.TOTAL_FACT] = fb.re_search(regex, pagina)

    return([num_pag, factura]) 


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
        num_pag = factura[0]
        factura = factura[1]

        errores = []
        observaciones = []

        error = verificar.num_factura(factura)
        errores.append(error) if error else None

        # >>>>>>>>>> AJUSTES PERSONALIZADOS <<<<<<<<<< #
        # factura[KEY.FECHA_FACT] = re.sub(r"[-,]","", factura[KEY.FECHA_FACT])
        error = verificar.fecha(factura, is_eeuu=True)
        errores.append(error) if error else None

        error = verificar.importe(factura, KEY.BASE_IVA)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.importe(factura, KEY.TIPO_IVA)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.importe(factura, KEY.CUOTA_IVA)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.importe(factura, KEY.BASE_RE)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.importe(factura, KEY.TIPO_RE)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.importe(factura, KEY.CUOTA_RE)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.importe(factura, KEY.BASE_IRPF)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.importe(factura, KEY.TIPO_IRPF)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.importe(factura, KEY.CUOTA_IRPF)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.importe(factura, KEY.TOTAL_FACT)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        # >>>>>>>>>> AJUSTES PROVISIONALES <<<<<<<<<< #
        # nif = re.sub(r"[^a-zA-Z0-9]","",factura[KEY.NIF]).upper() if factura[KEY.NIF] else None
        # if nif == "X3581661W":
        #     nif = "X3586116W"
        #     observaciones.append("Corregido NIF erroneo que aparece en factura: X3581661W")
        # factura[KEY.NIF] = nif
        error = verificar.nif(factura)
        errores.append(error) if error else None
 
        # >>>>>>>>>> AJUSTES PROVISIONALES <<<<<<<<<< #
        if factura[KEY.EMPRESA] and len(factura[KEY.EMPRESA]) > 40:
            factura[KEY.EMPRESA] = acorta_nombre_cliente(factura)
            observaciones.append("Acortado el nombre del nombre a un máximo de 40 caracteres")
        error = verificar.nombre(factura)
        errores.append(error) if error else None

        error = verificar.calculo_cuota(factura, KEY.CUOTA_IVA)
        # >>>>>>>>>> AJUSTES PROVISIONALES <<<<<<<<<< #
        if error == f"Cuota {KEY.BASE_IVA} no calculable":
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
            factura["Errores"] = f'<<Pag. {num_pag}>> ' + ", ".join(errores)
            facturas_con_errores.append(factura)
        else:
            if observaciones:
                factura["Observaciones"] = f'<<Pag. {num_pag}>> ' + ", ".join(observaciones)
            facturas_correctas.append(factura)

    return facturas_correctas, facturas_con_errores

def acorta_nombre_cliente(factura):
    nombre = factura[KEY.EMPRESA]
    if nombre[:20] == "Ramírez Sánchez S.L.":
        nombre = "Ramírez Sánchez S.L. 'Rest Refrectorium'"
    elif nombre[:21] == "Luis Gaspar Rodríguez":
        nombre = "Luis Gaspar Rodríguez 'Rest. El Rengue'"
    elif nombre[:8] == "La Magna":
        nombre = "La Magna. La oficina se sienta a la mesa"
    elif nombre[:19] == "Bar Mesón `El Tejón":
        nombre = "Bar Mesón 'El Tejón' - Enrique Gilabert"
    return nombre
