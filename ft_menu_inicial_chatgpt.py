import json
import os

def cargar_datos(archivo_json):
    """
    Carga los datos desde un archivo JSON.
    :param archivo_json: Nombre del archivo JSON.
    :return: Diccionario con los datos del JSON.
    """
    with open(archivo_json, "r", encoding="utf-8") as file:
        return json.load(file)

def mostrar_menu(datos):
    """
    Muestra un menú con las empresas y permite seleccionar una.
    :param datos: Diccionario con los datos de las empresas.
    :return: Clave seleccionada o None si elige salir.
    """
    while True:
        print("\nSeleccione una empresa:")
        for clave, empresa in datos.items():
            print(f"{clave}. {empresa['nombre']} ({empresa['nif']})")
        print("0. Salir")
        opcion = input("Opción: ")
        if opcion == "0":
            return None
        if opcion in datos:
            return opcion
        print("Opción no válida, intente nuevamente.")

def obtener_nombre_pdf(nombre_empresa):
    """
    Solicita el nombre del archivo PDF al usuario.
    :param nombre_empresa: Nombre de la empresa para construir el path.
    :return: Ruta relativa del archivo PDF.
    """
    while True:
        nombre_pdf = input("Ingrese el nombre del archivo PDF (sin o con .pdf): ")
        if not nombre_pdf.lower().endswith(".pdf"):
            nombre_pdf += ".pdf"
        ruta = os.path.join(nombre_empresa, nombre_pdf)
        if os.path.exists(ruta):
            return ruta
        print("El archivo no existe, intente nuevamente.")

def seleccionar_empresa_y_archivo(archivo_json):
    """
    Función principal que gestiona la selección de empresa y archivo.
    :param archivo_json: Nombre del archivo JSON con los datos de empresas.
    :return: Tupla (ruta_pdf, datos_empresa) o (None, None) si se elige salir.
    """
    datos = cargar_datos(archivo_json)
    seleccion = mostrar_menu(datos)
    if seleccion is None:
        return None, None
    empresa = datos[seleccion]
    ruta_pdf = obtener_nombre_pdf(empresa["nombre"])
    return ruta_pdf, empresa

# Ejemplo de uso:
# ruta, empresa = seleccionar_empresa_y_archivo("empresas.json")
# print(ruta, empresa)

# Ejemplo de uso
if __name__ == "__main__":
    archivo_json = "empresas.json"  # Ajusta según tu caso
    ruta, empresa = seleccionar_empresa_y_archivo("empresas.json")
    if ruta:
        print(ruta, empresa)
