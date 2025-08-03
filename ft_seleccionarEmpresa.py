import json
import os
import ft_mensajes_POO as mensajes

msg = mensajes.Mensaje()

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
        msg.error(f'Archivo "{ruta_json}" no encontrado.')
        return
    except (json.JSONDecodeError):
        msg.error(f'El archivo "{ruta_json}" tiene un formato inválido.')
        return
    except (ValueError):
        msg.error(f'El archivo "{ruta_json}" tiene claves no numéricas.')
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
                msg.info(f"Has elegido {nombre} ({nif})\n")
                return empresas[opcion]
            elif opcion == 0:  # Opción de salida
                return None
            else:
                msg.error("Opción no válida. Inténtalo de nuevo.")
                
        except ValueError:
            msg.error("Entrada no válida. Introduce un número.")

def obtener_ruta_pdf(empresa):
    directorio = os.path.join("..", "DistiFact-Facturas", empresa['nombre'])
    if not os.path.exists(directorio):
        msg.error(f"El directorio '{directorio}' no existe.")
        return None
    
    while True:
        if empresa["tipo"] == "excel":
            nombre = input(f"Nombre del archivo Excel en directorio '{directorio}': ")
            if nombre and not nombre.endswith(".xlsx"):
                nombre += ".xlsx"
        else:
            nombre = input(f"Nombre del archivo PDF en directorio '{directorio}': ")
            if nombre and not nombre.endswith(".pdf"):
                nombre += ".pdf"
        
        if not nombre:
            msg.error("No se ha introducido ningun nombre de archivo.")
            return None
                   
        ruta = os.path.join(directorio, nombre)
        if os.path.isfile(ruta):
            return ruta
        else:
            msg.error(f"El archivo '{ruta}' no existe. Inténtelo de nuevo.\n")
    

def seleccionarEmpresa(ruta_json):
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
    datos_empresa, ruta_pdf = seleccionarEmpresa("empresas.json")
    if datos_empresa and ruta_pdf:
        msg.info(f"\nDatos empresa: {datos_empresa}")
        msg.info(f"Ruta al PDF: {ruta_pdf}\n")
