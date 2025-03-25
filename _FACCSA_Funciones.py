import conceptos_factura as KEY
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
    num_pag = pagina[0]
    pagina = pagina[1]

    factura = {}

    regex = r"FACTURA\s*(.+)"
    factura[KEY.NUM_FACT] = fb.re_search(regex, pagina)

    regex = r"FECHA\s*([\d.]+)"
    factura[KEY.FECHA_FACT] = fb.re_search(regex, pagina)
    factura[KEY.FECHA_OPER] = factura[KEY.FECHA_FACT]
    
    factura[KEY.CONCEPTO] = 600

    regex = r"BASE\s*IMPONIB.\s*(.+)"
    factura[KEY.BASE_IVA] = fb.re_search(regex, pagina)
    factura[KEY.TIPO_IVA] = 10
    regex = r"TOTAL\s*IVA\s*(.+)"
    factura[KEY.CUOTA_IVA] = fb.re_search(regex, pagina)
    
    factura[KEY.BASE_IRPF] = factura[KEY.BASE_IVA]
    factura[KEY.TIPO_IRPF] = 0
    factura[KEY.CUOTA_IRPF] = 0

    factura[KEY.BASE_RE] = factura[KEY.BASE_IVA]
    factura[KEY.TIPO_RE] = 1.4
    regex = r"TOTAL\s*R.E.\s*(.+)"
    factura[KEY.CUOTA_RE] = fb.re_search(regex, pagina)

    factura[KEY.NIF] = "A17001231"

    factura[KEY.EMPRESA] = "FRIG. AND. CONSERVAS CARNES SA"

    regex = r"TOTAL\s*FACTURA.*?([\d]+\s*,\s*\d+)"
    factura[KEY.TOTAL_FACT] = fb.re_search(regex, pagina)

    return([num_pag, factura])     

# def nif_cliente(pagina, empresa):
#     '''
#     De todos los NIF que aparezcan en la factura, devuelve el primero que sea
#     distinto del NIF de la empresa.
#     Los devuelve tal como están en la página de la factura
#     '''
#     regex = r"(?:NIF\s+|CIF\s+|CIF:\s+|TARJETA DE RESIDENCIA\s+)\b([a-zA-Z0-9](?:\s*)?\d{7}(?:\s*)?[a-zA-Z0-9])\b"
#     match = re.findall(regex, pagina)
#     # Filtrar para descartar el NIF de la empresa y seleccionar el correcto
#     nif_cliente = [nif for nif in match if nif.replace(" ", "") != empresa["nif"]]
#     # Devuelve el primer NIF distinto o None
#     return nif_cliente[0] if nif_cliente else None

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
        if factura[KEY.FECHA_FACT]:
            factura[KEY.FECHA_FACT] = factura[KEY.FECHA_FACT].replace(".","/")
        error = verificar.fecha(factura)
        errores.append(error) if error else None

        conceptos = [KEY.BASE_IVA, KEY.TIPO_IVA, KEY.CUOTA_IVA,
                    KEY.BASE_IRPF, KEY.TIPO_IRPF, KEY.CUOTA_IRPF,
                    KEY.BASE_RE, KEY.TIPO_RE, 
                    KEY.CUOTA_RE, KEY.TOTAL_FACT]
        for concepto in conceptos:
            error = verificar.importe(factura, concepto)
            if concepto == KEY.TOTAL_FACT:
                observaciones.append(error) if error else None
            else:
                errores.append(error) if error else None
                
        error = verificar.nif(factura)
        errores.append(error) if error else None

        error = verificar.nombre(factura)
        errores.append(error) if error else None

        error = verificar.calculo_cuota(factura, KEY.CUOTA_IVA)
        errores.append(error) if error else None

        error = verificar.calculo_cuota(factura, KEY.CUOTA_RE)
        errores.append(error) if error else None

        error = verificar.calculos_totales(factura)
        observaciones.append(error) if error else None

        if errores:
            factura["Errores"] = f'<<Pag. {num_pag}>> ' + ", ".join(errores)
            facturas_con_errores.append(factura)
        else:
            if observaciones:
                factura["Observaciones"] = f'<<Pag. {num_pag}>> ' + ", ".join(observaciones)
            facturas_correctas.append(factura)

    return facturas_correctas, facturas_con_errores