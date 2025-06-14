import conceptos_factura as KEY

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

    factura = {}

    factura[KEY.CONCEPTO] = 700

    factura[KEY.NUM_FACT] = pagina[1]
    factura[KEY.EMPRESA] = pagina[2]
    factura[KEY.NIF] = str(pagina[5]).upper()

    factura[KEY.FECHA_FACT] = pagina[7]
    factura[KEY.FECHA_OPER] = factura[KEY.FECHA_FACT]
    
    factura[KEY.BASE_IVA] = pagina[14]
    factura[KEY.TIPO_IVA] = 21.0
    factura[KEY.CUOTA_IVA] = pagina[15]
    
    factura[KEY.BASE_RE] = factura[KEY.BASE_IVA]
    factura[KEY.TIPO_RE] = 0.0
    factura[KEY.CUOTA_RE] = 0.0
    
    factura[KEY.BASE_IRPF] = factura[KEY.BASE_IVA]
    factura[KEY.TIPO_IRPF] = 0.0
    factura[KEY.CUOTA_IRPF] = 0.0

    factura[KEY.TOTAL_FACT] = pagina[11]

    return([num_pag, factura])     
