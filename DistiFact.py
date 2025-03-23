from importlib import import_module    # Para importar un modulo almacenado en una variable
import ft_comunes as ftc
from ft_seleccionarEmpresa import seleccionarEmpresa
from ft_mensajes_POO import msg

def main():
    msg.info("\nBienvenido a DistiFact")
   
    empresa, ruta_PDF = seleccionarEmpresa("empresas.json")
    if not(empresa and ruta_PDF):
        msg.salida()
        return

    facturas = ftc.procesarFacturas(ruta_PDF, empresa)
    if not facturas:
        msg.salida()
        return

    fe = import_module(empresa["funciones"][:-3])
    facturas_correctas, facturas_con_errores = fe.clasificar_facturas(facturas)
    if not (facturas_correctas or facturas_con_errores):
        msg.salida()
        return

    excel_path=ruta_PDF.replace(".pdf", ".xlsx")
    ftc.exportar_a_excel(facturas_correctas, facturas_con_errores, excel_path)

if __name__ == "__main__":
    main()
