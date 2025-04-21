import conceptos_factura as KEY
import re
import ft_basicas as fb
import ft_verificadores as verificar

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
    factura[KEY.NIF] = pagina[5]
    
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


#########################################################################
#
# VERIFICACION
#
def clasificar_facturas(facturas):
    """
    Clasifica las facturas en correctas y con errores.
    Retorna dos listas: facturas_correctas y facturas_con_errores.
    """
    facturas_correctas = []
    facturas_con_errores = []

    for factura in facturas:
        num_pag = factura[0]
        factura = factura[1]

        errores = []
        observaciones = []

        error = verificar.num_factura(factura)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.fecha(factura)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.importe(factura, KEY.BASE_IVA)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.importe(factura, KEY.TIPO_IVA)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.importe(factura, KEY.CUOTA_IVA)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.importe(factura, KEY.BASE_RE)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.importe(factura, KEY.TIPO_RE)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.importe(factura, KEY.CUOTA_RE)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.importe(factura, KEY.BASE_IRPF)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.importe(factura, KEY.TIPO_IRPF)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.importe(factura, KEY.CUOTA_IRPF)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.importe(factura, KEY.TOTAL_FACT)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        factura[KEY.NIF] = factura[KEY.NIF].upper() if factura[KEY.NIF] else None
        error = verificar.nif(factura)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.nombre(factura)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.calculo_cuota(factura, KEY.CUOTA_IVA)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.calculo_cuota(factura, KEY.CUOTA_RE)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.calculo_cuota(factura, KEY.CUOTA_IRPF)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.calculos_totales(factura)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        if errores:
            factura["Errores"] = ", ".join(errores)
            facturas_con_errores.append(factura)
        else:
            factura["Observaciones"] = ", ".join(observaciones)
            facturas_correctas.append(factura)

    return facturas_correctas, facturas_con_errores