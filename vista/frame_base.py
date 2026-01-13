import tkinter as tk
from tkinter import ttk
from typing import Optional, Any  # <--- Aquí faltaba 'Any'
from abc import ABC, abstractmethod

class FrameBase(ttk.Frame, ABC):
    """Clase base abstracta para todos los frames."""
    
    nombre: str = "base"
    
    # Nota: Usamos 'App' como string (Forward reference) para evitar importación circular
    def __init__(self, parent: tk.Widget, app: 'App', controlador: Any):
        super().__init__(parent)
        self.app = app
        self.controlador = controlador
        self._inicializar_componentes()
    
    def _inicializar_componentes(self):
        """Configuración base común."""
        self.lbl_titulo = ttk.Label(
            self, 
            text=self._obtener_titulo(),
            style="Header.TLabel"
        )
        self.lbl_titulo.pack(fill='x')
    
    @abstractmethod
    def _obtener_titulo(self) -> str:
        """Debe retornar el título del frame."""
        pass
    
    def inicializar(self):
        """Hook para lógica al mostrar el frame."""
        pass
    
    def mostrar_mensaje(self, tipo: str, mensaje: str, titulo: Optional[str] = None):
        """Wrapper para mostrar mensajes desde la App."""
        self.app.mostrar_mensaje(tipo, mensaje, titulo)