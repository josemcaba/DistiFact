import conceptos_factura as KEY
import re
import ft_basicas as ftb
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

    factura[KEY.CONCEPTO] = 700     # Ingresos
    
    regex = r"FACTURA\s+(.*)"
    factura[KEY.EMPRESA] = ftb.re_search(regex, pagina)

    regex = r"(.*?)\s*\d{6}\n"
    factura[KEY.NIF] = ftb.re_search(regex, pagina)

    regex = r"mero(?:\s+\S+)?\s+(.{2}[/S58].{4})\n"
    factura[KEY.NUM_FACT] = ftb.re_search(regex, pagina)

    regex = r"Fecha\n+(.*)\n"
    factura[KEY.FECHA_FACT] = ftb.re_search(regex, pagina)

    regex = r"\n([-\d,.]+)\s+([\d,.]+)\s+([-\d,.]+)\n"
    grupos = ftb.re_search_multiple(regex, pagina)
    grupos_ok = grupos and (len(grupos) == 3)
    factura[KEY.BASE_IVA] = grupos[0] if grupos_ok else None
    factura[KEY.TIPO_IVA] = grupos[1] if grupos_ok else None
    factura[KEY.CUOTA_IVA] = grupos[2] if grupos_ok else None

    factura[KEY.BASE_IRPF] = factura[KEY.BASE_IVA]
    factura[KEY.TIPO_IRPF] = 0.0
    factura[KEY.CUOTA_IRPF] = 0.0
    factura[KEY.BASE_RE] = factura[KEY.BASE_IVA]
    factura[KEY.TIPO_RE] = 0.0
    factura[KEY.CUOTA_RE] = 0.0

    regex = r"\n([-\d,.]+)\s+Euro"
    factura[KEY.TOTAL_FACT] = ftb.re_search(regex, pagina)

    return([num_pag, factura]) 

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
        num_pag = factura[0]
        factura = factura[1]

        errores = []
        observaciones = []
        
        factura[KEY.NUM_FACT] = re.sub(r"^(.{2})([58])(.{4})$", r"\1S\3", factura[KEY.NUM_FACT]) if factura[KEY.NUM_FACT] else None
        error = verificar.num_factura(factura)
        errores.append(error) if error else None

        error = verificar.fecha(factura)
        errores.append(error) if error else None

        conceptos = [KEY.BASE_IVA, KEY.TIPO_IVA, KEY.CUOTA_IVA,
                    KEY.BASE_IRPF, KEY.TIPO_IRPF, KEY.CUOTA_IRPF,
                    KEY.BASE_RE, KEY.TIPO_RE, KEY.CUOTA_RE,
                    KEY.TOTAL_FACT]
        for concepto in conceptos:
            error = verificar.importe(factura, concepto)
            errores.append(error) if error else None

        factura[KEY.NIF] = re.sub(r"['-. ]", "", factura[KEY.NIF]) if factura[KEY.NIF] else None
        error = verificar.nif(factura)
        errores.append(error) if error else None

        error = verificar.nombre(factura)
        errores.append(error) if error else None

        error = verificar.calculo_cuota(factura, KEY.CUOTA_IVA)
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