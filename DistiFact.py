import pdfplumber
import re
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
    separador = "<>>>>> FACTURA <<<<<>\n"
    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if texto:
                texto_completo += separador + texto + "\n"

    paginas = re.split(separador, texto_completo)
                                        
    facturas = []
    for pagina in paginas:
        factura = procesar_seccion(pagina, nombre_proveedor, nif_proveedor, extractores)
        if factura:
            facturas.append(factura)

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

def main():
    json_file = ft_menu.seleccionar_tipo_PDF()
    if json_file is None:
        return
    
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
        ft.exportar_a_excel(facturas_correctas, facturas_con_errores, excel_path)
    print()

if __name__ == "__main__":
    main()
