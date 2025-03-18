from importlib import import_module    # Para importar un modulo almacenado en una variable
import ft_comunes as fc
from ft_seleccionarEmpresa import seleccionarEmpresa
import mensajes_POO as mensajes

def main():
    msg = mensajes.Mensaje()
    msg.info("Bienvenido a DistiFact")
    msg.info("Este programa te ayudará a procesar facturas de diferentes empresas")
   
    empresa, ruta_PDF = seleccionarEmpresa("empresas.json")
    if not(empresa and ruta_PDF):
        msg.salida()
        return

    facturas = fc.procesarFacturas(ruta_PDF, empresa)
    if not facturas:
        msg.salida()
        return

    fe = import_module(empresa["funciones"][:-3])
    facturas_correctas, facturas_con_errores = fe.clasificar_facturas(facturas)
    if not (facturas_correctas or facturas_con_errores):
        msg.salida()
        return

    excel_path=ruta_PDF.replace(".pdf", ".xlsx")
    fc.exportar_a_excel(facturas_correctas, facturas_con_errores, excel_path)

if __name__ == "__main__":
    main()
