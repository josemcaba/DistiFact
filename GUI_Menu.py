import tkinter as tk
from tkinter import ttk, messagebox
from ft_mensajes import msg
import json

def cargarEmpresas(ruta_json):
    try:
        with open(ruta_json, 'r') as archivo:
            datos_json = json.load(archivo)

        # Convertimos la key a entero
        empresas = {}
        for key, values in datos_json.items():
            empresas[int(key)] = values  
        return empresas
    
    except FileNotFoundError:
        msg.error(f'Archivo "{ruta_json}" no encontrado.')
        return
    except (json.JSONDecodeError):
        msg.error(f'El archivo "{ruta_json}" tiene un formato inválido.')
        return
    except (ValueError):
        msg.error(f'El archivo "{ruta_json}" tiene claves no numéricas.')
        return

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
    # empresas1 = cargarEmpresas("empresas.json")
    # print(empresas1)
    
    empresas = {
        1: {"nombre": "Pescadería Marengo", "nif": "33384986A", "funciones": "_Pescaderias_Funciones.py", "tipoPDF": "texto"},
        2: {"nombre": "Pescadería Salvador", "nif": "25041071M", "funciones": "_Pescaderias_Funciones.py", "tipoPDF": "texto"},
        3: {"nombre": "Gregorio Aranda", "nif": "25693621E", "funciones": "_Gregorio_Funciones.py", "tipoPDF": "texto"},
        4: {"nombre": "Rosa Maria Moncayo", "nif": "25042336M", "funciones": "_Moncayo_Funciones.py", "tipoPDF": "texto"},
        5: {"nombre": "FACCSA", "nif": "A17001231", "funciones": "_FACCSA_Funciones.py", "tipoPDF": "imagen"},
        6: {"nombre": "ADISADI", "nif": "B93643245", "funciones": "_ADISADI_Funciones.py", "tipoPDF": "imagen"},
        7: {"nombre": "Ignacio Ibanez", "nif": "33360360X", "funciones": "_Ignacio_Funciones.py", "tipoPDF": "imagen"},
        8: {"nombre": "Gomez Moreno Mijas", "nif": "B92421601", "funciones": "_GOMEZMORENO_Funciones.py", "tipoPDF": "imagen"},
        9: {"nombre": "Antonio Osorio", "nif": "76753510A", "funciones": "_AntonioOsorio_Funciones.py", "tipoPDF": "imagen"}
    }
    print(empresas)

    
    app = MenuGUI(empresas)