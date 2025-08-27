import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from vista.componentes.Tabla import Tabla

class App(tk.Tk):
	def __init__(self):
		super().__init__()
		self._configurar_titulo()
		self._configurar_ventana()
		self._mostrar_tabla_empresas()
		self._crear_botones()

	def _configurar_ventana(self):
		self.title('Manejo de tabla')
		# self.geometry('688x600')
		# self.minsize(688,600)
		self.configure(background='#f0f0f0')
		# self.columnconfigure(0, weight=1)
		# self.rowconfigure(0, weight=0)
		# self.rowconfigure(1, weight=1)
		# self.rowconfigure(2, weight=0)

	def _configurar_titulo(self):
		marco_titulo = ttk.Label(self)
		marco_titulo.configure(text="DistiSCAN", background='green', foreground='white', font=('Arial', 15, 'bold'))
		# marco_titulo.columnconfigure(0, weight=1)
		marco_titulo.grid(row=0, column=0, sticky="nsew")

	def _mostrar_tabla_empresas(self):
		# Crear un marco contenedor para la tabla
		marco_tabla = ttk.Frame(self)
		marco_tabla.rowconfigure(0, weight=1)
		marco_tabla.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
		
		self.tabla_empresas = Tabla(marco_tabla)

		columnas = [
			{"ancho":  50, "alineacion": "c", "expandible": False, "nombre": "Núm."},
			{"ancho": 100, "alineacion": "c", "expandible": False, "nombre": "DNI/CIF"},
			{"ancho": 375, "alineacion": "w", "expandible": True,  "nombre": "Apellidos y Nombre o Razón Social"},
			{"ancho": 125, "alineacion": "w", "expandible": False, "nombre": "Tipo"}
		]
		self.tabla_empresas.cabecera(columnas)
		
		# Cargar datos de ejemplo
		self.cargar_datos_ejemplo()


	def _crear_botones(self):
		# Marco para los botones
		marco_botones = ttk.Frame(self)
		marco_botones.grid(row=2, column=0, sticky="e", padx=10, pady=5)
		
		# Botón para procesar la selección
		btn_procesar = ttk.Button(marco_botones, text="Procesar", 
									command=self.procesar_seleccion)
		btn_procesar.grid(row=0, column=0, ipady=15)
		
		# Centrar los botones
		# marco_botones.columnconfigure(0, weight=1)

	def cargar_datos_ejemplo(self):
		datos = (
			(575, '23645938F', 'ACIEGO ESCOBAR, MARIA JOSE', 'PDF Imagenes'), 
			(229, '36532215A', "ALAMINOS PEREZ, FRANCISCO JAVIER", 'Excel'),
			(123, '12345678A', "GARCÍA LÓPEZ, JUAN", 'Word'),
			(456, '87654321B', "MARTÍNEZ SÁNCHEZ, ANA", 'PDF'),
			(789, '11223344C', "RODRÍGUEZ FERNÁNDEZ, CARLOS", 'Excel')
		)
		datos = datos * 5  # Multiplicar para tener más datos
		self.tabla_empresas.insertar(datos)
		
	def procesar_seleccion(self):
		"""Ejemplo de cómo obtener y procesar la selección desde App"""
		seleccion = self.tabla_empresas.seleccionar()
		
		if seleccion:
			# Aquí puedes hacer cualquier procesamiento con los datos
			# Por ejemplo, enviarlos a una función de análisis, guardarlos, etc.
			
			# Simulamos un procesamiento externo
			resultado = self.analizar_datos_empresa(seleccion)
			print(resultado)
			
			showinfo("Procesamiento Externo", 
					f"Datos procesados externamente:\n\n{resultado}")
		else:
			showinfo("Información", "No hay ninguna fila seleccionada")

	def analizar_datos_empresa(self, datos_empresa):
		"""Función de ejemplo para procesar datos externamente"""
		numero, dni, nombre, tipo = datos_empresa
		
		# Aquí iría tu lógica de procesamiento real
		resultado = f"Empresa: {nombre}\n"
		resultado += f"Número: {numero}\n"
		resultado += f"DNI/CIF: {dni}\n"
		resultado += f"Tipo: {tipo}\n\n"
		resultado += "Análisis completado exitosamente"
		
		return resultado

if __name__ == "__main__":
    app = App()
    app.mainloop()