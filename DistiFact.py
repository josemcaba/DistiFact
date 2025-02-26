import pdfplumber
import re
import pandas as pd
import os
from importlib import import_module    # Para importar un modulo almacenado en una variable
import ft_comunes as ft
import ft_menu 

def procesar_seccion(seccion, nombre_proveedor, nif_proveedor, extractores):
    """
    Procesa una sección de texto para extraer los datos de una factura.
    Retorna un diccionario con los datos de la factura.
    """
    if "Fecha emisión" not in seccion:
        return None

    extraer = import_module(extractores[:-3])
    datos_factura = {
        "Num. Factura": extraer.numero_factura(seccion),
        "Fecha Fact.": extraer.fecha(seccion),
        "Fecha Oper.": extraer.fecha(seccion),
        "Concepto": 700,
        "Base I.V.A.": extraer.base_iva(seccion),
        "% I.V.A.": 0,
        "Cuota I.V.A.": extraer.cuota_iva(seccion),
        "Base I.R.P.F.": extraer.base_iva(seccion),
        "% I.R.P.F.": 0,
        "Cuota I.R.P.F.": 0,
        "Base R. Equiv.": extraer.base_iva(seccion),
        "% R. Equiv.": 0,
        "Cuota R. Equiv.": 0,
        "NIF/DNI": extraer.nif_cliente(seccion, nif_proveedor),
        "Nombre": extraer.nombre_cliente(seccion, nombre_proveedor),
        "Total Factura": extraer.total_factura(seccion)
    }

    # Calcular % I.V.A.
    base_valor = datos_factura["Base I.V.A."]
    iva_valor = datos_factura["Cuota I.V.A."]
    datos_factura["% I.V.A."] = int(round((iva_valor / base_valor) * 100)) if base_valor else 0

    return datos_factura

def extraer_informacion_facturas(pdf_path, nombre_proveedor, nif_proveedor, extractores):
    """
    Extrae la información de las facturas de un archivo PDF.
    Retorna una lista de diccionarios con los datos de las facturas.
    """
    if not os.path.exists(pdf_path):
        print(f"El archivo {pdf_path} no existe.")
        return []

    texto_completo = ""
    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if texto:
                texto_completo += texto + "\n"

    secciones = re.split(r"(?=Fecha emisión)", texto_completo)
    facturas = [procesar_seccion(seccion, nombre_proveedor, nif_proveedor, extractores) for seccion in secciones \
                                            if procesar_seccion(seccion, nombre_proveedor, nif_proveedor, extractores)]
    return facturas

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

def exportar_a_excel(facturas_correctas, facturas_con_errores, excel_path):
    """
    Exporta las facturas correctas y con errores a archivos Excel separados.
    """
    columnas = [
        "Num. Factura", "Fecha Fact.", "Fecha Oper.", "Concepto",
        "Base I.V.A.", "% I.V.A.", "Cuota I.V.A.", 
        "Base I.R.P.F.", "% I.R.P.F.", "Cuota I.R.P.F.",
        "Base R. Equiv.", "% R. Equiv.", "Cuota R. Equiv.",
        "NIF/DNI", "Nombre"
    ]
    
    # Exportar facturas correctas
    if facturas_correctas:
        df_correctas = pd.DataFrame(facturas_correctas, columns=columnas)
        df_correctas = df_correctas.sort_values(by=columnas[0])
        df_correctas.to_excel(excel_path.replace(".xlsx", "_correctas.xlsx"), index=False)
        print(f"Se han exportado {len(facturas_correctas)} facturas correctas.")
    else:
        print("No hay facturas correctas para exportar.")

    # Exportar facturas con errores
    if facturas_con_errores:
        df_errores = pd.DataFrame(facturas_con_errores, columns=columnas + ["Errores"])
        df_errores = df_errores.sort_values(by=columnas[0])
        df_errores.to_excel(excel_path.replace(".xlsx", "_errores.xlsx"), index=False)
        print(f"Se han exportado {len(facturas_con_errores)} facturas con errores.")
    else:
        print("No hay facturas con errores para exportar.")

def main():
    is_PDF_texto = ft_menu.seleccionar_tipo_PDF()
    if is_PDF_texto is None:
        return
    json_file='proveedores_PDFtext.json' if is_PDF_texto else 'proveedores_PDFimagen.json'
    
    nombre_proveedor, nif_proveedor, extractores = ft_menu.seleccionar_proveedor(json_file)
    if nombre_proveedor is None:
        return

    nombre_archivo = input("Nombre del archivo PDF sin '.pdf' (merged): ").strip()
    if not nombre_archivo:
        nombre_archivo = "merged"
    print()

    pdf_path = f"{nombre_proveedor}/{nombre_archivo}.pdf"
    excel_path = f"{nombre_proveedor}/{nombre_archivo}.xlsx"

    facturas = extraer_informacion_facturas(pdf_path, nombre_proveedor, nif_proveedor, extractores)
    if facturas:
        facturas_correctas, facturas_con_errores = clasificar_facturas(facturas)
        exportar_a_excel(facturas_correctas, facturas_con_errores, excel_path)
    print()

if __name__ == "__main__":
    main()
