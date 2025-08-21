import tkinter as tk
from tkinter import ttk

class Tabla():
	def __init__(self, ventana):
		self.marco = ttk.Frame(ventana)
		self.marco.columnconfigure(0, weight=1) # Columna para la tabla
		self.marco.columnconfigure(1, weight=0) # Columna para la scrollbar
		self.marco.rowconfigure(0, weight=1)
		self.marco.grid(row=0, column=0, sticky="nsew")

		self._agregar_tabla()
		self._definir_estilo()
		self._agregar_scrollbar()

	def _definir_estilo(self):
		self.estilo = ttk.Style()
		self.estilo.theme_use('clam')
		self.estilo.configure('Treeview', background='#ffffee', rowheight=30, font=('Arial', 10, 'bold'))
		self.estilo.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
		self.estilo.map('Treeview', background=[('selected','#0078d7')])

	def _agregar_tabla(self):
		self.tabla = ttk.Treeview(self.marco)
		self.tabla.grid(row=0, column=0, sticky="nsew")
	

	def _agregar_scrollbar(self):
		self.scrollbar = ttk.Scrollbar(self.marco, orient=tk.VERTICAL, command=self.tabla.yview)
		self.tabla.configure(yscroll=self.scrollbar.set)
		self.scrollbar.grid(row=0, column=1, sticky="ns")

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




if __name__ == "__main__":
	ventana = tk.Tk()
	ventana.geometry('700x600')
	ventana.configure(background='#f0f0f0')
	ventana.title=('Manejo de tabla')
	ventana.columnconfigure(0, weight=1)



	tabla_empresas = Tabla(ventana)
	columnas = [
		{"ancho": 50,  "alineacion": "c", "expandible": False, "nombre": "Num."},
		{"ancho": 100,  "alineacion": "c", "expandible": False, "nombre": "DNI/CIF"},
		{"ancho": 375, "alineacion": "w", "expandible": True,  "nombre": "Apellidos y Nombre o Razón Social"},
		{"ancho": 125, "alineacion": "w", "expandible": False,  "nombre": "Tipo"}
	]
	tabla_empresas.cabecera(columnas)
	datos = ((575, '23645938F', 'ACIEGO ESCOBAR, MARIA JOSE', 'PDF Imagenes'), (229, '36532215A', "ALAMINOS PEREZ,FRANCISCO JAVIER", 'Excel')) # Tupla de tuplas
	datos = datos + datos + datos + datos + datos + datos + datos + datos + datos + datos + datos
	tabla_empresas.insertar(datos)

	ventana.mainloop()