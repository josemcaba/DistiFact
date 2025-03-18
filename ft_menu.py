from ft_mensajes import msg
import tkinter as tk
from tkinter import ttk, messagebox

# class MenuCLI:
#     def __init__(self, empresas):
#         self.empresas = empresas

#     def mostrar_menu(self):
#         print("\n===== LISTADO DE EMPRESAS =====")
#         for id, datos in sorted(self.empresas.items()):
#             print(f"{id:>3}. {datos['nombre']} ({datos['nif']})")
#         print(f"{0:>3}. Salir")

#     def seleccionar(self):
#         while True:
#             self.mostrar_menu()
#             try:
#                 opcion = int(input("\nSeleccione una empresa: "))

#                 if opcion in self.empresas:
#                     nombre = self.empresas[opcion]["nombre"]
#                     nif = self.empresas[opcion]["nif"]
#                     msg.info(f"\n✅ Has elegido {nombre} ({nif})\n")
#                     return self.empresas[opcion]
#                 elif opcion == 0:  # Opción de salida
#                     return None
#                 else:
#                     msg.error("Opción no válida. Inténtalo de nuevo.")
                    
#             except ValueError:
#                 msg.error("Entrada no válida. Introduce un número.")

class Menu: #GUI:
    def __init__(self, empresas):
        self.empresas = empresas
        self.root = tk.Tk()
        self.root.title("Seleccionar Empresa")
        
        ttk.Label(self.root, text="Seleccione una empresa:").pack(pady=10)
        
        self.empresa_var = tk.StringVar()
        self.combo_empresas = ttk.Combobox(self.root, textvariable=self.empresa_var, state="readonly")
        self.combo_empresas.pack(pady=5)
        
        lista_empresas = [f"{id}. {datos['nombre']}" for id, datos in sorted(self.empresas.items())]
        self.combo_empresas['values'] = lista_empresas
        
        self.boton_seleccionar = ttk.Button(self.root, text="Seleccionar", command=self.seleccionar)
        self.boton_seleccionar.pack(pady=10)

        self.boton_salir = ttk.Button(self.root, text="Salir", command=self.salir)
        self.boton_salir.pack(pady=5)
        
        self.root.mainloop()
        
    def seleccionar(self):
        seleccion = self.empresa_var.get()
        if seleccion:
            id_empresa = int(seleccion.split(".")[0])
            if id_empresa == 0:
                msg.salida()
                self.salir()
            else:
                empresa = self.empresas.get(id_empresa, None)
                if empresa:
                    msg.info(f"✅ Has elegido {empresa['nombre']} ({empresa['nif']})")
                    return empresa
        else:
            msg.error("Debe seleccionar una empresa.")
        return None
    
    def salir(self):
        self.root.quit()


