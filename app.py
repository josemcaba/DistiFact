"""
Módulo que contiene la clase App, ventana principal de la aplicación.
"""
import tkinter as tk
from controlador.controlador import Controlador

from tkinter import ttk, messagebox, filedialog
from typing import Optional


# Importamos los frames de la aplicación
from vista.frame_empresa import FrameSeleccionEmpresa
from vista.frame_archivo import FrameSeleccionArchivo
from vista.frame_proceso import FrameProcesamiento
from vista.frame_resultados import FrameResultados


class App(tk.Tk):
    """
    Clase principal de la aplicación que hereda de tk.Tk.
    Gestiona la ventana principal y los diferentes frames.
    """
    def __init__(self):
        super().__init__()
        self.title("DistiScan V1.0 - Distirel ©")
        self._configurar_estilo()
    
        # Referencia al controlador
        self.controlador = Controlador()
        # Inicializar controlador
        if not self.controlador.iniciar("empresas.json"):
            print("Error al cargar el archivo de empresas.")
            return

        # Contenedor principal
        self.container = ttk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Diccionario para almacenar los frames
        self.frames = {}
        
        # Inicializar frames
        self._inicializar_frames()
        
        # Mostrar el frame inicial
        self.mostrar_frame("seleccion_empresa")
    
    def _configurar_estilo(self):
        """Configura el estilo global de la aplicación."""
        estilo_bg = "#f0f0f0"
        estilo_font = ("Arial", 10)
        self.configure(bg=estilo_bg)
        self.style = ttk.Style()
        self.style.theme_use("clam")  # clam alt default classic aqua
        
        # Configurar colores y estilos
        self.style.configure("TFrame", background=estilo_bg)
        self.style.configure("TButton", font=estilo_font, background="#4a7abc")
        self.style.configure("TLabel", font=estilo_font, background=estilo_bg)
        self.style.configure("Header.TLabel", font=("Arial", 14, "bold"), background=estilo_bg)


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
