import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Dict, Optional, Type

# Importaciones directas (asegúrate de que __init__.py en 'vista' permita esto o usa rutas absolutas)
from vista.frame_base import FrameBase
from vista.frame_empresa import FrameSeleccionEmpresa
from vista.frame_archivo import FrameSeleccionArchivo
from vista.frame_proceso import FrameProcesamiento
from vista.frame_resultados import FrameResultados

class App(tk.Tk):
    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador
        self.frames: Dict[str, FrameBase] = {}
        
        self._configurar_ventana()
        self._configurar_estilos()
        self._inicializar_interfaz()
        
        self.mostrar_frame("seleccion_empresa")
    
    def _configurar_ventana(self):
        self.title("DistiScan V2.0 - Distirel ©")
        self.geometry("600x600")
        
    def _configurar_estilos(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        estilos = {
            "TFrame": {"background": "#f0f0f0", "font": ('Arial', 10)},
            "TButton": {
                "background": "#e1e1e1", "font": ('Arial', 10, 'bold'),
                "width": 17, "padding": (0, 7, 0, 7)
            },
            "TLabel": {"background": "#f0f0f0", "font": ('Arial', 10, 'bold')},
            "Header.TLabel": {
                "background": "#3d8624", "foreground": "#ffffee",
                "anchor": "c", "font": ('Arial', 14, 'bold')
            },
            "Info.TLabel": {  # <--- Añadir este nuevo estilo
                "background": "#e8f4ff", 
                "foreground": "#003366",
                "font": ('Arial', 10),
                "relief": "solid",
                "borderwidth": 1
            }
        }
        
        for nombre, config in estilos.items():
            self.style.configure(nombre, **config)

    def _inicializar_interfaz(self):
        self.container = ttk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        clases_frames: list[Type[FrameBase]] = [
            FrameSeleccionEmpresa,
            FrameSeleccionArchivo,
            FrameProcesamiento,
            FrameResultados
        ]
        
        for ClaseFrame in clases_frames:
            frame = ClaseFrame(parent=self.container, app=self, controlador=self.controlador)
            self.frames[frame.nombre] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def mostrar_frame(self, nombre_frame: str):
        if nombre_frame in self.frames:
            frame = self.frames[nombre_frame]
            frame.tkraise()
            frame.inicializar()

    def mostrar_mensaje(self, tipo: str, mensaje: str, titulo: Optional[str] = None):
        titulo = titulo or tipo.capitalize()
        iconos = {"info": messagebox.showinfo, "error": messagebox.showerror, "warning": messagebox.showwarning}
        if funcion := iconos.get(tipo):
            funcion(titulo, mensaje)

    def seleccionar_archivo(self, tipos_archivo: list, titulo: str = "Seleccionar archivo") -> Optional[str]:
        ruta = filedialog.askopenfilename(title=titulo, filetypes=tipos_archivo)
        return ruta if ruta else None
    
    def seleccionar_directorio(self, titulo: str = "Seleccionar directorio") -> Optional[str]:
        ruta = filedialog.askdirectory(title=titulo)
        return ruta if ruta else None