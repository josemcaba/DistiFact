"""
Módulo para unificar múltiples archivos PDF en uno solo.
"""
import os
from pathlib import Path
from typing import List, Tuple, Optional
import logging

# Intentar importar PyPDF2, si no está disponible, instálalo con: pip install PyPDF2
try:
    from PyPDF2 import PdfMerger, PdfReader
except ImportError:
    print("Error: PyPDF2 no está instalado. Instálalo con: pip install PyPDF2")
    raise

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UnificadorPDF:
    """Clase para unificar múltiples archivos PDF en uno solo."""
    
    @staticmethod
    def unificar_pdfs_en_directorio(
        directorio: str,
        nombre_salida: str = "merged.pdf",
        ordenar_por_nombre: bool = True,
        excluir_subdirectorios: bool = True
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Unifica todos los archivos PDF en un directorio en un solo archivo PDF.
        
        Args:
            directorio: Ruta del directorio que contiene los PDFs
            nombre_salida: Nombre del archivo de salida (por defecto: "merged.pdf")
            ordenar_por_nombre: Si True, ordena los PDFs alfabéticamente
            excluir_subdirectorios: Si True, solo busca PDFs en el directorio raíz
            
        Returns:
            Tuple[bool, str, Optional[str]]: 
                - Éxito (True/False)
                - Mensaje descriptivo
                - Ruta del archivo generado (si éxito) o None
        """
        try:
            # Verificar que el directorio existe
            if not os.path.isdir(directorio):
                return False, f"El directorio '{directorio}' no existe.", None
            
            # Buscar archivos PDF en el directorio
            if excluir_subdirectorios:
                # Solo archivos en el directorio raíz
                archivos = [f for f in os.listdir(directorio) 
                           if f.lower().endswith('.pdf') and 
                           os.path.isfile(os.path.join(directorio, f))]
            else:
                # Incluir subdirectorios
                archivos = []
                for root, dirs, files in os.walk(directorio):
                    for file in files:
                        if file.lower().endswith('.pdf'):
                            ruta_completa = os.path.join(root, file)
                            archivos.append(ruta_completa)
            
            # Verificar que hay al menos un PDF
            if not archivos:
                return False, f"No se encontraron archivos PDF en el directorio '{directorio}'.", None
            
            # Ordenar los archivos si se requiere
            if ordenar_por_nombre:
                if excluir_subdirectorios:
                    archivos.sort()
                else:
                    # Para rutas completas, ordenar por nombre de archivo
                    archivos.sort(key=lambda x: os.path.basename(x).lower())
            
            # Crear objeto PdfMerger
            merger = PdfMerger()
            
            # Contador para archivos procesados correctamente
            archivos_procesados = 0
            
            # Procesar cada archivo PDF
            for archivo in archivos:
                try:
                    ruta_archivo = archivo if excluir_subdirectorios else archivo
                    if excluir_subdirectorios:
                        ruta_archivo = os.path.join(directorio, archivo)
                    
                    # Verificar que el archivo existe
                    if not os.path.isfile(ruta_archivo):
                        logger.warning(f"El archivo no existe: {ruta_archivo}")
                        continue
                    
                    # Verificar que es un PDF válido
                    try:
                        with open(ruta_archivo, 'rb') as f:
                            reader = PdfReader(f)
                            if len(reader.pages) == 0:
                                logger.warning(f"PDF vacío: {ruta_archivo}")
                                continue
                    except Exception as e:
                        logger.warning(f"PDF inválido {ruta_archivo}: {str(e)}")
                        continue
                    
                    # Añadir el PDF al merger
                    merger.append(ruta_archivo)
                    archivos_procesados += 1
                    logger.info(f"Añadido: {ruta_archivo}")
                    
                except Exception as e:
                    logger.error(f"Error procesando {archivo}: {str(e)}")
                    continue
            
            # Verificar que se añadió al menos un archivo
            if archivos_procesados == 0:
                return False, "No se pudo procesar ningún archivo PDF válido.", None
            
            # Definir ruta de salida
            ruta_salida = os.path.join(directorio, nombre_salida)
            
            # Si el archivo de salida ya existe, añadir sufijo numérico
            contador = 1
            ruta_salida_final = ruta_salida
            while os.path.exists(ruta_salida_final):
                nombre_base, extension = os.path.splitext(nombre_salida)
                ruta_salida_final = os.path.join(
                    directorio, 
                    f"{nombre_base}_{contador}{extension}"
                )
                contador += 1
            
            # Guardar el PDF unido
            try:
                with open(ruta_salida_final, 'wb') as archivo_salida:
                    merger.write(archivo_salida)
                
                merger.close()
                
                mensaje = (f"Se unificaron {archivos_procesados} archivos PDF "
                          f"en '{ruta_salida_final}'.")
                
                logger.info(mensaje)
                return True, mensaje, ruta_salida_final
                
            except Exception as e:
                error_msg = f"Error al guardar el archivo unificado: {str(e)}"
                logger.error(error_msg)
                return False, error_msg, None
                
        except Exception as e:
            error_msg = f"Error inesperado durante la unificación: {str(e)}"
            logger.error(error_msg)
            return False, error_msg, None
    
    @staticmethod
    def unificar_pdfs_lista(
        lista_rutas: List[str],
        ruta_salida: str
    ) -> Tuple[bool, str]:
        """
        Unifica una lista específica de archivos PDF.
        
        Args:
            lista_rutas: Lista de rutas de archivos PDF
            ruta_salida: Ruta donde guardar el PDF unificado
            
        Returns:
            Tuple[bool, str]: Éxito y mensaje
        """
        try:
            # Verificar que hay archivos para procesar
            if not lista_rutas:
                return False, "La lista de archivos está vacía."
            
            # Crear objeto PdfMerger
            merger = PdfMerger()
            
            # Contador para archivos procesados
            archivos_procesados = 0
            
            # Procesar cada archivo
            for ruta in lista_rutas:
                try:
                    # Verificar que el archivo existe
                    if not os.path.isfile(ruta):
                        logger.warning(f"El archivo no existe: {ruta}")
                        continue
                    
                    # Verificar extensión PDF
                    if not ruta.lower().endswith('.pdf'):
                        logger.warning(f"No es un archivo PDF: {ruta}")
                        continue
                    
                    # Añadir el PDF al merger
                    merger.append(ruta)
                    archivos_procesados += 1
                    logger.info(f"Añadido: {ruta}")
                    
                except Exception as e:
                    logger.error(f"Error procesando {ruta}: {str(e)}")
                    continue
            
            # Verificar que se añadió al menos un archivo
            if archivos_procesados == 0:
                return False, "No se pudo procesar ningún archivo PDF válido."
            
            # Guardar el PDF unido
            with open(ruta_salida, 'wb') as archivo_salida:
                merger.write(archivo_salida)
            
            merger.close()
            
            mensaje = f"Se unificaron {archivos_procesados} archivos PDF en '{ruta_salida}'."
            logger.info(mensaje)
            return True, mensaje
            
        except Exception as e:
            error_msg = f"Error durante la unificación: {str(e)}"
            logger.error(error_msg)
            return False, error_msg


# Función de conveniencia para uso simple
def unificar_pdfs_directorio(
    directorio: str,
    nombre_salida: str = "merged.pdf"
) -> Tuple[bool, str, Optional[str]]:
    """
    Función simple para unificar PDFs en un directorio.
    
    Args:
        directorio: Ruta del directorio con PDFs
        nombre_salida: Nombre del archivo de salida
        
    Returns:
        Tuple[bool, str, Optional[str]]: Éxito, mensaje, ruta de salida
    """
    return UnificadorPDF.unificar_pdfs_en_directorio(directorio, nombre_salida)


if __name__ == "__main__":
    # Ejemplo de uso
    import sys
    
    if len(sys.argv) > 1:
        directorio = sys.argv[1]
    else:
        directorio = input("Ingrese la ruta del directorio con PDFs: ")
    
    resultado = unificar_pdfs_directorio(directorio)
    
    if resultado[0]:
        print(f"✓ {resultado[1]}")
        print(f"Archivo creado: {resultado[2]}")
    else:
        print(f"✗ {resultado[1]}")