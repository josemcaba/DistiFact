import conceptos_factura as KEY
import re
import ft_basicas as fb
import ft_verificadores as verificar

# El parámetro identificador es un texto que debe aparecer en la página
# del PDF para ser validada como factura.
# Las páginas que no contengan este texto son descartadas.

identificador = "Enlaza Soluciones"

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

        if factura[KEY.NIF] == 'B82382155':
            factura[KEY.NIF] = 'B82832155'
            observaciones.append(f'<<Pag. {num_pag}>> NIF incorrecto ha sido corregido')
        error = verificar.nif(factura)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.nombre(factura)
        if error:
            if "demasiado largo" in error:
                observaciones.append(f'<<Pag. {num_pag}>> {error}')
            else:
                errores.append(f'<<Pag. {num_pag}>> {error}')

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