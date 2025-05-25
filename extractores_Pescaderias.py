import conceptos_factura as KEY
import re
import ft_basicas as fb

# El parámetro identificador es un texto que debe aparecer en la página
# del PDF para ser validada como factura.
# Las páginas que no contengan este texto son descartadas.

identificador = "Fecha emisión"

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

    regex = r"Nº factura\s*(.+)"
    factura[KEY.NUM_FACT] = fb.re_search(regex, pagina)

    regex = r"Fecha emisión\s*(.*)"
    factura[KEY.FECHA_FACT] = fb.re_search(regex, pagina)
    factura[KEY.FECHA_OPER] = factura[KEY.FECHA_FACT]
    
    factura[KEY.CONCEPTO] = 700
 
    regex = r"Base\s*([\d,\.]+)"
    factura[KEY.BASE_IVA] = fb.re_search(regex, pagina)

    factura[KEY.TIPO_IVA] = 10.0

    regex = r"IVA\s*([\d,\.]+)"
    factura[KEY.CUOTA_IVA] = fb.re_search(regex, pagina)

    factura[KEY.BASE_IRPF] = factura[KEY.BASE_IVA]
    factura[KEY.TIPO_IRPF] = 0.0
    factura[KEY.CUOTA_IRPF] = 0.0
    factura[KEY.BASE_RE] = factura[KEY.BASE_IVA]
    factura[KEY.TIPO_RE] = 0.0
    factura[KEY.CUOTA_RE] = 0.0

    nif_empresa = empresa["nif"][:8] + "-" + empresa["nif"][-1]
    regex = rf"{nif_empresa}\s*(.+)"
    factura[KEY.NIF] = fb.re_search(regex, pagina)
    factura[KEY.NIF] = re.sub(r"-", "", factura[KEY.NIF]) if factura[KEY.NIF] else None

    regex = rf"{empresa['nombre']}\s*(.+)"
    factura[KEY.EMPRESA] = fb.re_search(regex, pagina)
    if factura[KEY.EMPRESA] and len(factura[KEY.EMPRESA]) > 40:
        acorta_nombre_cliente(factura)

    regex = r"Total\s*([\d,\.]+)\s*€?"
    factura[KEY.TOTAL_FACT] = fb.re_search(regex, pagina)

    return([num_pag, factura]) 

def acorta_nombre_cliente(factura):
    nombre = factura[KEY.EMPRESA]
    if nombre[:20] == "Ramírez Sánchez S.L.":
        nombre = "Ramírez Sánchez S.L. 'Rest Refrectorium'"
    elif nombre[:21] == "Luis Gaspar Rodríguez":
        nombre = "Luis Gaspar Rodríguez 'Rest. El Rengue'"
    elif nombre[:8] == "La Magna":
        nombre = "La Magna. La oficina se sienta a la mesa"
    elif nombre[:19] == "Bar Mesón `El Tejón":
        nombre = "Bar Mesón 'El Tejón'"
    return nombre
