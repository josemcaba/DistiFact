"""
Módulo que contiene la clase App, ventana principal de la aplicación.
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from typing import Dict, Any, Optional, Callable

# Importamos los frames de la aplicación
from vista.frame_base import FrameBase
from vista.frame_empresa import FrameSeleccionEmpresa
from vista.frame_archivo import FrameSeleccionArchivo
from vista.frame_proceso import FrameProcesamiento
from vista.frame_resultados import FrameResultados


class App(tk.Tk):
    """
    Clase principal de la aplicación que hereda de tk.Tk.
    Gestiona la ventana principal y los diferentes frames.
    """
    def __init__(self, controlador):
        """
        Inicializa la ventana principal de la aplicación.
        
        Args:
            controlador: Instancia del controlador de la aplicación
        """
        super().__init__()
        
        self.title("DistiScan V1.0 - Distirel ©")
        self.geometry("600x600")
        # self.resizable(False, False)
        # self.minsize(600, 600)
        
        # Configuración de estilo
        self.style = ttk.Style()
        self.style.theme_use("clam")  # clam alt default classic aqua
        
        # Configurar colores y estilos
        self.style.configure("TFrame", 
                            background='#f0f0f0', 
                            font=('Arial', 10))
        self.style.configure('TButton', 
                            background='#e1e1e1',
                            font=('Arial', 10, 'bold'),
                            width=17, 
                            padding=(0, 7, 0, 7))
        self.style.configure('TLabel',
                            background='#f0f0f0', 
                            font=('Arial', 10, 'bold'))
        self.style.configure("Header.TLabel", 
                            background='#3d8624', # verde
                            foreground='#ffffee', # amarillito
                            anchor='c',
                            font=('Arial', 14, 'bold'))
        
        # Referencia al controlador
        self.controlador = controlador
        
        # Contenedor principal
        self.container = ttk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Diccionario para almacenar los frames
        self.frames = {}
        
        # Inicializar frames
        self._inicializar_frames()
        
        # Mostrar el frame inicial
        self.mostrar_frame("seleccion_empresa")
    
    def _inicializar_frames(self):
        """Inicializa todos los frames de la aplicación."""
        # Lista de clases de frames a inicializar
        frame_classes = [
            FrameSeleccionEmpresa,
            FrameSeleccionArchivo,
            FrameProcesamiento,
            FrameResultados
        ]
        
        # Crear instancias de cada frame
        for F in frame_classes:
            nombre_frame = F.nombre
            frame = F(parent=self.container, app=self, controlador=self.controlador)
            self.frames[nombre_frame] = frame
            frame.grid(row=0, column=0, sticky="nsew")
    
    def mostrar_frame(self, nombre_frame: str):
        """
        Muestra el frame especificado.
        
        Args:
            nombre_frame: Nombre del frame a mostrar
        """
        if nombre_frame in self.frames:
            frame = self.frames[nombre_frame]
            frame.tkraise()
            # Si el frame tiene un método de inicialización, lo llamamos
            if hasattr(frame, "inicializar"):
                frame.inicializar()
    
    def mostrar_mensaje(self, tipo: str, mensaje: str, titulo: Optional[str] = None):
        """
        Muestra un mensaje en un diálogo.
        
        Args:
            tipo: Tipo de mensaje ('info', 'error', 'warning')
            mensaje: Contenido del mensaje
            titulo: Título del diálogo (opcional)
        """
        if not titulo:
            titulo = tipo.capitalize()
        
        if tipo == "info":
            messagebox.showinfo(titulo, mensaje)
        elif tipo == "error":
            messagebox.showerror(titulo, mensaje)
        elif tipo == "warning":
            messagebox.showwarning(titulo, mensaje)
    
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
