import extractores.conceptos_factura as KEY
import re
import modelo.ft_basicas as fb

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
    
    regex = r"91\s+(.*)"
    factura[KEY.EMPRESA] = fb.re_search(regex, pagina)

    regex = r"\n(.+)\n\d{6}\nN"
    factura[KEY.NIF] = fb.re_search(regex, pagina)
    factura[KEY.NIF] = re.sub(r"['. -]", "", factura[KEY.NIF])
    
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
