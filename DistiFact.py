import ft_extraer_paginas as ft_texto
import ft_comunes as ft
from ft_cargarDatosEmpresa import cargarDatosEmpresa

def clasificar_facturas(facturas):
    """
    Clasifica las facturas en correctas y con errores.
    Retorna dos listas: facturas_correctas y facturas_con_errores.
    """
    facturas_correctas = []
    facturas_con_errores = []

    for factura in facturas:
        errores = []

        # Verificar Núm. Factura
        numfact = factura.get("Num. Factura", 0)
        if numfact == 0:
            errores.append("Num. Factura no encontrado")

        # Verificar fecha incorrecta y formatear si es correcta
        fecha_fact = factura.get("Fecha Fact.", 0)
        if fecha_fact != 0:
            fecha_valida = ft.validar_fecha(fecha_fact, is_eeuu=True)
            if fecha_valida:
                # Reemplazar el valor de la fecha por el formato dd/mm/aaaa
                factura["Fecha Fact."] = fecha_valida
                factura["Fecha Oper."] = fecha_valida
            else:
                errores.append("Fecha incorrecta")

        # Verificar % I.V.A.
        if factura.get("% I.V.A.", 0) != 10:
            errores.append("% I.V.A. es distinto de 10")
      
        # Verificar NIF
        nif = factura.get("NIF/DNI", 0)
        if nif == 0:
            errores.append("NIF no encontrado")
        elif nif == "NIF Inválido":
            errores.append("NIF inválido")

        # Verificar Nombre del cliente
        if factura.get("Nombre", 0) == 0:
            errores.append("Nombre del cliente no encontrado")
        elif len(factura.get("Nombre", 0)) > 40:
            errores.append("Nombre del cliente demasiado largo. Máximo 40 caracteres.")

        # Verificar diferencias en el total
        base_valor = factura.get("Base I.V.A.", 0)
        cuota_valor = factura.get("Cuota I.V.A.", 0)
        total_factura = factura.get("Total Factura", 0)
        importe_calculado = round(base_valor + cuota_valor, 2)
        if abs(importe_calculado - total_factura) > 0.01:
            errores.append(f"Diferencia en total factura ({importe_calculado} != {total_factura})")

        if errores:
            factura["Errores"] = ", ".join(errores)
            facturas_con_errores.append(factura)
        else:
            facturas_correctas.append(factura)

    return facturas_correctas, facturas_con_errores

def main():
    empresa, ruta_PDF = cargarDatosEmpresa("empresas.json")
    if not(empresa and ruta_PDF):
        print("\n👋 Saliendo del programa...\n")
        return

    if empresa:
        print("\nDatos completos de la empresa seleccionada:")
        for clave, valor in empresa.items():
            print(f"- {clave}: {valor}")
    print(empresa["nombre"])

    return

    pdf_path = f"{nombre_proveedor}/{nombre_archivo}.pdf"
    excel_path = f"{nombre_proveedor}/{nombre_archivo}.xlsx"

    paginas = ft_texto.extraer_paginas_texto(pdf_path)
    
    facturas = []
    for pagina in paginas:
        factura = ft_texto.registros_facturas(pagina, nombre_proveedor, nif_proveedor, extractores)
        if factura:
            facturas.append(factura)
    
    if facturas:
        facturas_correctas, facturas_con_errores = clasificar_facturas(facturas)
        ft.exportar_a_excel(facturas_correctas, facturas_con_errores, excel_path)
    print()

if __name__ == "__main__":
    main()
