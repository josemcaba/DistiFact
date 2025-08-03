import conceptos_factura as KEY
import re
import modelo.ft_basicas as ftb

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

    regex = r"FACTURA\s*FECHA\s*(.+?)\s+([0-9/]+)"
    grupos = ftb.re_search_multiple(regex, pagina)
    grupos_ok = grupos and (len(grupos) == 2)
    factura[KEY.NUM_FACT] = grupos[0] if grupos_ok else None
    factura[KEY.FECHA_FACT] = grupos[1] if grupos_ok else None
    
    factura[KEY.CONCEPTO] = 600

    regex = r"(?:IMPONIBLE|IMPORTE).+?([\d,.]+)\s*([\d]+)."
    grupos = ftb.re_search_multiple(regex, pagina)
    grupos_ok = grupos and (len(grupos) == 2)
    factura[KEY.BASE_IVA] = grupos[0] if grupos_ok else None
    factura[KEY.TIPO_IVA] = grupos[1] if grupos_ok else None

    regex = rf"{factura[KEY.BASE_IVA]}\s.+{factura[KEY.BASE_IVA]}.+?([\d,.]+)\s"
    factura[KEY.CUOTA_IVA] = ftb.re_search(regex, pagina)

    factura[KEY.BASE_IRPF] = factura[KEY.BASE_IVA]
    factura[KEY.TIPO_IRPF] = 0.0
    factura[KEY.CUOTA_IRPF] = 0.0

    factura[KEY.BASE_RE] = factura[KEY.BASE_IVA]
    factura[KEY.TIPO_RE] = 0.0
    factura[KEY.CUOTA_RE] = 0.0

    factura[KEY.NIF] = "B92421601"

    factura[KEY.EMPRESA] = "GOMEZ MORENO MIJAS S.L."

    regex = r"TOTAL\s*FACTURA.*?([\d,]+)\s"
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
