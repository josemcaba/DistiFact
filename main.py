"""
Punto de entrada principal de la aplicación DistiFact con interfaz gráfica Tkinter.
Refactorizado para mayor robustez y manejo de errores visual.
"""
import sys
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

# Configuración del path para asegurar que se encuentren los módulos
# Esto es útil si ejecutas el script directamente desde su carpeta
raiz_proyecto = Path(__file__).parent.absolute()
if str(raiz_proyecto) not in sys.path:
    sys.path.append(str(raiz_proyecto))

# Importar componentes de la aplicación
# Se asume que controlador y vista están en el mismo nivel que main.py
try:
    from controlador.controlador import Controlador
    from vista.app import App
except ImportError as e:
    # Capturar error si faltan dependencias críticas
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error Fatal", f"No se pudieron importar componentes necesarios:\n{e}")
    sys.exit(1)

def mostrar_error_critico(titulo: str, mensaje: str):
    """
    Muestra un mensaje de error utilizando Tkinter sin iniciar la app completa.
    Útil para errores de arranque (configuración faltante, etc).
    """
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana raíz vacía
    messagebox.showerror(titulo, mensaje)
    root.destroy()

def main():
    """Función principal que inicia la aplicación."""
    
    # 1. Definir rutas usando pathlib
    ruta_base = Path(__file__).parent.absolute()
    ruta_empresas = ruta_base / "datos" / "empresas.json"
    
    # print(f"Iniciando aplicación en: {ruta_base}") # Debug opcional
    
    # 2. Validación robusta del archivo de configuración
    if not ruta_empresas.exists():
        mensaje = (
            f"No se encontró el archivo de configuración en:\n{ruta_empresas}\n\n"
            "Por favor, asegúrese de que el archivo 'empresas.json' existe "
            "dentro de la carpeta 'datos'."
        )
        print(f"Error: {mensaje}") # Log en consola por si acaso
        mostrar_error_critico("Archivo no encontrado", mensaje)
        sys.exit(1)
    
    try:
        # 3. Inicializar Controlador
        controlador = Controlador()
        
        # Convertimos a string porque algunas librerías antiguas de IO prefieren str sobre Path
        exito_carga = controlador.iniciar(str(ruta_empresas))
        
        if not exito_carga:
            mostrar_error_critico(
                "Error de Datos", 
                "El controlador no pudo cargar el archivo de empresas.\n"
                "Verifique que el formato JSON sea correcto."
            )
            sys.exit(1)
            
        # 4. Iniciar Aplicación (Vista)
        app = App(controlador)
        app.mainloop()
        
    except Exception as e:
        # Captura cualquier otro error no previsto (ej. errores de sintaxis en controlador, etc.)
        import traceback
        traceback.print_exc() # Imprimir detalle técnico en consola
        mostrar_error_critico(
            "Error Inesperado", 
            f"Ocurrió un error crítico al iniciar la aplicación:\n{str(e)}"
        )
        sys.exit(1)

if __name__ == "__main__":
    main()
