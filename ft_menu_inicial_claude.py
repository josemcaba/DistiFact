# -*- coding: utf-8 -*-
"""
Módulo para la gestión de empresas y selección de archivos PDF
"""
import json
import os

def cargar_empresas(ruta_json):
    """
    Carga los datos de las empresas desde un archivo JSON.
    
    Args:
        ruta_json (str): Ruta al archivo JSON con datos de empresas
        
    Returns:
        dict: Diccionario con los datos de las empresas o None si hay error
    """
    try:
        with open(ruta_json, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    except Exception as e:
        print(f"Error al cargar el archivo JSON: {e}")
        return None

def mostrar_menu(empresas):
    """
    Muestra un menú con las empresas disponibles.
    
    Args:
        empresas (dict): Diccionario con los datos de las empresas
        
    Returns:
        None
    """
    print("\n=== SELECCIÓN DE EMPRESA ===")
    for id_empresa, datos in empresas.items():
        print(f"{id_empresa}. {datos['nombre']} ({datos['nif']})")
    print("0. Salir")

def seleccionar_empresa(empresas):
    """
    Permite al usuario seleccionar una empresa del menú.
    
    Args:
        empresas (dict): Diccionario con los datos de las empresas
        
    Returns:
        dict or None: Datos de la empresa seleccionada o None si se elige salir
    """
    while True:
        mostrar_menu(empresas)
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "0":
            return None
        
        if opcion in empresas:
            return empresas[opcion]
        
        print("Opción no válida. Intente nuevamente.")

def obtener_ruta_pdf(empresa):
    """
    Solicita al usuario el nombre de un archivo PDF y construye la ruta relativa.
    
    Args:
        empresa (dict): Diccionario con los datos de la empresa seleccionada
        
    Returns:
        str: Ruta relativa al archivo PDF
    """
    nombre_directorio = empresa["nombre"]
    nombre_archivo = input(f"Introduzca el nombre del archivo PDF en el directorio '{nombre_directorio}': ")
    
    # Añadir extensión .pdf si no está presente
    if not nombre_archivo.lower().endswith('.pdf'):
        nombre_archivo += '.pdf'
    
    # Construir ruta relativa
    ruta_relativa = os.path.join(nombre_directorio, nombre_archivo)
    
    return ruta_relativa

def procesar_seleccion(ruta_json="empresas.json"):
    """
    Función principal que gestiona la selección de empresa y archivo PDF.
    
    Args:
        ruta_json (str): Ruta al archivo JSON con datos de empresas
        
    Returns:
        tuple or None: Tupla (ruta_pdf, datos_empresa) o None si se cancela
    """
    # Cargar datos de empresas
    empresas = cargar_empresas(ruta_json)
    if not empresas:
        return None
    
    # Seleccionar empresa
    empresa = seleccionar_empresa(empresas)
    if not empresa:
        print("Programa finalizado.")
        return None
    
    # Obtener ruta del archivo PDF
    ruta_pdf = obtener_ruta_pdf(empresa)
    
    return (ruta_pdf, empresa)

if __name__ == "__main__":
    ruta_pdf, datos_empresa = procesar_seleccion()
    if datos_empresa:
        print("\nSelección realizada:")
        print(f"Empresa: {datos_empresa['nombre']}")
        print(f"Ruta al PDF: {ruta_pdf}")
        print(f"Datos completos: {datos_empresa}")