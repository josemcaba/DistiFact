from importlib import import_module    # Para importar un modulo almacenado en una variable
import ft_comunes as ft
from ft_cargarDatosEmpresa import cargarDatosEmpresa
import verificadoresPescaderia as verificar


def clasificar_facturas(facturas):
    """
    Clasifica las facturas en correctas y con errores.
    Retorna dos listas: facturas_correctas y facturas_con_errores.
    """
    facturas_correctas = []
    facturas_con_errores = []

    for factura in facturas:
        errores = []

        error = verificar.num_factura(factura)
        errores.append(error) if error else None

        error = verificar.fecha(factura)
        errores.append(error) if error else None

        error = verificar.iva(factura)
        errores.append(error) if error else None

        # Verificar Cuota IVA
        cuota = 0.0
        if factura["Cuota I.V.A."] is None:
            errores.append("Cuota I.V.A. no encontrada")
        else:
            cuota = ft.convertir_a_float(factura["Cuota I.V.A."])
            if cuota is None:
                errores.append("Cuota I.V.A. incorrecta")
            else:
                factura["Cuota I.V.A."] = cuota
        
        # Verificar Total Factura
        total = 0.0
        if factura["Total Factura"] is None:
            errores.append("Total Factura no encontrada")
        else:
            total = ft.convertir_a_float(factura["Total Factura"])
            if total is None:
                errores.append("Total Factura incorrecta")
            else:
                factura["Total Factura"] = total

        # Verificar % I.V.A.
        base = float(factura["Cuota I.V.A."])
        if base and cuota:
            factura["% I.V.A."] = round((cuota / base) * 100.0, 0)
        if factura["% I.V.A."] != 10:
            errores.append("% I.V.A. es distinto de 10")
      
        # Verificar NIF
        if factura["NIF/DNI"] is None:
            errores.append("NIF/DNI no encontrado")
        else:
            nif = factura["NIF/DNI"].replace("-","")
            if ft.validar_nif(nif):
                factura["NIF/DNI"] = nif
            else:
                errores.append("NIF/DNI incorrecto")

        # Verificar Nombre del cliente
        if factura["Nombre"] is None:
            errores.append("Nombre del cliente no encontrado")
        elif len(factura["Nombre"]) > 40:
            errores.append("Nombre del cliente demasiado largo. Máximo 40 caracteres.")

        # Verificar diferencias en el total
        if base and cuota and total:
            total_calculado = base + cuota
            if abs(total_calculado - total) > 0.01:
                errores.append(f"Diferencia en total factura ({total_calculado} != {total})")

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

    extractores = empresa["extractores"]
    extraer = import_module(extractores[:-3])
    facturas = extraer.facturas_del_PDF(ruta_PDF, empresa)

    if facturas:
        facturas_correctas, facturas_con_errores = clasificar_facturas(facturas)
        excel_path=ruta_PDF.replace(".pdf", ".xlsx")
        ft.exportar_a_excel(facturas_correctas, facturas_con_errores, excel_path)
    print()

if __name__ == "__main__":
    main()
