import extractores.conceptos_factura as KEY
import re
import modelo.ft_basicas as fb

# El parámetro identificador es un texto que debe aparecer en la página
# del PDF para ser validada como factura.
# Las páginas que no contengan este texto son descartadas.

identificador = "Datos Cliente"

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

    regex = r"Número de Factura.*\s+(?:Fact-)?(\d+)"
    factura[KEY.NUM_FACT] = fb.re_search(regex, pagina)

    regex = r"Fecha de Facturación.*\s+([\d/]+)"
    factura[KEY.FECHA_FACT] = fb.re_search(regex, pagina)
    factura[KEY.FECHA_OPER] = factura[KEY.FECHA_FACT]
    
    factura[KEY.CONCEPTO] = 700
    
    # regex = r"(?:Descuento\s*[-\d,]+\s*Total\s*|Subtotal\s*)([\d,]+)"
    regex = r"otal\s*([\d,.]+)\s+IVA"
    factura[KEY.BASE_IVA] = fb.re_search(regex, pagina)
    
    regex = r"IVA\s+\((\d+)%\)"
    factura[KEY.TIPO_IVA] = fb.re_search(regex, pagina)

    regex = r"IVA\s+\(\d+%\)\s+([\d.,]+)"
    factura[KEY.CUOTA_IVA] = fb.re_search(regex, pagina)

    factura[KEY.BASE_IRPF] = factura[KEY.BASE_IVA]
    factura[KEY.TIPO_IRPF] = 0.0
    factura[KEY.CUOTA_IRPF] = 0.0
    factura[KEY.BASE_RE] = factura[KEY.BASE_IVA]
    factura[KEY.TIPO_RE] = 0.0
    factura[KEY.CUOTA_RE] = 0.0

    factura[KEY.NIF] = nif_cliente(pagina, empresa)

    regex = rf"(.*?)\s+Gregorio Aranda"
    factura[KEY.EMPRESA] = fb.re_search(regex, pagina)

    regex = r"Envío\s+(?:[\d,]+\s+)?Total\s+([\d.,]+)"
    factura[KEY.TOTAL_FACT] = fb.re_search(regex, pagina)

    return([num_pag, factura])     

# De todos los NIF que aparezcan en la página devuelve el primero que sea
# distinto del NIF de la empresa
def nif_cliente(pagina, empresa):
    regex = r"\b([a-zA-Z0-9]\d{7}[a-zA-Z0-9])\b"
    match = re.findall(regex, pagina)
    # Filtrar para descartar el NIF de la empresa y seleccionar el correcto
    nif_cliente = [nif for nif in match if nif != empresa["nif"]]
    # Devuelve el primer NIF distinto o None
    return nif_cliente[0] if nif_cliente else None
