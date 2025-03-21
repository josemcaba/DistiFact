from ft_seleccionarEmpresa import seleccionarEmpresa
import ft_imagenes as fti
import fitz  # PyMuPDF
from ft_mensajes_POO import msg

def main():
    empresa, ruta_PDF = seleccionarEmpresa("empresas.json")
    if not(empresa and ruta_PDF):
        msg.salida()
        return

    rectangulos = fti.cargar_rectangulos_json(empresa["nif"])
    if not rectangulos:
        msg.salida()
        return
    angulo = rectangulos["angulo"]  
    
    with fitz.open(ruta_PDF) as pdf_doc:
        total_paginas = len(pdf_doc)
        for n_pag in range(total_paginas):
            imagen_pag = fti.extraer_imagen_de_la_pagina(pdf_doc, n_pag, angulo)
            imagenes = fti.extraer_imagenes_de_los_rectangulos(imagen_pag, rectangulos)
            msg.info(f"\n>>>>> Página {n_pag+1}")
            for imagen in imagenes:
                texto = fti.extraer_texto_de_imagen(imagen[0], imagen[1], verRectangulos=True)
    return

if __name__ == "__main__":
    main()
