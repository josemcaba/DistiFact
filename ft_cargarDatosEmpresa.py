import json
import os

def cargar_empresas(ruta_json):
    try:
        with open(ruta_json, 'r', encoding='utf-8') as archivo:
            datos_json = json.load(archivo)

        # Convertimos la key a entero
        empresas = {}
        for key, values in datos_json.items():
            empresas[int(key)] = values  
        return empresas
    
    except FileNotFoundError:
        print(f'\n❌ Error: Archivo "{ruta_json}" no encontrado.')
        return
    except (json.JSONDecodeError):
        print(f'\n❌ Error: El archivo "{ruta_json}" tiene un formato inválido.')
        return
    except (ValueError):
        print(f'\n❌ Error: El archivo "{ruta_json}" tiene claves no numéricas.')
        return

def mostrar_menu(empresas):
    print("\n===== LISTADO DE EMPRESAS =====")
    for id_empresa, datos in sorted(empresas.items()):
        print(f"{id_empresa:>4}. {datos['nombre']} ({datos['nif']})")
    print(f"{0:>4}. Salir")

def seleccionar_empresa(empresas):
    while True:
        mostrar_menu(empresas)
        try:
            opcion = int(input("\nSeleccione una empresa: "))

            if opcion in empresas:
                nombre = empresas[opcion]["nombre"]
                nif = empresas[opcion]["nif"]
                print(f"\n✅ Has elegido {nombre} ({nif})\n")
                return empresas[opcion]
            elif opcion == 0:  # Opción de salida
                return None
            else:
                print("\n❌ Opción no válida. Inténtalo de nuevo.")

        except ValueError:
            print("\n⚠ Entrada no válida. Introduce un número.")

def obtener_ruta_pdf(empresa):
    directorio = empresa['nombre']
    if not os.path.exists(directorio):
        print(f"El directorio '{directorio}' no existe.")
        return None
    
    while True:
        nombre_pdf = input(f"Nombre del archivo PDF en directorio '{directorio}'): ")
        if nombre_pdf:
            if not nombre_pdf.endswith(".pdf"):
                nombre_pdf += ".pdf"
        else:
            print("No se ha introducido ningun nombre de archivo.")
            return None
        
        ruta_pdf = os.path.join(directorio, nombre_pdf)
        if os.path.isfile(ruta_pdf):
            return ruta_pdf
        else:
            print(f"El archivo '{ruta_pdf}' no existe. Inténtelo de nuevo.\n")
    

def cargarDatosEmpresa(ruta_json):
    empresas = cargar_empresas(ruta_json)
    if not empresas:
        return None, None
    
    empresa = seleccionar_empresa(empresas)
    if not empresa:
        return None, None
    
    ruta_pdf = obtener_ruta_pdf(empresa)
    if not ruta_pdf:
        return None, None    

    return (empresa, ruta_pdf)

if __name__ == "__main__":
    datos_empresa, ruta_pdf = cargarDatosEmpresa("empresas.json")
    if datos_empresa and ruta_pdf:
        print(f"\nDatos empresa: {datos_empresa}")
        print(f"Ruta al PDF: {ruta_pdf}\n")
