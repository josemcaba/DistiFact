import extractores.conceptos_factura as KEY

#########################################################################
#
# EXTRACCION TIPO EXCEL
#
# Se limita exclusivamente a extraer los datos tal como aparecen en las
# facturas. Sin ningún tipo de ajuste o manipulación. Eso se hace en la
# fase de verificación
#
identificador=""

def extraerDatosFactura(pagina, empresa):
    num_pag = pagina[0]
    columna = pagina[1]

    factura = {}
    
    factura[KEY.CONCEPTO]   = 700   # Ingresos

    factura[KEY.EMPRESA] = columna[KEY.B]
    factura[KEY.NIF]     = columna[KEY.E]

    factura[KEY.NUM_FACT]   = columna[KEY.A]    
    factura[KEY.FECHA_FACT] = columna[KEY.G] 
    factura[KEY.FECHA_OPER] = columna[KEY.G] 
    
    factura[KEY.BASE_IVA]  = columna[KEY.N]
    factura[KEY.TIPO_IVA]  = 21.0
    factura[KEY.CUOTA_IVA] = columna[KEY.O]

    factura[KEY.BASE_IRPF] = factura[KEY.BASE_IVA]
    factura[KEY.TIPO_IRPF] = 0.0
    factura[KEY.CUOTA_IRPF] = 0.0

    factura[KEY.BASE_RE] = factura[KEY.BASE_IVA]
    factura[KEY.TIPO_RE] = 0.0
    factura[KEY.CUOTA_RE] = 0.0
    
    factura[KEY.TOTAL_FACT] = columna[KEY.K]

    return([num_pag, factura])     
