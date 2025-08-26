"""
Módulo que contiene la clase App, ventana principal de la aplicación.
"""
import tkinter as tk
from controlador.controlador import Controlador

from tkinter import ttk, filedialog
from typing import Optional

# Importamos las clases de los frames de la aplicación
from vista.frameSeleccionarEmpresa import SeleccionarEmpresa
from vista.frameSeleccionarArchivo import SeleccionarArchivo
# from vista.frame_proceso import FrameProcesamiento
# from vista.frame_resultados import FrameResultados

class App(tk.Tk):
    """
    Clase principal de la aplicación que hereda de tk.Tk.
    Gestiona la ventana principal y los diferentes frames.
    """
    def __init__(self):
        super().__init__()
        self.title("DistiScan V1.0 - Distirel ©")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self._configurar_estilo()

        self.controlador = Controlador()
          
        # Diccionario para almacenar los frames
        self.frames = {}
        self._inicializar_frames()
        self.mostrar_frame('SeleccionarEmpresa')
        
    def _configurar_estilo(self):
        """Configura el estilo global de la aplicación."""
        estilo_bg = "#f0f0f0"
        estilo_font = ("Arial", 10, "bold")
        self.configure(background=estilo_bg)
        self.style = ttk.Style()
        self.style.theme_use("clam")  # clam alt default classic aqua
        
        # Configurar colores y estilos
        self.style.configure("TFrame", background=estilo_bg)
        self.style.configure("TButton", font=estilo_font, background="#e1e1e1", width=14, padding=(0, 7, 0, 7))
        self.style.configure("TLabel", font=estilo_font, background='#3d8624')
        self.style.configure("Header.TLabel", font=("Arial", 14, "bold"), background=estilo_bg)


    def _inicializar_frames(self):
        """Inicializa todos los frames de la aplicación."""
        # Lista de clases de frames a inicializar
        frameClasses = [
            SeleccionarEmpresa,
            SeleccionarArchivo
            # FrameProcesamiento,
            # FrameResultados
            ]
        
        # Crear instancias de cada frame
        for frameClass in frameClasses:
            frame = frameClass(parent=self, app=self, controlador=self.controlador)
            self.frames[frame.nombre] = frame
    
    def mostrar_frame(self, nombre_frame: str):
        """
        Muestra el frame especificado.
        
        Args:
            nombre_frame: Nombre del frame a mostrar
        """
        if nombre_frame in self.frames:
            frame = self.frames[nombre_frame]
            frame.grid(row=0, column=0, sticky="nsew")
            frame.tkraise()
            # Si el frame tiene un método de inicialización, lo llamamos
            if hasattr(frame, "inicializar"):
                frame.inicializar()
    
   
    def seleccionar_archivo(self, tipos_archivo: list, titulo: str = "Seleccionar archivo") -> Optional[str]:
        """
        Muestra un diálogo para seleccionar un archivo.
        
        Args:
            tipos_archivo: Lista de tuplas con descripciones y extensiones
            titulo: Título del diálogo
            
        Returns:
            Ruta del archivo seleccionado o None si se cancela
        """
        ruta = filedialog.askopenfilename(
            title=titulo,
            filetypes=tipos_archivo
        )
        return ruta if ruta else None
    
    def seleccionar_directorio(self, titulo: str = "Seleccionar directorio") -> Optional[str]:
        """
        Muestra un diálogo para seleccionar un directorio.
        
        Args:
            titulo: Título del diálogo
            
        Returns:
            Ruta del directorio seleccionado o None si se cancela
        """
        ruta = filedialog.askdirectory(title=titulo)
        return ruta if ruta else None
    
    def guardar_archivo(self, tipos_archivo: list, titulo: str = "Guardar archivo") -> Optional[str]:
        """
        Muestra un diálogo para guardar un archivo.
        
        Args:
            tipos_archivo: Lista de tuplas con descripciones y extensiones
            titulo: Título del diálogo
            
        Returns:
            Ruta del archivo a guardar o None si se cancela
        """
        ruta = filedialog.asksaveasfilename(
            title=titulo,
            filetypes=tipos_archivo
        )
        return ruta if ruta else None
