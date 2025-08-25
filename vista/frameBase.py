"""
Módulo que contiene la clase FrameBase, base para todos los frames de la aplicación.
"""
from tkinter import ttk
from typing import Dict, Any, Optional


class FrameBase(ttk.Frame):
    """
    Clase base para todos los frames de la aplicación.
    """
    def __init__(self, parent, app, controlador):
        """
        Inicializa el frame base.
        
        Args:
            app: Instancia de la aplicación principal
            parent: Widget padre
            controlador: Instancia del controlador
        """
        super().__init__(parent)
        self.app = app
        self.controlador = controlador
        
        # Configuración del frame
        self.configure(padding="10")
        
        # Inicializar componentes
        self._inicializar_componentes()
    
    def _inicializar_componentes(self):
        """
        Inicializa los componentes del frame.
        Este método debe ser sobrescrito por las clases hijas.
        """
        # Título del frame
        self.lbl_titulo = ttk.Label(
            self, 
            text=self._obtener_titulo(),
            style="Header.TLabel"
        )
        self.lbl_titulo.pack(pady=(0, 20))
    
    def _obtener_titulo(self) -> str:
        """
        Retorna el título del frame.
        Este método debe ser sobrescrito por las clases hijas.
        
        Returns:
            Título del frame
        """
        return "Frame Base"
    
    def inicializar(self):
        """
        Método llamado cuando el frame se muestra.
        Este método puede ser sobrescrito por las clases hijas.
        """
        pass
    
    def mostrar_mensaje(self, tipo: str, mensaje: str, titulo: Optional[str] = None):
        """
        Muestra un mensaje usando el método de la aplicación principal.
        
        Args:
            tipo: Tipo de mensaje ('info', 'error', 'warning')
            mensaje: Contenido del mensaje
            titulo: Título del diálogo (opcional)
        """
        self.app.mostrar_mensaje(tipo, mensaje, titulo)
