import json
import os

def cargar_empresas(archivo_json):
    """
    Carga las empresas desde un archivo JSON y las devuelve como diccionario.
    
    Argumentos:
        archivo_json (str): Ruta del archivo JSON que contiene los datos de las empresas.
    
    Retorna:
        dict: Diccionario con los datos de las empresas.
    """
    with open(archivo_json, 'r', encoding='utf-8') as file:
        return json.load(file)

def mostrar_menu(empresas):
    """
    Muestra un menú con las empresas disponibles y permite al usuario elegir una.
    
    Argumentos:
        empresas (dict): Diccionario con los datos de las empresas.
    
    Retorna:
        str: ID de la empresa seleccionada o None si se elige salir.
    """
    print("Seleccione una empresa:")
    for key, empresa in empresas.items():
        print(f"{key}. {empresa['nombre']} ({empresa['nif']})")
    print("0. Salir")
    
    opcion = input("Ingrese el número de la empresa (o 0 para salir): ")
    if opcion == "0":
        return None
    elif opcion in empresas:
        return opcion
    else:
        print("Opción no válida. Intente nuevamente.")
        return mostrar_menu(empresas)

def obtener_archivo_pdf(empresa):
    """
    Pregunta al usuario el nombre de un archivo PDF relacionado con la empresa seleccionada.
    
    Argumentos:
        empresa (dict): Datos de la empresa seleccionada.
    
    Retorna:
        str: Path relativo al archivo PDF.
    """
    nombre_empresa = empresa['nombre']
    # directorio = nombre_empresa.replace(" ", "_")  # Normalizar el nombre del directorio
    directorio = nombre_empresa
    if not os.path.exists(directorio):
        print(f"El directorio '{directorio}' no existe.")
        return None
    
    nombre_pdf = input(f"Ingrese el nombre del archivo PDF (en el directorio '{directorio}'): ")
    if not nombre_pdf.endswith(".pdf"):
        nombre_pdf += ".pdf"
    
    ruta_pdf = os.path.join(directorio, nombre_pdf)
    if not os.path.isfile(ruta_pdf):
        print(f"El archivo '{ruta_pdf}' no existe.")
        return None
    
    return ruta_pdf

def obtener_datos_empresa_y_pdf(archivo_json):
    """
    Obtiene los datos de la empresa seleccionada y el path relativo a un archivo PDF.
    
    Argumentos:
        archivo_json (str): Ruta del archivo JSON que contiene los datos de las empresas.
    
    Retorna:
        tuple: Tupla con el diccionario de datos de la empresa y el path relativo al archivo PDF,
               o (None, None) si el usuario decide salir.
    """
    empresas = cargar_empresas(archivo_json)
    id_empresa = mostrar_menu(empresas)
    
    if id_empresa is None:
        return None, None
    
    empresa_seleccionada = empresas[id_empresa]
    ruta_pdf = obtener_archivo_pdf(empresa_seleccionada)
    
    if ruta_pdf is None:
        return None, None
    
    return empresa_seleccionada, ruta_pdf

# Ejemplo de uso
if __name__ == "__main__":
    archivo_json = "empresas.json"  # Asegúrate de que este archivo exista en el mismo directorio
    empresa, pdf_path = obtener_datos_empresa_y_pdf(archivo_json)
    
    if empresa and pdf_path:
        print("\nDatos de la empresa seleccionada:")
        print(empresa)
        print(f"\nRuta relativa al archivo PDF: {pdf_path}")
    else:
        print("Operación cancelada.")