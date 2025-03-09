from importlib import import_module    # Para importar un modulo almacenado en una variable
import ft_comunes as fc
from ft_seleccionarEmpresa import seleccionarEmpresa

def main():
    empresa, ruta_PDF = seleccionarEmpresa("empresas.json")
    if not(empresa and ruta_PDF):
        print("\n👋 Saliendo del programa...\n")
        return

    facturas = fc.extraerFacturas(ruta_PDF, empresa)
    if not facturas:
        print("\n👋 Saliendo del programa...\n")
        return

if __name__ == "__main__":
    main()
