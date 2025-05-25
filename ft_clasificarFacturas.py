import conceptos_factura as KEY
import ft_verificadores as verificar

def clasificarFacturas(facturas):
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

        error = verificar.nif(factura)
        errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        error = verificar.nombre(factura)
        if error:
            if "demasiado largo" in error:
                observaciones.append(f'<<Pag. {num_pag}>> {error}')
            else:
                errores.append(f'<<Pag. {num_pag}>> {error}')

        conceptos = [KEY.BASE_IVA, KEY.TIPO_IVA, KEY.CUOTA_IVA,
                    KEY.BASE_IRPF, KEY.TIPO_IRPF, KEY.CUOTA_IRPF,
                    KEY.BASE_RE, KEY.TIPO_RE, KEY.CUOTA_RE, 
                    KEY.TOTAL_FACT]
        for concepto in conceptos:
            error = verificar.importe(factura, concepto)
            if concepto == KEY.TOTAL_FACT:
                observaciones.append(f'<<Pag. {num_pag}>> {error}') if error else None
            else:
                errores.append(f'<<Pag. {num_pag}>> {error}') if error else None

        conceptos = [KEY.CUOTA_IVA, KEY.CUOTA_IRPF, KEY.CUOTA_RE]
        for concepto in conceptos:
            error = verificar.calculo_cuota(factura, concepto)
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
