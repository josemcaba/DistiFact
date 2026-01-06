"""
Punto de entrada principal de la aplicación DistiFact con interfaz gráfica Tkinter.
"""
import os
import sys

# Agregar directorio actual al path para importaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar componentes de la aplicación
from controlador.controlador import Controlador
from vista.app import App


def main():
    """Función principal que inicia la aplicación."""
    # Crear instancia del controlador
    controlador = Controlador()

    # Definir ruta del archivo empresas.json usando una ruta relativa
    # El archivo está en el directorio 'datos' dentro del proyecto
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_empresas = os.path.join(ruta_base, "datos", "empresas.json")
    
    print(f"Buscando archivo de empresas en: {ruta_empresas}")
    
    # Verificar si el archivo existe antes de intentar cargarlo
    if not os.path.exists(ruta_empresas):
        print(f"Error: No se encontró el archivo {ruta_empresas}")
        print("Por favor, asegúrate de que el archivo empresas.json existe en el directorio 'datos'.")
        return
    
    # Inicializar controlador
    if not controlador.iniciar(ruta_empresas):
        print("Error al cargar el archivo de empresas.")
        return
    
    # Crear y configurar la aplicación
    app = App(controlador)
    
    # Iniciar el bucle principal de la aplicación
    app.mainloop()


if __name__ == "__main__":
    main()
