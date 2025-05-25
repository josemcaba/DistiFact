"""
Módulo que contiene la clase ProcesadorFacturas para procesar archivos de facturas.
"""
from importlib import import_module
import pdfplumber
import fitz  # PyMuPDF
import openpyxl
import sys
import os
from typing import List, Dict, Any, Tuple, Optional, Callable

# Importamos módulos del proyecto
from modelo.factura import Factura
from modelo.empresa import Empresa

class ProcesadorFacturas:
    """
    Clase que procesa archivos de facturas en diferentes formatos.
    """
    def __init__(self):
        """Inicializa el procesador de facturas."""
        self._progreso_callback = None
        self._mensaje_callback = None
    
    def set_callbacks(self, progreso_callback: Callable[[int, int], None], 
                     mensaje_callback: Callable[[str, str], None]) -> None:
        """
        Establece las funciones de callback para reportar progreso y mensajes.
        
        Args:
            progreso_callback: Función para reportar progreso (página actual, total)
            mensaje_callback: Función para mostrar mensajes (tipo, mensaje)
        """
        self._progreso_callback = progreso_callback
        self._mensaje_callback = mensaje_callback
    
    def _mostrar_mensaje(self, tipo: str, mensaje: str) -> None:
        """
        Muestra un mensaje usando el callback si está disponible.
        
        Args:
            tipo: Tipo de mensaje ('info', 'error')
            mensaje: Contenido del mensaje
        """
        if self._mensaje_callback:
            self._mensaje_callback(tipo, mensaje)
        else:
            print(f"{tipo.upper()}: {mensaje}")
    
    def _actualizar_progreso(self, actual: int, total: int) -> None:
        """
        Actualiza el progreso usando el callback si está disponible.
        
        Args:
            actual: Página o elemento actual
            total: Total de páginas o elementos
        """
        if self._progreso_callback:
            self._progreso_callback(actual, total)
        else:
            sys.stdout.write(f'\rProcesando: {actual}/{total}')
            sys.stdout.flush()
    
    def procesar_archivo(self, ruta_archivo: str, empresa: Empresa) -> List[Factura]:
        """
        Procesa un archivo según el tipo de empresa.
        
        Args:
            ruta_archivo: Ruta al archivo a procesar
            empresa: Instancia de Empresa con la configuración
            
        Returns:
            Lista de facturas procesadas
        """
        if not os.path.exists(ruta_archivo):
            self._mostrar_mensaje('error', f'El archivo "{ruta_archivo}" no existe.')
            return []
        
        try:
            # Carga el módulo de funciones extractoras correspondientes a la empresa
            modulo_nombre = empresa.funciones[:-3]  # Quitamos la extensión .py
            fe = import_module(modulo_nombre)
        except ImportError:
            self._mostrar_mensaje('error', f'No existe el módulo "{empresa.funciones}"')
            return []
        
        # Procesamos según el tipo de archivo
        if empresa.tipo == "PDFtexto":
            paginas = self._procesar_pdf_texto(ruta_archivo, fe.identificador)
        elif empresa.tipo == "PDFimagen":
            paginas = self._procesar_pdf_imagen(ruta_archivo, fe.identificador, empresa.nif)
        elif empresa.tipo == "excel":
            paginas = self._procesar_excel(ruta_archivo, fe.identificador, empresa.nif)
        else:
            self._mostrar_mensaje('error', f'Tipo de archivo "{empresa.tipo}" no válido')
            return []
        
        if not paginas:
            return []
        
        # Extraemos los datos de cada página
        facturas = []
        for pagina in paginas:
            try:
                # Verificar que pagina sea una lista con al menos 2 elementos
                if not isinstance(pagina, list) or len(pagina) < 2:
                    self._mostrar_mensaje('error', f'Estructura de página/fila inválida: {pagina}')
                    continue
                
                num_pagina = pagina[0]
                texto = pagina[1]
                
                # Usamos el extractor específico de la empresa
                try:
                    datos_factura = fe.extraerDatosFactura(pagina, empresa.to_dict())
                    
                    if datos_factura:
                        # Asegurarse de que datos_factura tenga la estructura correcta
                        if isinstance(datos_factura, list) and len(datos_factura) >= 2:
                            if isinstance(datos_factura[1], dict):
                                factura = Factura(datos_factura[0], datos_factura[1])
                                facturas.append(factura)
                            else:
                                self._mostrar_mensaje('error', f'datos_factura[1] no es un diccionario: {type(datos_factura[1])}')
                        else:
                            # Si no es una lista, intentar crear la factura directamente
                            factura = Factura(num_pagina, datos_factura)
                            facturas.append(factura)
                except Exception as e:
                    self._mostrar_mensaje('error', f'Error en extractor: {str(e)}')
            except Exception as e:
                self._mostrar_mensaje('error', f'Error procesando página/fila: {str(e)}')
        
        if not facturas:
            self._mostrar_mensaje('error', f'El archivo "{ruta_archivo}" no contiene facturas')
        
        return facturas
    
    def _procesar_pdf_texto(self, ruta_pdf: str, identificador: str) -> List[List]:
        """
        Procesa un PDF de tipo texto.
        
        Args:
            ruta_pdf: Ruta al archivo PDF
            identificador: Cadena para identificar páginas relevantes
            
        Returns:
            Lista de páginas procesadas [num_pagina, texto]
        """
        paginas = []
        paginas_descartadas = []
        
        try:
            with pdfplumber.open(ruta_pdf) as pdf:
                total_paginas = len(pdf.pages)
                
                for n_pag, pagina in enumerate(pdf.pages, start=1):
                    self._actualizar_progreso(n_pag, total_paginas)
                    texto = pagina.extract_text()
                    
                    if texto and identificador in texto:
                        paginas.append([n_pag, texto])
                    else:
                        paginas_descartadas.append(str(n_pag))
                
                self._mostrar_mensaje('info', f'Procesadas {total_paginas} páginas')
                if paginas_descartadas:
                    self._mostrar_mensaje('info', f"Páginas descartadas: {' - '.join(paginas_descartadas)}")
                
                return paginas
        except Exception as e:
            self._mostrar_mensaje('error', f'Error al procesar PDF: {str(e)}')
            return []
    
    def _procesar_pdf_imagen(self, ruta_pdf: str, identificador: str, nif: str) -> List[List]:
        """
        Procesa un PDF de tipo imagen.
        
        Args:
            ruta_pdf: Ruta al archivo PDF
            identificador: Cadena para identificar páginas relevantes
            nif: NIF de la empresa para cargar los rectángulos
            
        Returns:
            Lista de páginas procesadas [num_pagina, texto]
        """
        # Importamos aquí para evitar dependencias circulares
        import ft_imagenes as fci
        
        rectangulos = fci.cargar_rectangulos_json(nif, ruta_json="rectangulos.json")
        if not rectangulos:
            self._mostrar_mensaje('error', f'No se encontraron rectángulos para el NIF {nif}')
            return []
        
        angulo = rectangulos["angulo"]
        paginas = []
        paginas_descartadas = []
        
        try:
            with fitz.open(ruta_pdf) as pdf_doc:
                total_paginas = len(pdf_doc)
                
                for n_pag in range(total_paginas):
                    self._actualizar_progreso(n_pag + 1, total_paginas)
                    
                    imagen_pag = fci.extraer_imagen_de_la_pagina(pdf_doc, n_pag, angulo)
                    imagenes = fci.extraer_imagenes_de_los_rectangulos(imagen_pag, rectangulos)
                    texto = fci.extraer_texto_de_las_imagenes(imagenes, verRectangulos=False)
                    
                    if texto and identificador in texto:
                        paginas.append([n_pag + 1, texto])
                    else:
                        paginas_descartadas.append(str(n_pag + 1))
                
                self._mostrar_mensaje('info', f'Procesadas {total_paginas} páginas')
                if paginas_descartadas:
                    self._mostrar_mensaje('info', f"Páginas descartadas: {' - '.join(paginas_descartadas)}")
                
                return paginas
        except Exception as e:
            self._mostrar_mensaje('error', f'Error al procesar PDF imagen: {str(e)}')
            return []
    
    def _procesar_excel(self, ruta_excel: str, identificador: str, nif: str) -> List[List]:
        """
        Procesa un archivo Excel.
        
        Args:
            ruta_excel: Ruta al archivo Excel
            identificador: Cadena para identificar filas relevantes (no se usa en Excel)
            nif: NIF de la empresa
            
        Returns:
            Lista de filas procesadas [num_fila, texto_o_datos]
            donde texto_o_datos es un string o diccionario con los datos de la fila
        """
        try:
            # Cargar el libro de trabajo
            libro = openpyxl.load_workbook(ruta_excel, data_only=True)
            
            # Seleccionar la primera hoja
            hoja = libro.active
            
            # Obtener encabezados (primera fila)
            # encabezados = []
            # for celda in hoja[1]:
            #     encabezados.append(str(celda.value) if celda.value is not None else "")
            
            filas = []
            contador = 2  # Inicializamos el contador (asumiendo que la primera fila es encabezado)
            
            # Obtener el total de filas para el progreso
            max_row = hoja.max_row
            
            # Iterar sobre todas las filas con contenido
            for i, fila in enumerate(hoja.iter_rows(min_row=2, values_only=True), start=2):
                self._actualizar_progreso(i, max_row)
                
                try:
                    # Filtrar filas completamente vacías (todas las celdas son None)
                    if any(celda is not None for celda in fila):
                        # Crear una nueva lista que comience con el contador
                        fila = [contador] + list(fila)
                        filas.append(fila)
                        contador += 1  # Incrementar el contador
                except Exception as e:
                    self._mostrar_mensaje('error', f'Error procesando fila {i}: {str(e)}')
                    # Continuar con la siguiente fila en caso de error
            
            self._mostrar_mensaje('info', f'Procesadas {contador-2} filas de Excel')
            return filas
            
        except Exception as e:
            self._mostrar_mensaje('error', f'Error al procesar Excel: {str(e)}')
            return []
