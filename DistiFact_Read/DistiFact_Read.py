import pdfplumber
import re
import pandas as pd
import os
import funciones_comunes as ft
from mostrar_menu import mostrar_menu

def extraer_numero_factura(seccion):
    """
    Extrae el número de factura de una sección de texto.
    Retorna el número como entero o 0 si no se encuentra.
    """
    num_factura = re.search(r"Nº factura\s*(\d+)", seccion)
    return int(num_factura.group(1)) if num_factura else 0

def extraer_fecha(seccion):
    """
    Extrae la fecha de emisión de una sección de texto.
    Retorna la fecha como cadena o 0 si no se encuentra.
    """
    fecha = re.search(r"Fecha emisión\s*(.*)", seccion)
    if not fecha:
        return 0
    fecha = re.sub(r"[.,]", "", fecha.group(1))
    return fecha

def extraer_base_iva(seccion):
    """
    Extrae la base imponible del IVA de una sección de texto.
    Retorna el valor como float o 0.0 si no se encuentra.
    """
    base = re.search(r"Base\s*([\d,\.]+)", seccion)
    return ft.convertir_a_float(base.group(1)) if base else 0.0

def extraer_cuota_iva(seccion):
    """
    Extrae la cuota de IVA de una sección de texto.
    Retorna el valor como float o 0.0 si no se encuentra.
    """
    iva = re.search(r"IVA\s*([\d,\.]+)", seccion)
    return ft.convertir_a_float(iva.group(1)) if iva else 0.0

def extraer_total_factura(seccion):
    """
    Extrae el total de la factura de una sección de texto.
    Retorna el valor como flotante o 0.0 si no se encuentra.
    """
    total_match = re.search(r"Total\s*([\d,\.]+)\s*€?", seccion)
    return ft.convertir_a_float(total_match.group(1)) if total_match else 0.0


def extraer_nombre_cliente(seccion, nombre_proveedor):
    """
    Extrae el nombre del cliente a partir del patrón "Pescadería Salvador".
    Se asume que en la sección aparece una línea con el formato:
    "Pescadería Salvador [Nombre del cliente]"

    Retorna el nombre del cliente (cadena) o 0 si no se encuentra.
    """
    nombre = re.search(rf"{nombre_proveedor}\s*(.+)", seccion)
    return nombre.group(1).strip() if nombre else 0

def extraer_nif_cliente(seccion, nif_proveedor):
    """
    Extrae el NIF del cliente a partir del patrón "25041071-M".
    Se asume que en la sección aparece una línea con el formato:
    "25041071-M [NIF del cliente]"

    Retorna el NIF validado (cadena) si se encuentra y es válido, 
    "NIF Inválido" si la validación falla o 0 si no se encuentra.
    """
    nif = re.search(rf"{nif_proveedor}\s*(.+)", seccion)
 
    if nif:
        nif = re.sub(r"[^a-zA-Z0-9]", "", nif.group(1)).upper()
        if nif == 'X3581661W':
            nif = 'X3586116W'
        return nif if ft.validar_nif(nif) else "NIF Inválido"
    return 0

def procesar_seccion(seccion, nombre_proveedor, nif_proveedor):
    """
    Procesa una sección de texto para extraer los datos de una factura.
    Retorna un diccionario con los datos de la factura.
    """
    if "Fecha emisión" not in seccion:
        return None

    datos_factura = {
        "Num. Factura": extraer_numero_factura(seccion),
        "Fecha Fact.": extraer_fecha(seccion),
        "Fecha Oper.": extraer_fecha(seccion),
        "Concepto": 700,
        "Base I.V.A.": extraer_base_iva(seccion),
        "Cuota I.V.A.": extraer_cuota_iva(seccion),
        "Base I.R.P.F.": extraer_base_iva(seccion),
        "% I.R.P.F.": 0,
        "Cuota I.R.P.F.": 0,
        "Base R. Equiv.": extraer_base_iva(seccion),
        "% R. Equiv.": 0,
        "Cuota R. Equiv.": 0,
        "Nombre": extraer_nombre_cliente(seccion, nombre_proveedor),
        "NIF/DNI": extraer_nif_cliente(seccion, nif_proveedor),
        "Total Factura": extraer_total_factura(seccion)
    }

    # Calcular % I.V.A.
    base_valor = datos_factura["Base I.V.A."]
    iva_valor = datos_factura["Cuota I.V.A."]
    datos_factura["% I.V.A."] = int(round((iva_valor / base_valor) * 100)) if base_valor else 0

    return datos_factura

def extraer_informacion_facturas(pdf_path, nombre_proveedor, nif_proveedor):
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
    facturas = [procesar_seccion(seccion, nombre_proveedor, nif_proveedor) for seccion in secciones \
                                            if procesar_seccion(seccion, nombre_proveedor, nif_proveedor)]
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
            fecha_valida = ft.validar_fecha(fecha_fact)
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
        "Base I.V.A.", "% I.V.A.", "Cuota I.V.A.", "Base I.R.P.F.", "% I.R.P.F.", "Cuota I.R.P.F.",
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
    nombre_proveedor, nif_proveedor = mostrar_menu()
    if nombre_proveedor is None:
        return
    nombre_archivo = input("Nombre del archivo PDF (sin .pdf): ").strip()

    pdf_path = f"{nombre_proveedor}/{nombre_archivo}.pdf"
    excel_path = f"{nombre_proveedor}/{nombre_archivo}.xlsx"

    facturas = extraer_informacion_facturas(pdf_path, nombre_proveedor, nif_proveedor)
    if facturas:
        facturas_correctas, facturas_con_errores = clasificar_facturas(facturas)
        exportar_a_excel(facturas_correctas, facturas_con_errores, excel_path)

if __name__ == "__main__":
    main()
