import conceptos_factura as KEY
import re
import ft_basicas as fb
import ft_verificadores as verificar

# El parámetro identificador es un texto que debe aparecer en la página
# del PDF para ser validada como factura.
# Las páginas que no contengan este texto son descartadas.

identificador = "33.360.360-X"

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

    print(pagina)

    factura = {}

    factura[KEY.CONCEPTO] = 700
    
    regex = r"N.mero\s+(.*)\s+Fecha"
    factura[KEY.NUM_FACT] = fb.re_search(regex, pagina)

    regex = r"Fecha\s+(.*)"
    factura[KEY.FECHA_FACT] = fb.re_search(regex, pagina)
    factura[KEY.FECHA_OPER] = factura[KEY.FECHA_FACT]
    
    regex = r"91\s+(.*)\s+29003"
    factura[KEY.EMPRESA] = fb.re_search(regex, pagina)

    regex = r"info@servinfotec\.com 29004 MALAGA\s(.*)"
    factura[KEY.NIF] = fb.re_search(regex, pagina)
    factura[KEY.NIF] = re.sub(r"[.-]", "", factura[KEY.NIF])
    
    regex = r"TOTAL\n.+?\s(.+?)\s(.+?)\s(.+?)\s(.+?)\s(.+?)\s(.+?)\s"
    grupos = fb.re_search_multiple(regex, pagina)
    grupos_ok = grupos and (len(grupos) == 6)
    factura[KEY.BASE_IVA] = grupos[0] if grupos_ok else None
    factura[KEY.TIPO_IVA] = grupos[1] if grupos_ok else None
    factura[KEY.CUOTA_IVA] = grupos[2] if grupos_ok else None
    factura[KEY.BASE_RE] = factura[KEY.BASE_IVA]
    factura[KEY.TIPO_RE] = grupos[3] if grupos_ok else None
    factura[KEY.CUOTA_RE] = grupos[4] if grupos_ok else None
    factura[KEY.TOTAL_FACT] = grupos[5] if grupos_ok else None

    factura[KEY.BASE_IRPF] = factura[KEY.BASE_IVA]
    factura[KEY.TIPO_IRPF] = 0.0
    factura[KEY.CUOTA_IRPF] = 0.0

    return([num_pag, factura])     

def nif_cliente(pagina, empresa):
    '''
    De todos los NIF que aparezcan en la factura, devuelve el primero que sea
    distinto del NIF de la empresa.
    Los devuelve tal como están en la página de la factura
    '''
    regex = r"\b([a-zA-Z0-9]\d{7}[a-zA-Z0-9])\b"
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
        num_pag = factura[0]
        factura = factura[1]

        errores = []
        observaciones = []

        error = verificar.num_factura(factura)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.fecha(factura)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

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

        error = verificar.nif(factura)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.nombre(factura)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.calculo_cuota(factura, KEY.CUOTA_IVA)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.calculo_cuota(factura, KEY.CUOTA_RE)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.calculo_cuota(factura, KEY.CUOTA_IRPF)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.calculos_totales(factura)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        if errores:
            factura["Errores"] = ", ".join(errores)
            facturas_con_errores.append(factura)
        else:
            factura["Observaciones"] = ", ".join(observaciones)
            facturas_correctas.append(factura)

    return facturas_correctas, facturas_con_errores