import extractores.conceptos_factura as KEY
import re
import modelo.ft_basicas as fb

# El parámetro identificador es un texto que debe aparecer en la página
# del PDF para ser validada como factura.
# Las páginas que no contengan este texto son descartadas.

identificador = "FACTURA"

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

    factura[KEY.CONCEPTO] = 700

    # regex = r"Factura\n(\d+)"
    regex = r"Factura\s*(\d+)\n"
    factura[KEY.NUM_FACT] = fb.re_search(regex, pagina)

    regex = r"\n(\d{2}-\d{2}-\d{4})\n"
    factura[KEY.FECHA_FACT] = fb.re_search(regex, pagina)
    
    regex = r"Facturación Dirección\n(.+)"
    texto = fb.re_search(regex, pagina)                 # Selecciona la línea que contiene EMPRESA y NIF
    texto = texto[:-9] + texto[-9:].replace(" ", "")    # Elimina espacios en los últimos 9 caracteres
    regex = r"(\S+)$"                                   # Selecciona la última palabra que es el NIF
    factura[KEY.NIF] = fb.re_search(regex, texto)

    factura[KEY.EMPRESA] = " ".join(texto.split()[:-1]) # Selecciona todo salvo la ultima palabra que es el NIF
    factura[KEY.EMPRESA] = factura[KEY.EMPRESA].replace(" CIF:","").replace(" NIE","").replace(". cif","")

    regex = r"Total.+ (.+)\n"
    factura[KEY.BASE_IVA] = fb.re_search(regex, pagina)

    regex = r"Impuesto:\s+(.+)%"
    factura[KEY.TIPO_IVA] = fb.re_search(regex, pagina)

    regex = r"Impuesto:.+ (.+)\n"
    factura[KEY.CUOTA_IVA] = fb.re_search(regex, pagina)

    regex = r"Gran total.+ (.+)\n"
    factura[KEY.TOTAL_FACT] = fb.re_search(regex, pagina)

    factura[KEY.BASE_RE] = factura[KEY.BASE_IVA]
    factura[KEY.TIPO_RE] = 0.0
    factura[KEY.CUOTA_RE] = 0.0

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
    regex = r"([A-Z0-9]\d{7}[A-Z0-9])"
    match = re.findall(regex, pagina)
    # Filtrar para descartar el NIF de la empresa y seleccionar el correcto
    nif_cliente = [nif for nif in match if nif != empresa["nif"]]
    # Devuelve el primer NIF distinto o None
    return nif_cliente[0] if nif_cliente else None
