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

    fe = import_module(empresa["funciones"][:-3])
    facturas_correctas, facturas_con_errores = fe.clasificar_facturas(facturas)
    if not (facturas_correctas or facturas_con_errores):
        print("\n👋 Saliendo del programa...\n")
        return

    excel_path=ruta_PDF.replace(".pdf", ".xlsx")
    fc.exportar_a_excel(facturas_correctas, facturas_con_errores, excel_path)

if __name__ == "__main__":
    main()
