import pdfplumber
import re
import pandas as pd
import os
from datetime import datetime

def convertir_a_float(valor_str):
    """
    Convierte una cadena con formato numérico (usando comas o puntos como separador decimal)
    a un número flotante. Si falla, retorna 0.0.
    """
    try:
        return round(float(valor_str.replace(",", ".")), 2)
    except (ValueError, AttributeError):
        return 0.0

def extraer_numero_factura(seccion):
    """
    Extrae el número de factura de una sección de texto.
    Retorna el número como entero o 0 si no se encuentra.
    """
    num_factura = re.search(r"Nº factura\s*(\d+)", seccion)
    return int(num_factura.group(1)) if num_factura else 0

def validar_fecha(fecha_str):
    """
    Valida que una fecha tenga el formato dd/mm/aaaa y sea una fecha válida.
    Retorna True si es válida, False en caso contrario.
    """
    if not re.match(r"^\d{2}/\d{2}/\d{4}$", fecha_str):
        return False

    try:
        # Intentar convertir la cadena a un objeto datetime
        datetime.strptime(fecha_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def extraer_fecha(seccion):
    """
    Extrae la fecha de emisión de una sección de texto.
    Retorna la fecha como cadena o 0 si no se encuentra.
    """
    fecha = re.search(r"Fecha emisión\s*([\d/]+)", seccion)
    return fecha.group(1) if fecha else 0

def extraer_base_iva(seccion):
    """
    Extrae la base imponible del IVA de una sección de texto.
    Retorna el valor como cadena o 0 si no se encuentra.
    """
    base = re.search(r"Base\s*([\d,\.]+)", seccion)
    return base.group(1) if base else 0

def extraer_cuota_iva(seccion):
    """
    Extrae la cuota de IVA de una sección de texto.
    Retorna el valor como cadena o 0 si no se encuentra.
    """
    iva = re.search(r"IVA\s*([\d,\.]+)", seccion)
    return iva.group(1) if iva else 0

def extraer_total_factura(seccion):
    """
    Extrae el total de la factura de una sección de texto.
    Retorna el valor como flotante o 0 si no se encuentra.
    """
    total_match = re.search(r"Total\s*([\d,\.]+)\s*€?", seccion)
    return convertir_a_float(total_match.group(1)) if total_match else 0.0

def validar_nif(nif):
    """
    Valida un NIF (DNI, NIE o CIF) según las normas españolas.
    Retorna True si es válido, False en caso contrario.
    """
    if not nif:
        return False

    # Expresiones regulares para DNI, NIE y CIF
    dni_pattern = r"^\d{8}[A-HJ-NP-TV-Z]$"
    nie_pattern = r"^[XYZ]\d{7}[A-HJ-NP-TV-Z]$"
    cif_pattern = r"^[ABCDEFGHJKLMNPQRSUVW]\d{7}[0-9A-J]$"

    if re.match(dni_pattern, nif):
        return validar_dni(nif)
    elif re.match(nie_pattern, nif):
        return validar_nie(nif)
    elif re.match(cif_pattern, nif):
        return validar_cif(nif)
    else:
        return False

def validar_dni(dni):
    """
    Valida un DNI español.
    """
    letras = "TRWAGMYFPDXBNJZSQVHLCKE"
    numero = int(dni[:-1])
    letra_calculada = letras[num % 23]
    return dni[-1].upper() == letra_calculada

def validar_nie(nie):
    """
    Valida un NIE español.
    """
    # Convertir la primera letra a un número
    nie = nie.upper()
    if nie[0] == "X":
        nie = "0" + nie[1:]
    elif nie[0] == "Y":
        nie = "1" + nie[1:]
    elif nie[0] == "Z":
        nie = "2" + nie[1:]

    return validar_dni(nie)

def validar_cif(cif):
    """
    Valida un CIF español.
    """
    cif = cif.upper()
    letra = cif[0]
    numero = cif[1:-1]
    digito_control = cif[-1]

    # Calcular el dígito de control
    suma_pares = sum(int(n) for n in numero[1::2])
    suma_impares = sum(sum(divmod(int(n) * 2, 10)) for n in numero[0::2])
    total = suma_pares + suma_impares
    digito_calculado = str((10 - (total % 10)) % 10)

    if letra in ["A", "B", "E", "H"]:
        return digito_control == digito_calculado
    elif letra in ["K", "P", "Q", "S"]:
        return digito_control in "JABCDEFGHI"[int(digito_calculado)]
    else:
        return digito_control == digito_calculado or digito_control in "JABCDEFGHI"[int(digito_calculado)]

def extraer_nombre_y_nif(seccion):
    """
    Extrae el nombre y el NIF/DNI del cliente de una sección de texto.
    Retorna un diccionario con "Nombre" y "NIF/DNI".
    """
    lines = [line.strip() for line in seccion.splitlines() if line.strip()]
    datos = {"Nombre": 0, "NIF/DNI": 0}

    if "logo" in lines:
        idx_logo = lines.index("logo")
        if len(lines) > idx_logo + 1:
            linea_nombres = lines[idx_logo + 1]
            if "Pescadería Salvador" in linea_nombres:
                datos["Nombre"] = linea_nombres.replace("Pescadería Salvador", "").strip()
            else:
                datos["Nombre"] = linea_nombres

        if len(lines) > idx_logo + 3:
            nif_line = lines[idx_logo + 3]
            tokens = nif_line.split()
            if len(tokens) >= 2:
                # Eliminar caracteres no alfanuméricos y convertir a mayúsculas
                nif_limpio = re.sub(r"[^a-zA-Z0-9]", "", tokens[1]).upper()
                datos["NIF/DNI"] = nif_limpio if validar_nif(nif_limpio) else "NIF Inválido"

    return datos

def procesar_seccion(seccion):
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
        "Base R. Equiv.": extraer_base_iva(seccion),
        "% I.R.P.F.": 0,
        "Cuota I.R.P.F.": 0,
        "% R. Equiv.": 0,
        "Cuota R. Equiv.": 0,
        "Total Factura": extraer_total_factura(seccion),
    }

    # Calcular % I.V.A.
    base_valor = convertir_a_float(datos_factura["Base I.V.A."])
    iva_valor = convertir_a_float(datos_factura["Cuota I.V.A."])
    datos_factura["% I.V.A."] = int(round((iva_valor / base_valor) * 100)) if base_valor else 0

    # Extraer nombre y NIF/DNI
    datos_cliente = extraer_nombre_y_nif(seccion)
    datos_factura.update(datos_cliente)

    return datos_factura

