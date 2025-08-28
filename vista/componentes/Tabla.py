import tkinter as tk
from tkinter import ttk

class Tabla(tk.Frame):
	def __init__(self, parent):
		super().__init__(parent)
		self.columnconfigure(0, weight=1) # Columna para la tabla
		self.columnconfigure(1, weight=0) # Columna para la scrollbar vertical
		self.rowconfigure(0, weight=1)    # Columna para la tabla
		self.rowconfigure(1, weight=0)    # Columna para la scrollbar horizontal

		self.tabla = ttk.Treeview(self)
		self.tabla.grid(row=0, column=0, sticky="nsew")

		self.scrollbar_v = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tabla.yview)
		self.tabla.configure(yscrollcommand=self.scrollbar_v.set)
		self.scrollbar_v.grid(row=0, column=1, sticky="ns", pady=(27, 0))

		self.scrollbar_h = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tabla.xview)
		self.tabla.configure(xscrollcommand=self.scrollbar_h.set)
		self.scrollbar_h.grid(row=1, column=0, sticky="ew")

		self.estilo = ttk.Style()
		self.estilo.theme_use('clam')
		self.estilo.configure('Treeview', 
							background='#ffffee',      # Color de fondo de las celdas con datos
                         	fieldbackground='#ffffee', # Color de fondo de las celdas vacías							rowheight=30, 
							rowheight=26,
							font=('Arial', 12))        
		self.estilo.configure('Treeview.Heading', 
							background='#a6caf0', 
							font=('Arial', 10, 'bold'))
		self.estilo.map('Treeview', background=[('selected','#0078d7')])

	def cabecera(self, columnas):
        # Extraer solo los nombres de las columnas
		col_names = [col["nombre"] for col in columnas]
		self.tabla.configure(columns=col_names, show='headings')
        
        # Configurar cada columna con sus propiedades
		for columna in columnas:
			nombre = columna["nombre"]
			self.tabla.heading(nombre, text=nombre)
            
            # Configurar la columna con propiedades opcionales
			config = {
                "width": columna.get("ancho"),
                "anchor": columna.get("alineacion"),
                "stretch": columna.get("expandible"),
                "minwidth": columna.get("ancho")
            }
			# Filtrar configuraciones None (si alguna propiedad no está definida)
			config = {k: v for k, v in config.items() if v is not None}
			
			self.tabla.column(nombre, **config)
	
	def insertar(self, datos):
		for dato in datos:
			self.tabla.insert(parent='', index=tk.END, values=dato)
    
	def seleccionar(self):
		"""Devuelve los datos del elemento seleccionado"""
		seleccion = self.tabla.selection()
		if seleccion:
			return self.tabla.item(seleccion[0])["values"]
		return None
	
	def deseleccionar(self):
		"""Deselecciona el elemento seleccionado"""
		self.tabla.selection_set()
