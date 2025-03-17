import json
import os
from ft_menu import Menu
from ft_mensajes import msg


def cargarEmpresas(ruta_json):
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

def obtener_ruta_pdf(empresa):
    directorio = empresa['nombre']
    if not os.path.exists(directorio):
        msg.error(f"El directorio '{directorio}' no existe.")
        return None
    
    while True:
        nombre_pdf = input(f"Nombre del archivo PDF en directorio '{directorio}': ")
        if nombre_pdf:
            if not nombre_pdf.endswith(".pdf"):
                nombre_pdf += ".pdf"
        else:
            msg.error("No se ha introducido ningun nombre de archivo.")
            return None
        
        ruta_pdf = os.path.join(directorio, nombre_pdf)
        if os.path.isfile(ruta_pdf):
            return ruta_pdf
        else:
            msg.error(f"El archivo '{ruta_pdf}' no existe. Inténtelo de nuevo.\n")
    

def seleccionarEmpresa(empresas):
    menu = Menu(empresas)
    empresa = menu.seleccionar()
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
