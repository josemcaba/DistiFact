import tkinter as tk
from tkinter import ttk
from typing import Optional, Any, TYPE_CHECKING  # <--- Añadir TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from app import App  # Forward reference para evitar importación circular

class FrameBase(ttk.Frame, ABC):
    """Clase base abstracta para todos los frames."""
    
    nombre: str = "base"
    
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
    
    def _crear_cabecera_empresa(self, mostrar_boton: bool = False):
        """Crea la cabecera con información de la empresa seleccionada."""
        # Frame para información de empresa
        self.frame_empresa = ttk.Frame(self)
        self.frame_empresa.pack(fill="x", padx=5, pady=(10, 5))
        
        # Información de la empresa (izquierda)
        f_info = ttk.Frame(self.frame_empresa)
        f_info.pack(side="left", fill="x", expand=True)
        
        ttk.Label(f_info, text="Empresa seleccionada:").pack(anchor="w")
        self.lbl_empresa_info = ttk.Label(
            f_info, 
            text="", 
            relief="solid", 
            padding=5,
            style="Info.TLabel"  # Nuevo estilo para información de empresa
        )
        self.lbl_empresa_info.pack(anchor="w", pady=(5, 0), padx=(0, 5))
        
        # Botón Unificar PDFs (derecha, solo si se solicita)
        if mostrar_boton:
            self.btn_unificar = ttk.Button(
                self.frame_empresa, 
                text="Unificar PDFs", 
                command=self._on_unificar_pdfs
            )
            self.btn_unificar.pack(side="right", pady=(19, 0))
        
        # Separador
        ttk.Separator(self, orient="horizontal").pack(fill='x', padx=5, pady=5)
    
    def _actualizar_info_empresa(self):
        """Actualiza la información de la empresa en la cabecera."""
        empresa = self.controlador.obtener_empresa_actual()
        if empresa and hasattr(self, 'lbl_empresa_info'):
            texto = f"{empresa.nombre} ({empresa.nif}) - Tipo: {empresa.tipo}"
            self.lbl_empresa_info.config(text=texto)
    
    def _on_unificar_pdfs(self):
        """Método base para unificar PDFs (puede ser sobrescrito)."""
        directorio = self.app.seleccionar_directorio("Directorio con PDFs a unificar")
        if directorio:
            res = self.controlador.unificar_pdfs(directorio)
            tipo = "info" if res["exito"] else "error"
            mensaje = res["mensaje"]
            if res.get('ruta_salida'):
                mensaje += f"\nGenerado: {res.get('ruta_salida')}"
            self.mostrar_mensaje(tipo, mensaje)
