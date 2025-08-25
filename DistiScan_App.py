import tkinter as tk
import tkinter.ttk as ttk # Importar el módulo ttk para usar widgets mejorados

# Crear y configurar la ventana principal
ventana = tk.Tk()
# ventana.geometry("600x600")
# ventana.minsize(600, 600)
ventana.title("DistiScan V1.0 - Distirel ©")
ventana.configure(background="#1d2d3d")
ventana.iconbitmap("recursos/Distirel.ico")

#

marco_titulo = ttk.Frame(ventana)
titulo = ttk.Label(marco_titulo,font=("Arial", 16, "bold"), foreground="#d1d2d3")
titulo.config(text="DistiScan - Procesador de Facturas")
titulo.pack()
marco_titulo.pack()


# titulo_principal.pack(pady=20)

# Creamos un separador
separador = ttk.Separator(ventana, orient="horizontal")
separador.pack(fill="x", padx=10)

ventana.mainloop()

# # Creamos una caja de texto
# caja_texto = ttk.Entry(ventana, font=("Arial", 10), width=50) # El ancho coincide con el umero de caracteres para el font seleccionado
# # caja_texto.pack(pady=20)

# # Extrae la info de la caja de texto
# def seleccionar_empresa():
#     empresa = caja_texto.get()
#     print(f"¡Empresa seleccionada: {empresa}!")
#     etiqueta.configure(text=f"bbbbb {empresa}")


# # Creamos botones
# boton_seleccionar = ttk.Button(ventana, text="Seleccionar", command=seleccionar_empresa)
# # boton_seleccionar.pack(pady=20)

# boton_salir = ttk.Button(ventana, text="Salir", command=ventana.quit)
# # boton_salir.pack(pady=20)

# etiqueta = ttk.Label(ventana, text="        ")
# # etiqueta.pack(pady=10)

# # DEfinicion de botones
# b1 = ttk.Button(ventana, text="Botón 1")
# b2 = ttk.Button(ventana, text="Botón 2")
# b3 = ttk.Button(ventana, text="Botón 3")

# # Configuracion del grid
# ventana.columnconfigure(0, weight=1)
# ventana.columnconfigure(1, weight=1)
# ventana.columnconfigure(2, weight=1)

# ventana.rowconfigure(0, weight=1)
# ventana.rowconfigure(1, weight=1)
# ventana.rowconfigure(2, weight=1)

# b1.grid(row=0, column=0, padx=20, pady=20, ipadx=20, ipady=20)
# b2.grid(row=0, column=1, sticky=tk.SE, ipadx=20, ipady=20)
# b3.grid(row=0, column=2, sticky=tk.NW)

# # Hacemos que la ventana principal se muestre
# ventana.mainloop()
