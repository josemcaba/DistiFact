"""
Módulo que contiene la clase FrameBase, base para todos los frames de la aplicación.
"""
from tkinter import ttk
from typing import Dict, Any, Optional

class FrameBase(ttk.Frame):
    def __init__(self, parent, app, controlador, titulo):
        """
        Args:
            parent: Widget padre
            app: Instancia de la aplicación principal
            controlador: Instancia del controlador
        """
        super().__init__(parent)
        self.app = app
        self.controlador = controlador
        self._nombre = self.__class__.__name__
        self.titulo = titulo
        self._configurar_frame()
        self._configurar_titulo()

    @property
    def nombre(self) -> str:
        return self._nombre
        
    # Configure the frame itself to expand
    def _configurar_frame(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)  # Título
        self.rowconfigure(1, weight=1)  # Marco principal
        self.rowconfigure(2, weight=0)  # Botones

    def _configurar_titulo(self):
        marco_titulo = ttk.Label(self)
        marco_titulo.grid(row=0, column=0, sticky="ew", pady=5)
        marco_titulo.configure(text=self.titulo, anchor='c', 
                                foreground='white', font=('Arial', 15, 'bold'))

        
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
