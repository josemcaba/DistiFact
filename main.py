"""
Punto de entrada principal de la aplicación DistiFact con interfaz gráfica Tkinter.
"""
import os
import sys

# Agregar directorio actual al path para importaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar componentes de la aplicación
from controlador.controlador import Controlador
from app import App


# def main():
#     """Función principal que inicia la aplicación."""
#     # Crear instancia del controlador
#     controlador = Controlador()
    
#     # Inicializar controlador
#     if not controlador.iniciar("empresas.json"):
#         print("Error al cargar el archivo de empresas.")
#         return
    
#     # Crear y configurar la aplicación
#     app = App(controlador)
    
#     # Iniciar el bucle principal de la aplicación
#     app.mainloop()

def main():
    app = App()

if __name__ == "__main__":
    main()
