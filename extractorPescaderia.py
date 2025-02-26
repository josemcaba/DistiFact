import re
import funciones_comunes as ft

def numero_factura(seccion):
    """
    Extrae el número de factura de una sección de texto.
    Retorna el número como entero o 0 si no se encuentra.
    """
    num_factura = re.search(r"Nº factura\s*(\d+)", seccion)
    return int(num_factura.group(1)) if num_factura else 0

def fecha(seccion):
    """
    Extrae la fecha de emisión de una sección de texto.
    Retorna la fecha como cadena o 0 si no se encuentra.
    """
    fecha = re.search(r"Fecha emisión\s*(.*)", seccion)
    if not fecha:
        return 0
    fecha = re.sub(r"[.,]", "", fecha.group(1))
    return fecha

def base_iva(seccion):
    """
    Extrae la base imponible del IVA de una sección de texto.
    Retorna el valor como float o 0.0 si no se encuentra.
    """
    base = re.search(r"Base\s*([\d,\.]+)", seccion)
    return ft.convertir_a_float(base.group(1)) if base else 0.0

def porcentaje_iva(seccion):
    """
    Extrae el % IVA de una sección de texto.
    Retorna el valor como float o 0.0 si no se encuentra.
    """
    return 0.0

def cuota_iva(seccion):
    """
    Extrae la cuota de IVA de una sección de texto.
    Retorna el valor como float o 0.0 si no se encuentra.
    """
    iva = re.search(r"IVA\s*([\d,\.]+)", seccion)
    return ft.convertir_a_float(iva.group(1)) if iva else 0.0

def total_factura(seccion):
    """
    Extrae el total de la factura de una sección de texto.
    Retorna el valor como flotante o 0.0 si no se encuentra.
    """
    total_match = re.search(r"Total\s*([\d,\.]+)\s*€?", seccion)
    return ft.convertir_a_float(total_match.group(1)) if total_match else 0.0


def nif_cliente(seccion, nif_proveedor):
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

def nombre_cliente(seccion, nombre_proveedor):
    """
    Extrae el nombre del cliente a partir del patrón "Pescadería Salvador".
    Se asume que en la sección aparece una línea con el formato:
    "Pescadería Salvador [Nombre del cliente]"

    Retorna el nombre del cliente (cadena) o 0 si no se encuentra.
    """
    nombre = re.search(rf"{nombre_proveedor}\s*(.+)", seccion)
    return nombre.group(1).strip() if nombre else 0
