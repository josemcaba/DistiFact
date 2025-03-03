import re
from datetime import datetime
import pandas as pd
import pdfplumber

def convertir_a_float(valor_str):
    """
    Convierte una cadena con formato numérico usando el separador decimal)
    a un número flotante. Si falla, retorna 0.0.
    """
    # Sustituye las comas por puntos
    valor_str = re.sub(r",", ".", valor_str) 
    # Elimina todos los puntos salvo el último
    valor_str = re.sub(r"\.(?=.*\.)", "", valor_str)
    try:
        return round(float(valor_str), 2)
    except:
        return None

def validar_fecha(fecha_str, is_eeuu=False):
    """
    Valida que una fecha esté en alguno de los formatos:
    desde dd/mm/aaaa hasta d/m/aa.
    
    Si no is_euro tambien valida los formatos:
    desde mm/dd/aaaa hasta m/d/aa.
    
    Si es válida, retorna la fecha en formato dd/mm/aaaa.
    Si no, retorna False.
    """
    # Se valida la estructura general con una expresión regular
    if not re.match(r"^\d{1,2}/\d{1,2}/(\d{2}|\d{4})$", fecha_str):
        return False

    # Se definen los formatos posibles
    formatos = ["%d/%m/%Y", "%d/%m/%y"]
    if is_eeuu:
        formatos.extend(["%m/%d/%Y", "%m/%d/%y"])

    for fmt in formatos:
        try:
            dt = datetime.strptime(fecha_str, fmt)
            return dt.strftime("%d/%m/%Y")
        except ValueError:
            continue

    return False

def validar_nif(nif):
    """
    Valida un NIF (DNI, NIE o CIF) según las normas españolas.
    Retorna True si es válido, False en caso contrario.
    """
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
    letra_calculada = letras[numero % 23]
    return dni[-1] == letra_calculada

def validar_nie(nie):
    """
    Valida un NIE español.
    """
    # Convertir la primera letra a un número
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

def extraerPaginasPDF_tipoTexto(pdf_path, separador):
    texto_completo = ""
    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if texto:
                texto_completo += texto + "\n"
    
    paginas = re.split(rf"(?={separador})", texto_completo)
    del paginas[0]

    return (paginas)

def exportar_a_excel(facturas_correctas, facturas_con_errores, excel_path):
    """
    Exporta las facturas correctas y con errores a archivos Excel separados.
    """
    columnas = [
        "Numero Factura", "Fecha Factura", "Fecha Operacion", "Concepto",
        "Base IVA", "Tipo IVA", "Cuota IVA", 
        "Base IRPF", "Tipo IRPF", "Cuota IRPF",
        "Base R. Equiv.", "Tipo R. Equiv.", "Cuota R. Equiv.",
        "NIF", "Nombre Cliente"
    ]

    # Exportar facturas correctas
    if facturas_correctas:
        df_correctas = pd.DataFrame(facturas_correctas, columns=columnas + ["Observaciones"])
        df_correctas = df_correctas.sort_values(by=columnas[1])
        df_correctas.to_excel(excel_path.replace(".xlsx", "_correctas.xlsx"), index=False)
        print(f"Se han exportado {len(facturas_correctas)} facturas correctas.")
    else:
        print("No hay facturas correctas para exportar.")

    # Exportar facturas con errores
    if facturas_con_errores:
        df_errores = pd.DataFrame(facturas_con_errores, columns=columnas + ["Errores"])
        df_errores = df_errores.sort_values(by=columnas[1])
        df_errores.to_excel(excel_path.replace(".xlsx", "_errores.xlsx"), index=False)
        print(f"Se han exportado {len(facturas_con_errores)} facturas con errores.")
    else:
        print("No hay facturas con errores para exportar.")

def re_search(regex, pagina):
    match = re.search(regex, pagina)
    return match.group(1) if match else None