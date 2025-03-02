from importlib import import_module    # Para importar un modulo almacenado en una variable
import ft_comunes as ft
from ft_cargarDatosEmpresa import cargarDatosEmpresa

def main():
    empresa, ruta_PDF = cargarDatosEmpresa("empresas.json")
    if not(empresa and ruta_PDF):
        print("\n👋 Saliendo del programa...\n")
        return

    fe = import_module(empresa["funciones"][:-3])
    facturas = fe.extraer_facturas_del_PDF(ruta_PDF, empresa)
    if not facturas:
        print("\n👋 Saliendo del programa...\n")
        return

    facturas_correctas, facturas_con_errores = fe.clasificar_facturas(facturas)
    excel_path=ruta_PDF.replace(".pdf", ".xlsx")
    ft.exportar_a_excel(facturas_correctas, facturas_con_errores, excel_path)
    print()

if __name__ == "__main__":
    main()
    input('Finalizando ...')
