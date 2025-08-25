import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning
from vista.frameTabla import Tabla

class SeleccionarEmpresa(tk.Frame):
	def __init__(self, parent, app, controlador):
		super().__init__(parent)
		self.app = app
		self.controlador = controlador
		self._configurar_frame()
		self._configurar_titulo()
		self._mostrar_tabla_empresas()
		self._crear_botones()

	def _configurar_frame(self):
        # Configure the frame itself to expand
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=0)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=0)

	def _configurar_titulo(self):
		marco_titulo = ttk.Label(self)
		marco_titulo.grid(row=0, column=0, sticky="ew")
		marco_titulo.configure(text="DistiSCAN - Selección de Empresa", foreground='white', font=('Arial', 15, 'bold'))

	def _mostrar_tabla_empresas(self):
		# Crear un marco contenedor para la tabla		
		self.tabla_empresas = Tabla(self)
		self.tabla_empresas.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

		columnas = [
			{"ancho":  50, "alineacion": "c", "expandible": False, "nombre": "Núm."},
			{"ancho": 100, "alineacion": "c", "expandible": False, "nombre": "DNI/CIF"},
			{"ancho": 275, "alineacion": "w", "expandible": True,  "nombre": "Apellidos y Nombre o Razón Social"},
			{"ancho": 125, "alineacion": "w", "expandible": False, "nombre": "Tipo"}
		]
		self.tabla_empresas.cabecera(columnas)
		
		# Cargar datos de empresas
		empresas = self.controlador.cargar_empresas('empresas.json')
		if not empresas:
			# self.mostrar_mensaje("error", "No se pudieron cargar las empresas.")
			showerror("Error", f"No se puede cargar el archivo 'empresas.json'")
			return
		self.tabla_empresas.insertar(empresas)

	def _crear_botones(self):	# Marco para los botones
		marco_botones = ttk.Frame(self)
		marco_botones.grid(row=2, column=0, sticky="e", padx=10, pady=5)
		
		# Botón para procesar la selección
		btn_procesar = ttk.Button(marco_botones, text="Seleccionar", 
									command=self._on_seleccionar)
		btn_procesar.grid(row=0, column=0, ipady=10, padx=10)
		
		# Botón de salir
		self.btn_salir = ttk.Button(marco_botones, text="Salir",
									command=self.app.quit)
		self.btn_salir.grid(row=0, column=1, ipady=10)
	
	def _on_seleccionar(self):
		seleccion = self.tabla_empresas.seleccionar()
		
		if not seleccion:
			showwarning("Atención", "Debe seleccionar una empresa.")
			return

		self.controlador.seleccionar_empresa(seleccion[0])
		self.tabla_empresas.deseleccionar()
		# self.destroy()
		# self.grid_remove()
		# self.grid()
	

