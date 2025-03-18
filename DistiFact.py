from importlib import import_module    # Para importar un modulo almacenado en una variable
import ft_comunes as fc
from ft_seleccionarEmpresa import cargarEmpresas, seleccionarEmpresa
from ft_mensajes import msg
import tkinter as tk
from tkinter import ttk

def main():
    empresas = cargarEmpresas("empresas.json")
    if not empresas:
        return

    empresa, ruta_PDF = seleccionarEmpresa(empresas)
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