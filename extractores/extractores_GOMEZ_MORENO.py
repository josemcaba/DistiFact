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

    factura = {}

    factura[KEY.CONCEPTO] = 600

    regex = r"([0-9][A-Z]/[0-9]{7})\s"
    factura[KEY.NUM_FACT] = ftb.re_search(regex, pagina)

    regex = r"([0-9]{2}/[0-9]{2}/20[0-9]{2})\s"
    factura[KEY.FECHA_FACT] = ftb.re_search(regex, pagina)

    # regex = r"FACTURA.*\s([0-9][A-Z]/[0-9]{7})\s"
    # factura[KEY.NUM_FACT] = ftb.re_search(regex, pagina)

    # regex = r"FECHA.*\s([0-9]{2}/[0-9]{2}/[0-9]{4})\s"
    # factura[KEY.FECHA_FACT] = ftb.re_search(regex, pagina)

    factura[KEY.BASE_IVA] = None

    regex = r"^([- —]*?(?:\d{2,}|\d+[,.]\d+))$"
    grupos = re.findall(regex, pagina, flags=re.MULTILINE)
    grupos_ok = grupos and (len(grupos) >= 3)
    if grupos_ok:
        factura[KEY.BASE_IVA]   = grupos[len(grupos)-3]
        factura[KEY.CUOTA_IVA]  = grupos[len(grupos)-2]
        factura[KEY.TOTAL_FACT] = grupos[len(grupos)-1]

        factura[KEY.BASE_IVA]   =  asegurar_decimal(re.sub(r"[ —]", "", factura[KEY.BASE_IVA]))
        factura[KEY.CUOTA_IVA]  =  asegurar_decimal(re.sub(r"[ —]", "", factura[KEY.CUOTA_IVA]))
        factura[KEY.TOTAL_FACT] =  asegurar_decimal(re.sub(r"[ —]", "", factura[KEY.TOTAL_FACT]))

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

def asegurar_decimal(cadena):
    # Si ya tiene punto o coma, no hacer nada
    if "." in cadena or "," in cadena:
        return cadena
    
    # Si no tiene separador, insertar coma en la tercera posición desde el final
    if len(cadena) >= 3:
        return cadena[:-2] + "," + cadena[-2:]
    else:
        # Por si la cadena es muy corta (ej: "5")
        return "0," + cadena.zfill(2)