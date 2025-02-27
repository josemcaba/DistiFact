import json
import os

def cargar_datos_json(ruta_archivo):
    """
    Carga los datos de un archivo JSON y los devuelve como un diccionario.

    Args:
        ruta_archivo (str): Ruta del archivo JSON.

    Returns:
        dict: Diccionario con los datos del archivo JSON.
    """
    with open(ruta_archivo, 'r') as archivo:
        datos = json.load(archivo)
    return datos

def mostrar_menu(datos):
    """
    Muestra un menú con las empresas disponibles y permite al usuario seleccionar una.

    Args:
        datos (dict): Diccionario con los datos de las empresas.

    Returns:
        str: Clave de la empresa seleccionada.
    """
    while True:
        print("\nSeleccione una empresa:")
        for clave, valor in datos.items():
            print(f"{clave}. {valor['nombre']} ({valor['nif']})")
        print("0. Salir")
        
        opcion = input("Ingrese el número de la empresa: ")
        if opcion == '0':
            print("Saliendo del programa...")
            exit()
        elif opcion in datos:
            return opcion
        else:
            print("Opción no válida. Intente de nuevo.")

def solicitar_archivo_pdf(nombre_empresa):
    """
    Solicita al usuario el nombre de un archivo PDF y devuelve la ruta relativa al directorio de la empresa.

    Args:
        nombre_empresa (str): Nombre de la empresa.

    Returns:
        str: Ruta relativa al archivo PDF.
    """
    while True:
        nombre_archivo = input(f"Ingrese el nombre del archivo PDF para {nombre_empresa} (sin extensión .pdf): ").strip()
        if not nombre_archivo:
            print("El nombre del archivo no puede estar vacío. Intente de nuevo.")
            continue
        
        # Añadir la extensión .pdf si no está presente
        if not nombre_archivo.lower().endswith('.pdf'):
            nombre_archivo += '.pdf'
        
        # Construir la ruta relativa
        ruta_archivo = os.path.join(nombre_empresa, nombre_archivo)
        
        # Verificar si el archivo existe
        if os.path.isfile(ruta_archivo):
            return ruta_archivo
        else:
            print(f"El archivo {ruta_archivo} no existe. Intente de nuevo.")

def seleccionar_empresa_y_archivo(ruta_json):
    """
    Carga los datos del JSON, muestra el menú, selecciona una empresa y solicita un archivo PDF.

    Args:
        ruta_json (str): Ruta del archivo JSON.

    Returns:
        tuple: (dict, str) Diccionario con los datos de la empresa y ruta relativa al archivo PDF.
    """
    datos = cargar_datos_json(ruta_json)
    clave_empresa = mostrar_menu(datos)
    empresa_seleccionada = datos[clave_empresa]
    
    ruta_pdf = solicitar_archivo_pdf(empresa_seleccionada['nombre'])
    
    return empresa_seleccionada, ruta_pdf

# Ejemplo de uso
if __name__ == "__main__":
    ruta_json = 'empresas.json'  # Cambiar por la ruta correcta del archivo JSON
    empresa, archivo_pdf = seleccionar_empresa_y_archivo(ruta_json)
    print(f"\nEmpresa seleccionada: {empresa}")
    print(f"Archivo PDF seleccionado: {archivo_pdf}")
