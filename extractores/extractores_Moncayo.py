import extractores.conceptos_factura as KEY
import re
import modelo.ft_basicas as fb

# El parámetro identificador es un texto que debe aparecer en la página
# del PDF para ser validada como factura.
# Las páginas que no contengan este texto son descartadas.

identificador="MONCAYO"

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
    print (pagina)
    factura = {}

    regex = r"(\d+).*\s"
    factura[KEY.NUM_FACT] = fb.re_search(regex, pagina)

    regex = r"Página.+\n+(.*)\b"
    linea = fb.re_search(regex, pagina)
    linea = re.sub(r" ", "", linea)
    regex = r"(.{1,2})[/I1](.{2})[/I1](.{4})"
    fecha = fb.re_search_multiple(regex, linea)
    if fecha and len(fecha) == 3:
        factura[KEY.FECHA_FACT] = fecha[0] + "/" + fecha[1] + "/" + fecha[2]
        factura[KEY.FECHA_FACT] = re.sub(r"o", "0", factura[KEY.FECHA_FACT])
        factura[KEY.FECHA_FACT] = re.sub(r"s", "5", factura[KEY.FECHA_FACT])
        factura[KEY.FECHA_FACT] = re.sub(r"S", "5", factura[KEY.FECHA_FACT])
        factura[KEY.FECHA_FACT] = re.sub(r"D", "0", factura[KEY.FECHA_FACT])
        factura[KEY.FECHA_FACT] = re.sub(r"E", "0", factura[KEY.FECHA_FACT])

    factura[KEY.CONCEPTO] = 700

    regex = r"(?m)^([\d A-Z]+)\s{3}\S+$"
    factura[KEY.NIF] = fb.re_search(regex, pagina)
    factura[KEY.NIF] = re.sub(r" ", "", factura[KEY.NIF]) if factura[KEY.NIF] else None

    regex = r"25042336M(?:\n\s*)*\n(?:.\n)?(.+)"
    factura[KEY.EMPRESA] = fb.re_search(regex, pagina)

    regex = r"(?m)^([\d,.]+)\s+([\d,.]+)\s+([\d,.]+)\s+\S+"
    importes = fb.re_search_multiple(regex, pagina)
    if importes and len(importes) == 3:
        factura[KEY.BASE_IVA] = importes[0]
        factura[KEY.TIPO_IVA] = importes[1]
        factura[KEY.CUOTA_IVA] = importes[2]    
        factura[KEY.BASE_IRPF] = factura[KEY.BASE_IVA]
        factura[KEY.TIPO_IRPF] = 0.0
        factura[KEY.CUOTA_IRPF] = 0.0
        factura[KEY.BASE_RE] = factura[KEY.BASE_IVA]
        factura[KEY.TIPO_RE] = 0.0
        factura[KEY.CUOTA_RE] = 0.0


    regex = r"([\d,.]+)\sEuros"
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
