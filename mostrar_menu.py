import json

def seleccionar_tipo_PDF():
    while True:
        print('\nTipo de archivo PDF de facturas:')
        print('1. PDF tipo texto')
        print('2. PDF tipo imagen')
        print('3. Salir')

        try:
            opcion = int(input(f"Elige una opción (1-3): ").strip())
            if opcion == 1:
                is_PDF_texto = True
                return is_PDF_texto
            elif opcion == 2:
                is_PDF_texto = False
                return is_PDF_texto
            elif opcion == 3:
                print("\n👋 Saliendo del menú...\n")
                return None
            else:
                print("\n❌ Opción no válida. Inténtalo de nuevo.")
        except ValueError:
            print("\n⚠ Entrada no válida. Introduce un número válido.")

def cargar_opciones_json(ruta_json):
    """Carga las opciones desde un archivo JSON y verifica que tengan los campos necesarios.
    El formato debe ser el siguiente:
        {
            "1": {"nombre": "Pescadería Marengo", "nif": "33384986-A"},
            "2": {"nombre": "Pescadería Salvador", "nif": "25041071-M"}
        }
    """
    try:
        with open(ruta_json, "r", encoding="utf-8") as archivo:
            opciones = json.load(archivo)

        # Validar que cada opción tenga "nombre" y "nif"
        opciones_validas = {}
        for key, value in opciones.items():
            if isinstance(value, dict) and "nombre" in value and "nif" in value:
                opciones_validas[int(key)] = value  # Convertimos la clave a entero
            else:
                print(f'\n⚠ Advertencia: Opción "{key}" en el "{ruta_json}" no es válida y será ignorada.')
        return opciones_validas
    
    except FileNotFoundError:
        print(f'\n❌ Error: Archivo "{ruta_json}" no encontrado.\n')
        return
    except (json.JSONDecodeError, ValueError):
        print(f'\n❌ Error: El archivo "{ruta_json}" tiene un formato inválido.\n')
        return

def seleccionar_proveedor(ruta_json):
    """
    Muestra un menú de opciones leído desde un archivo JSON y devuelve 
    el nombre y NIF de la opción seleccionada. Si el usuario elige salir, 
    retorna (None, None).
    """
    opciones = cargar_opciones_json(ruta_json)

    if not opciones:
        return None, None

    while True:
        print("\nMenú de opciones:")
        for key, value in sorted(opciones.items()):  # Asegura que las opciones se muestren en orden
            print(f"{key}. {value['nombre']}")

        salida = max(opciones.keys()) + 1  # Calcula la opción de salida dinámicamente
        print(f"{salida}. Salir")

        try:
            opcion = int(input(f"Elige una opción (1-{salida}): ").strip())

            if opcion in opciones:
                nombre = opciones[opcion]["nombre"]
                nif = opciones[opcion]["nif"]
                print(f"\n✅ Has elegido: {nombre} ({nif})\n")
                return nombre, nif
            elif opcion == salida:  # Opción de salida
                print("\n👋 Saliendo del menú...\n")
                return None, None
            else:
                print("\n❌ Opción no válida. Inténtalo de nuevo.")
        except ValueError:
            print("\n⚠ Entrada no válida. Introduce un número válido.")

