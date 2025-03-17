import tkinter as tk
from tkinter import ttk, messagebox

class MenuGUI:
    def __init__(self, empresas):
        self.empresas = empresas
        self.root = tk.Tk()
        self.root.title("Seleccionar Empresa")
        
        ttk.Label(self.root, text="Seleccione una empresa:").pack(pady=10)
        
        self.empresa_var = tk.StringVar()
        self.combo_empresas = ttk.Combobox(self.root, textvariable=self.empresa_var, state="readonly")
        self.combo_empresas.pack(pady=5)
        
        # Agregar la opción "Salir" al combobox
        lista_empresas = ["0. Salir"] + [f"{id}. {datos['nombre']}" for id, datos in sorted(self.empresas.items())]
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
                self.salir()
            else:
                empresa = self.empresas.get(id_empresa, None)
                if empresa:
                    messagebox.showinfo("Selección", f"✅ Has elegido {empresa['nombre']} ({empresa['nif']})")
                    return empresa  # Devuelve la empresa seleccionada
        else:
            messagebox.showerror("Error", "Debe seleccionar una empresa.")
        return None  # Si no se selecciona nada
    
    def salir(self):
        self.root.quit()

# Ejemplo de uso
if __name__ == "__main__":
    empresas = {
        1: {"nombre": "Empresa A", "nif": "A12345678"},
        2: {"nombre": "Empresa B", "nif": "B87654321"},
        3: {"nombre": "Empresa C", "nif": "C12348765"}
    }
    
    app = MenuGUI(empresas)