"""
Módulo que contiene la clase FrameSeleccionArchivo para seleccionar un archivo.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
from typing import Dict, Any, Optional

from vista.frame_base import FrameBase


class FrameSeleccionArchivo(FrameBase):
    """
    Frame para seleccionar un archivo a procesar.
    """
    nombre = "seleccion_archivo"
    
    def _obtener_titulo(self) -> str:
        """Retorna el título del frame."""
        return "Selección de Archivo"
    
    def _inicializar_componentes(self):
        """Inicializa los componentes del frame."""
        super()._inicializar_componentes()
        
        # Contenedor principal
        self.frame_contenido = ttk.Frame(self)
        self.frame_contenido.pack(fill="both", expand=True)
        
        # Contenedor para empresa seleccionada y botón de unificar
        self.frame_empresa_superior = ttk.Frame(self.frame_contenido)
        self.frame_empresa_superior.pack(fill="x", padx=5, pady=(10, 5))
        
        # Frame para información de la empresa (izquierda)
        self.frame_empresa_info = ttk.Frame(self.frame_empresa_superior)
        self.frame_empresa_info.pack(side="left", fill="x", expand=True)
        
        self.lbl_empresa_titulo = ttk.Label(
            self.frame_empresa_info,
            text="Empresa seleccionada:"
        )
        self.lbl_empresa_titulo.pack(anchor="w")

        self.lbl_empresa_info = ttk.Label(
            self.frame_empresa_info,
            text="",
            relief="solid", 
            padding=5,
        )
        self.lbl_empresa_info.pack(anchor="w", pady=(5, 0), padx=(0, 5))
        
        # Frame para botón de unificar PDFs (derecha)
        self.frame_boton_unificar = ttk.Frame(self.frame_empresa_superior)
        self.frame_boton_unificar.pack(side="right", padx=(0, 5), pady=(25, 0))
        
        # Botón para unificar PDFs (no se empaqueta aquí, se mostrará según tipo de empresa)
        self.btn_unificar = ttk.Button(
            self.frame_boton_unificar,
            text="Unificar PDFs",
            command=self._on_unificar_pdfs
        )
        # No se empaqueta aquí, se mostrará solo si la empresa NO es "excel"
        
        # Separador horizontal
        separador = ttk.Separator(self.frame_contenido, orient="horizontal")
        separador.pack(fill='x', padx=5, pady=5)

        # Selección de archivo
        self.frame_archivo = ttk.Frame(self.frame_contenido)
        self.frame_archivo.pack(fill="x", padx=5, pady=5)
        
        self.lbl_archivo = ttk.Label(
            self.frame_archivo,
            text="Archivo a procesar:"
        )
        self.lbl_archivo.pack(anchor="w", pady=(0, 5))
        
        # Frame para entrada y botón
        self.frame_entrada = ttk.Frame(self.frame_archivo)
        self.frame_entrada.pack(fill="x", pady=5)

        self.btn_examinar = ttk.Button(
            self.frame_entrada,
            text="Examinar",
            command=self._on_examinar
        )
        self.btn_examinar.pack(side="left")
        
        self.entry_ruta = ttk.Entry(
            self.frame_entrada,
            # width=50
        )
        self.entry_ruta.pack(side="right", fill="x", expand=True, padx=(10, 0))
        
        # Frame para botones de acción
        self.frame_botones_accion = ttk.Frame(self.frame_contenido)
        self.frame_botones_accion.pack(fill="x", padx=5, pady=10)

        # Botón para crear rectángulos (solo visible para PDF imagen)
        self.btn_crear = ttk.Button(
            self.frame_botones_accion,
            text="Crear rectángulos",
            command=self._on_crear_rectangulos
        )
        # No se empaqueta aquí, se mostrará solo si es PDF imagen
        
        # Botón para visualizar rectángulos (solo visible para PDF imagen)
        self.btn_visualizar = ttk.Button(
            self.frame_botones_accion,
            text="Ver rectángulos",
            command=self._on_visualizar_rectangulos
        )
        # No se empaqueta aquí, se mostrará solo si es PDF imagen
        
        # Frame para botones de navegación (a la derecha)
        self.frame_botones_nav = ttk.Frame(self.frame_botones_accion)
        self.frame_botones_nav.pack(side="right")
        
        # Botón de procesar
        self.btn_procesar = ttk.Button(
            self.frame_botones_nav,
            text="Procesar",
            command=self._on_procesar
        )
        self.btn_procesar.pack(side="right", padx=5)
        
        # Botón de volver
        self.btn_volver = ttk.Button(
            self.frame_botones_nav,
            text="Volver",
            command=lambda: self.app.mostrar_frame("seleccion_empresa")
        )
        self.btn_volver.pack(side="right", padx=5)
    
    def inicializar(self):
        """Inicializa el frame cuando se muestra."""
        # Obtener información de la empresa seleccionada
        empresa = self.controlador.obtener_empresa_actual()
        
        if not empresa:
            self.mostrar_mensaje("error", "No hay empresa seleccionada.")
            self.app.mostrar_frame("seleccion_empresa")
            return
        
        # Mostrar información de la empresa
        self.lbl_empresa_info.config(
            text=f"{empresa.nombre} ({empresa.nif}) - Tipo: {empresa.tipo}"
        )
        
        # Mostrar u ocultar botones según tipo de empresa
        if empresa.tipo == "PDFimagen":
            self.btn_visualizar.pack(side="left", padx=5)
            self.btn_crear.pack(side="left", padx=5)
        else:
            self.btn_visualizar.pack_forget()
            self.btn_crear.pack_forget()
        
        # Mostrar u ocultar botón de unificar PDFs
        # Solo se muestra si la empresa NO es de tipo "excel"
        if empresa.tipo != "excel":
            self.btn_unificar.pack(side="right")
        else:
            self.btn_unificar.pack_forget()
        
        # Limpiar campo de ruta
        self.entry_ruta.delete(0, tk.END)
    
    def _on_examinar(self):
        """Maneja el evento de examinar archivo."""
        empresa = self.controlador.obtener_empresa_actual()
        
        if not empresa:
            return
        
        # Determinar tipo de archivo según el tipo de empresa
        if empresa.tipo == "excel":
            tipos_archivo = [("Archivos Excel", "*.xlsx;*.xls")]
        else:
            tipos_archivo = [("Archivos PDF", "*.pdf")]
        
        # Mostrar diálogo de selección
        ruta = self.app.seleccionar_archivo(
            tipos_archivo=tipos_archivo,
            titulo=f"Seleccionar archivo para {empresa.nombre}"
        )
        
        if ruta:
            self.entry_ruta.delete(0, tk.END)
            self.entry_ruta.insert(0, ruta)
    
    def _on_visualizar_rectangulos(self):
        """Maneja el evento de visualizar rectángulos."""
        # Obtener ruta del archivo
        ruta = self.entry_ruta.get().strip()
        
        if not ruta:
            self.mostrar_mensaje("warning", "Debe seleccionar un archivo PDF.")
            return
        
        if not os.path.isfile(ruta):
            self.mostrar_mensaje("error", f"El archivo '{ruta}' no existe.")
            return
        
        if not ruta.lower().endswith(".pdf"):
            self.mostrar_mensaje("error", "El archivo debe ser un PDF.")
            return
        
        # Obtener empresa actual
        empresa = self.controlador.obtener_empresa_actual()

        # Visualizar rectángulos
        self.controlador.visualizar_rectangulos(ruta, empresa.to_dict())

    def _on_crear_rectangulos(self):
        """Maneja el evento de crear rectángulos."""
        ruta = self.entry_ruta.get().strip()
    
        if not ruta:
            self.mostrar_mensaje("warning", "Debe seleccionar un archivo PDF.")
            return
    
        if not os.path.isfile(ruta):
            self.mostrar_mensaje("error", f"El archivo '{ruta}' no existe.")
            return
    
        if not ruta.lower().endswith(".pdf"):
            self.mostrar_mensaje("error", "El archivo debe ser un PDF.")
            return
    
        empresa = self.controlador.obtener_empresa_actual()
    
        # Llamar al controlador para crear los rectángulos
        self.controlador.crear_rectangulos(ruta, empresa.to_dict())
    
    def _on_unificar_pdfs(self):
        """Maneja el evento de unificar PDFs."""
        try:
            # Pedir al usuario que seleccione un directorio
            directorio = self.app.seleccionar_directorio(
                titulo="Seleccionar directorio con PDFs a unificar"
            )
            
            if not directorio:
                return  # El usuario canceló
            
            # Verificar que el directorio existe
            if not os.path.isdir(directorio):
                self.mostrar_mensaje("error", f"El directorio '{directorio}' no existe.")
                return
            
            # Llamar al controlador para unificar los PDFs
            resultado = self.controlador.unificar_pdfs(directorio)
            
            # Mostrar mensaje de resultado usando el mismo estilo de la aplicación
            if resultado["exito"]:
                mensaje = resultado["mensaje"]
                if resultado.get("ruta_salida"):
                    mensaje += f"\n\nArchivo generado: {resultado.get('ruta_salida')}"
                self.mostrar_mensaje("info", mensaje, titulo="Operación completada")
            else:
                self.mostrar_mensaje("error", resultado["mensaje"], titulo="Error en la operación")
                
        except Exception as e:
            self.mostrar_mensaje("error", f"Error inesperado: {str(e)}", titulo="Error")
        
    def _on_procesar(self):
        """Maneja el evento de procesar archivo."""
        # Obtener ruta del archivo
        ruta = self.entry_ruta.get().strip()
        
        if not ruta:
            self.mostrar_mensaje("warning", "Debe seleccionar un archivo.")
            return
        
        if not os.path.isfile(ruta):
            self.mostrar_mensaje("error", f"El archivo '{ruta}' no existe.")
            return
        
        # Verificar extensión según tipo de empresa
        empresa = self.controlador.obtener_empresa_actual()
        
        if empresa.tipo in ["PDFtexto", "PDFimagen"] and not ruta.lower().endswith(".pdf"):
            self.mostrar_mensaje("error", "El archivo debe ser un PDF.")
            return
        
        if empresa.tipo == "excel" and not ruta.lower().endswith((".xlsx", ".xls")):
            self.mostrar_mensaje("error", "El archivo debe ser un Excel.")
            return
        
        # Establecer ruta en el controlador
        self.controlador.establecer_ruta_archivo(ruta)
        
        # Avanzar al frame de procesamiento
        self.app.mostrar_frame("procesamiento")