import extractores.conceptos_factura as KEY
import re
import modelo.ft_basicas as ftb

# El parámetro identificador es un texto que debe aparecer en la página
# del PDF para ser validada como factura.
# Las páginas que no contengan este texto son descartadas.

identificador="TOTAL FACTURA"

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

    factura[KEY.CONCEPTO] = 600

    regex = r"([0-9][A-Z]/[0-9]{7})\s.*?\s([0-9]{2}/[0-9]{2}/[0-9]{4})"
    grupos = ftb.re_search_multiple(regex, pagina)
    grupos_ok = grupos and (len(grupos) == 2)
    factura[KEY.NUM_FACT] = grupos[0] if grupos_ok else None
    factura[KEY.FECHA_FACT] = grupos[1] if grupos_ok else None

    # regex = r"FACTURA.*\s([0-9][A-Z]/[0-9]{7})\s"
    # factura[KEY.NUM_FACT] = ftb.re_search(regex, pagina)

    # regex = r"FECHA.*\s([0-9]{2}/[0-9]{2}/[0-9]{4})\s"
    # factura[KEY.FECHA_FACT] = ftb.re_search(regex, pagina)

    regex = r"([\d]+[,.][\d]+)"
    grupos = re.findall(regex, pagina)
    grupos_ok = grupos and (len(grupos) >= 3)
    if grupos_ok:
        factura[KEY.BASE_IVA] = grupos[len(grupos)-3]
        factura[KEY.CUOTA_IVA] = grupos[len(grupos)-2]
        factura[KEY.TOTAL_FACT] = grupos[len(grupos)-1]

    factura[KEY.TIPO_IVA] = 21.0

    factura[KEY.BASE_IRPF] = factura[KEY.BASE_IVA]
    factura[KEY.TIPO_IRPF] = 0.0
    factura[KEY.CUOTA_IRPF] = 0.0

    factura[KEY.BASE_RE] = factura[KEY.BASE_IVA]
    factura[KEY.TIPO_RE] = 0.0
    factura[KEY.CUOTA_RE] = 0.0

    factura[KEY.NIF] = "B92421601"

    factura[KEY.EMPRESA] = "GOMEZ MORENO MIJAS S.L."

    return([num_pag, factura]) 