def extraer_informacion_facturas(pdf_path):
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
    facturas = [procesar_seccion(seccion) for seccion in secciones if procesar_seccion(seccion)]
    return facturas

def exportar_a_excel(facturas, excel_path):
    """
    Exporta los datos de las facturas a un archivo Excel.
    """
    columnas = [
        "Num. Factura", "Fecha Fact.", "Fecha Oper.", "Concepto",
        "Base I.V.A.", "% I.V.A.", "Cuota I.V.A.", "Base I.R.P.F.", "% I.R.P.F.", "Cuota I.R.P.F.",
        "Base R. Equiv.", "% R. Equiv.", "Cuota R. Equiv.",
        "NIF/DNI", "Nombre"
    ]

    df = pd.DataFrame(facturas, columns=columnas)
    df.to_excel(excel_path, index=False)
    print(f"Se han extraído {len(facturas)} facturas y exportado a {excel_path}")

def verificar_facturas(facturas):
    """
    Verifica las facturas y muestra aquellas con % I.V.A. distinto de 10, diferencias en el total,
    fechas incorrectas o NIF inválido.
    """
    print("Facturas con % I.V.A. distinto de 10:")
    for factura in facturas:
        if factura.get("% I.V.A.", 0) != 10:
            print(
                f"Num. Factura: {factura.get('Num. Factura')}, "
                f"Fecha Fact.: {factura.get('Fecha Fact.')}, "
                f"Base I.V.A.: {factura.get('Base I.V.A.')}, "
                f"Cuota I.V.A.: {factura.get('Cuota I.V.A.')}, "
                f"% I.V.A.: {factura.get('% I.V.A.')}"
            )

    print("\nFacturas con diferencia entre Total Factura e Importe Calculado:")
    for factura in facturas:
        base_valor = convertir_a_float(factura.get("Base I.V.A.", 0))
        cuota_valor = convertir_a_float(factura.get("Cuota I.V.A.", 0))
        total_factura = factura.get("Total Factura", 0)
        importe_calculado = round(base_valor + cuota_valor, 2)

        if abs(importe_calculado - total_factura) > 0.01:
            print(
                f"Num. Factura: {factura.get('Num. Factura')}, "
                f"Fecha Fact.: {factura.get('Fecha Fact.')}, "
                f"Base I.V.A.: {factura.get('Base I.V.A.')}, "
                f"Cuota I.V.A.: {factura.get('Cuota I.V.A.')}, "
                f"Total Factura: {total_factura}, "
                f"Importe Calculado: {importe_calculado}"
            )

    print("\nFacturas con fecha incorrecta:")
    for factura in facturas:
        fecha_fact = factura.get("Fecha Fact.", 0)
        if fecha_fact != 0 and not validar_fecha(fecha_fact):
            print(
                f"Num. Factura: {factura.get('Num. Factura')}, "
                f"Fecha Fact.: {fecha_fact}"
            )

    print("\nFacturas con NIF inválido:")
    for factura in facturas:
        nif = factura.get("NIF/DNI", 0)
        if nif == "NIF Inválido":
            print(
                f"Num. Factura: {factura.get('Num. Factura')}, "
                f"NIF/DNI: {nif}"
            )

def main():
    nombre_archivo = input("Introduce el nombre del archivo PDF (sin .pdf): ").strip()
    pdf_path = f"{nombre_archivo}.pdf"
    excel_path = f"{nombre_archivo}.xlsx"

    facturas = extraer_informacion_facturas(pdf_path)
    if facturas:
        exportar_a_excel(facturas, excel_path)
        verificar_facturas(facturas)

if __name__ == "__main__":
    main()
