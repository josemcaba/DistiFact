import extractores.conceptos_factura as KEY
import re
import modelo.ft_basicas as fb

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
    factura[KEY.FECHA_FACT] = re.sub(r"\.", "/", factura[KEY.FECHA_FACT]) if factura[KEY.FECHA_FACT] else None
    
    factura[KEY.CONCEPTO] = 600

    regex = r"BASE\s*IMPONIB.\s*(.+)"
    factura[KEY.BASE_IVA] = fb.re_search(regex, pagina)
    factura[KEY.TIPO_IVA] = 10.0
    regex = r"TOTAL\s*IVA\s*(.+)"
    factura[KEY.CUOTA_IVA] = fb.re_search(regex, pagina)
    
    factura[KEY.BASE_IRPF] = factura[KEY.BASE_IVA]
    factura[KEY.TIPO_IRPF] = 0.0
    factura[KEY.CUOTA_IRPF] = 0.0

    factura[KEY.BASE_RE] = factura[KEY.BASE_IVA]
    factura[KEY.TIPO_RE] = 1.4
    regex = r"TOTAL\s*R.E.\s*(.+)"
    factura[KEY.CUOTA_RE] = fb.re_search(regex, pagina)

    factura[KEY.NIF] = empresa["nif"]

    factura[KEY.EMPRESA] = empresa["nombre"]

    factura[KEY.TOTAL_FACT] = 0.0

    return([num_pag, factura])     
