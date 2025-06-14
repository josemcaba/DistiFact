import conceptos_factura as KEY
import re
import ft_basicas as ftb

# El parámetro identificador es un texto que debe aparecer en la página
# del PDF para ser validada como factura.
# Las páginas que no contengan este texto son descartadas.

identificador="factura"

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

    regex = r"factura\s*(.+)\s"
    factura[KEY.NUM_FACT] = ftb.re_search(regex, pagina)

    regex = r"(\d{2}\/\d{2}\/\d{4})"
    factura[KEY.FECHA_FACT] = ftb.re_search(regex, pagina)
    factura[KEY.FECHA_OPER] = factura[KEY.FECHA_FACT]

    factura[KEY.CONCEPTO] = 600

    regex = r"factura\s*.+\s*(.+)\s"
    factura[KEY.EMPRESA] = ftb.re_search(regex, pagina)

    factura[KEY.NIF] = nif_cliente(pagina, empresa)
    factura[KEY.NIF] = re.sub(r"O", "0", factura[KEY.NIF]) if factura[KEY.NIF] else None

    # regex = r"IVA\s*(\d+)\s*%"
    # factura[KEY.TIPO_IVA] = ftb.re_search(regex, pagina)
    factura[KEY.TIPO_IVA] = 21.0

    regex = r"Imponible\s*([\d,.]+\s*)"
    factura[KEY.BASE_IVA] = ftb.re_search(regex, pagina)

    regex = r"Total\s*IVA\s*([\d,.]+)\s*"
    factura[KEY.CUOTA_IVA] = ftb.re_search(regex, pagina)

    regex = r"TOTAL\s*([\d,.]+)\s*"
    factura[KEY.TOTAL_FACT] = ftb.re_search(regex, pagina)


    factura[KEY.TIPO_RE] = 0.0
    factura[KEY.CUOTA_RE] = 0.0
    
    factura[KEY.BASE_RE] = factura[KEY.BASE_IVA]
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
    regex = r"NIF\s([0-9A-Z]*)\s"
    match = re.findall(regex, pagina)
    # Filtrar para descartar el NIF de la empresa y seleccionar el correcto
    nif_cliente = [nif for nif in match if nif.replace(" ", "") != empresa["nif"]]
    # Devuelve el primer NIF distinto o None
    return nif_cliente[0] if nif_cliente else None
