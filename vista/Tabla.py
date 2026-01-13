import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Any, Optional, Tuple

class Tabla(tk.Frame):
    def __init__(self, parent: tk.Widget):
        super().__init__(parent)
        self._configurar_grid()
        self._inicializar_widgets()
        self._configurar_estilos()

    def _configurar_grid(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

    def _inicializar_widgets(self):
        self.tabla = ttk.Treeview(self)
        self.tabla.grid(row=0, column=0, sticky="nsew")

        # Scrollbars
        self.scrollbar_v = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=self.scrollbar_v.set)
        self.scrollbar_v.grid(row=0, column=1, sticky="ns", pady=(28, 0))

        self.scrollbar_h = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tabla.xview)
        self.tabla.configure(xscrollcommand=self.scrollbar_h.set)
        self.scrollbar_h.grid(row=1, column=0, sticky="ew")

    def _configurar_estilos(self):
        # Nota: El theme_use global debe ir en App.py, no aquí.
        estilo = ttk.Style()
        estilo.configure('Treeview', 
                         background='#fffbcc',
                         fieldbackground='#ffffee',
                         rowheight=26,
                         font=('Arial', 12))        
        estilo.configure('Treeview.Heading', 
                         background='#afc3cb', 
                         font=('Arial', 10, 'bold'))
        estilo.map('Treeview', background=[('selected', '#2670b2')])

    def cabecera(self, columnas: List[Dict[str, Any]]):
        """Configura las columnas y cabeceras de la tabla."""
        col_names = [col["nombre"] for col in columnas]
        self.tabla.configure(columns=col_names, show='headings')
        
        for columna in columnas:
            nombre = columna["nombre"]
            self.tabla.heading(nombre, text=nombre)
            
            # Configuraciones por defecto si no existen
            config = {
                "width": columna.get("ancho", 100),
                "anchor": columna.get("alineacion", tk.W),
                "stretch": columna.get("expandible", True),
                "minwidth": columna.get("ancho", 50)
            }
            self.tabla.column(nombre, **config)
    
    def insertar(self, datos: List[Tuple]):
        """Limpia e inserta nuevos datos de forma eficiente."""
        self.limpiar()
        # Insertar en lote es más rápido en Tkinter moderno
        for dato in datos:
            self.tabla.insert(parent='', index=tk.END, values=dato)
    
    def limpiar(self):
        """Elimina todos los registros de la tabla."""
        self.tabla.delete(*self.tabla.get_children())

    def seleccionar(self) -> Optional[List[Any]]:
        """Devuelve los valores de la fila seleccionada."""
        seleccion = self.tabla.selection()
        if seleccion:
            return self.tabla.item(seleccion[0])["values"]
        return None
    
    def deseleccionar(self):
        """Quita la selección actual."""
        if self.tabla.selection():
            self.tabla.selection_remove(self.tabla.selection())