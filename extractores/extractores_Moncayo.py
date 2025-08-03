import conceptos_factura as KEY
import re
import modelo.ft_basicas as fb

# El parámetro identificador es un texto que debe aparecer en la página
# del PDF para ser validada como factura.
# Las páginas que no contengan este texto son descartadas.

identificador="FRA. NÚMERO"

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

    regex = r"FRA.\s*NÚMERO:\s+(.+)"
    factura[KEY.NUM_FACT] = fb.re_search(regex, pagina)

    regex = r"FECHA\s*FACTURA:\s+(.+)"
    factura[KEY.FECHA_FACT] = fb.re_search(regex, pagina)
    factura[KEY.FECHA_OPER] = factura[KEY.FECHA_FACT]
    
    factura[KEY.CONCEPTO] = 700

    regex = r"BASE\s*IMPONIBLE\s+(.+)"
    factura[KEY.BASE_IVA] = fb.re_search(regex, pagina)
    
    regex = r"IVA\s+(.+)\s*%"
    factura[KEY.TIPO_IVA] = fb.re_search(regex, pagina)

    regex = rf"IVA\s+{factura[KEY.TIPO_IVA]}\s*%\s+(.+)"
    factura[KEY.CUOTA_IVA] = fb.re_search(regex, pagina)
    
    factura[KEY.BASE_IRPF] = factura[KEY.BASE_IVA]
    factura[KEY.TIPO_IRPF] = 0.0
    factura[KEY.CUOTA_IRPF] = 0.0
    factura[KEY.BASE_RE] = factura[KEY.BASE_IVA]
    factura[KEY.TIPO_RE] = 0.0
    factura[KEY.CUOTA_RE] = 0.0

    factura[KEY.NIF] = nif_cliente(pagina, empresa)
    factura[KEY.NIF] = re.sub(r" ", "", factura[KEY.NIF]) if factura[KEY.NIF] else None

    regex = r"FECHA\s*FACTURA:\s*.+\s*(?:Referencia\s*[^\n]+)?\n([^\n]+)"
    factura[KEY.EMPRESA] = fb.re_search(regex, pagina)

    regex = r"TOTAL\s+(.+)"
    factura[KEY.TOTAL_FACT] = fb.re_search(regex, pagina)

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
