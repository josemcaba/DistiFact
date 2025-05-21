import tkinter as tk
from tkinter import ttk, messagebox
import json

class DistiFactWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DistiFact")
        self.geometry("550x344")
        self.resizable(False, False)
        self.configure(bg="#1e1e2e")    # Fondo oscuro
        

class DistiFactApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.seleccion = None
        self.empresas = {}  # Para guardar todas las empresas cargadas

        self.estilos()
        self.crear_widgets()
        self.cargar_datos()

    def estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use('clam')

        # Estilo general de los widgets
        estilo.configure('TLabel', background="#1e1e2e", foreground="#ffffff", font=("Arial", 12))
        estilo.configure('TButton', background="#44475a", foreground="#ffffff", font=("Arial", 11, "bold"))
        estilo.map('TButton',
                   background=[('active', '#6272a4')],
                   foreground=[('active', '#ffffff')])

        # Estilo de la tabla
        estilo.configure('Treeview',
                         background="#2b2b40",
                         foreground="#f8f8f2",
                         fieldbackground="#2b2b40",
                         rowheight=30,
                         font=("Arial", 11))
        estilo.configure('Treeview.Heading',
                         background="#44475a",
                         foreground="#f8f8f2",
                         font=("Arial", 11, "bold"))

    def crear_widgets(self):
        # Título
        titulo = ttk.Label(self, text="DistiFact", font=("Arial", 24, "bold"))
        titulo.pack(pady=10)

        # Entrada de búsqueda
        frame_busqueda = ttk.Frame(self)
        frame_busqueda.pack(padx=40, pady=(5, 0), fill="both")

        label_busqueda = ttk.Label(frame_busqueda, text="Buscar: ")
        label_busqueda.pack(side="left")

        self.entry_busqueda = ttk.Entry(frame_busqueda)
        self.entry_busqueda.pack(side="left", fill="x", expand=True)
        self.entry_busqueda.bind("<KeyRelease>", self.buscar_empresas)

        # Frame para la tabla y el scrollbar
        frame_tabla = ttk.Frame(self)
        frame_tabla.pack(fill="both", expand=True, padx=40, pady=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # Tabla
        columnas = ("Id", "Empresa", "NIF")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", yscrollcommand=scrollbar.set, height=5)

        for col in columnas:
            self.tabla.heading(col, text=col)

        self.tabla.column("Id", anchor="center", width=75, stretch=False)
        self.tabla.column("Empresa", anchor="w", width=200, stretch=True)
        self.tabla.column("NIF", anchor="center", width=125, stretch=False)

        self.tabla.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=self.tabla.yview)

        # Botón seleccionar
        boton_seleccionar = ttk.Button(self, text="Seleccionar", command=self.confirmar_seleccion)
        boton_seleccionar.pack(pady=10)

    def cargar_datos(self):
        try:
            with open("empresas.json", "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)

            # Convertimos la key a entero
            self.empresas = {}  # Reiniciar datos
            for key, values in datos.items():
                self.empresas[int(key)] = values  

            for key, empresa in self.empresas.items():
                self.tabla.insert("", "end", values=(key, empresa["nombre"], empresa["nif"]))

            self.mostrar_empresas()

        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo empresas.json")
        except (json.JSONDecodeError):
            messagebox.showerror("Error", "El archivo empresas.json tiene un formato inválido")
        except (ValueError):
            messagebox.showerror("Error", "El archivo empresas.json tiene claves no numéricas.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los datos: {e}")
    
    def mostrar_empresas(self, filtro=""):
        # Limpiar tabla
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        # Insertar datos
        filtro = filtro.lower()
        for id_empresa, datos in self.empresas.items():
            nombre = datos["nombre"]
            nif = datos["nif"]
            if filtro in nombre.lower() or filtro in nif.lower() or filtro == "":
                self.tabla.insert("", "end", values=(id_empresa, nombre, nif))

    def buscar_empresas(self, event):
        texto = self.entry_busqueda.get()
        self.mostrar_empresas(filtro=texto)

    def confirmar_seleccion(self):
        seleccionado = self.tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Debe seleccionar una empresa.")
            return
        
        valores = self.tabla.item(seleccionado, "values")
        empresa_nombre = valores[1]
        messagebox.showinfo("Empresa seleccionada", f"Has seleccionado: {empresa_nombre}")

if __name__ == "__main__":
    app = DistiFactApp()
    app.mainloop()
