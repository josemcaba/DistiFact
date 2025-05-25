from ft_seleccionarEmpresa import seleccionarEmpresa
from ft_procesarFacturas import procesarFacturas
from ft_clasificarFacturas import clasificarFacturas
from ft_exportarExcel import exportar_a_excel
from ft_mensajes_POO import msg

def main():
    msg.info("\nBienvenido a DistiFact")
   
    empresa, ruta_PDF = seleccionarEmpresa("empresas.json")
    if not(empresa and ruta_PDF):
        msg.salida()
        return

    facturas = procesarFacturas(ruta_PDF, empresa)
    if not facturas:
        msg.salida()
        return

    facturas_correctas, facturas_con_errores = clasificarFacturas(facturas)
    if not (facturas_correctas or facturas_con_errores):
        msg.salida()
        return

    excel_path=ruta_PDF.replace(".pdf", ".xlsx")
    exportar_a_excel(facturas_correctas, facturas_con_errores, excel_path)

if __name__ == "__main__":
    main()
