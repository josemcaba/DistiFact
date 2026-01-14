from tkinter import ttk
import extractores.conceptos_factura as KEY
from vista.frame_base import FrameBase
from vista.Tabla import Tabla

class FrameResultados(FrameBase):
    nombre = "resultados"
    
    def _obtener_titulo(self) -> str:
        return "Resultados del Procesamiento"
    
    def _inicializar_componentes(self):
        super()._inicializar_componentes()
        
        # Crear cabecera con información de empresa (sin botón)
        self._crear_cabecera_empresa(mostrar_boton=False)
        
        self.frame_contenido = ttk.Frame(self)
        self.frame_contenido.pack(fill="both", expand=True)
        
        self.notebook = ttk.Notebook(self.frame_contenido)
        self.notebook.pack(fill="both", expand=True, pady=10)
        
        # Configuración de tablas
        self.tab_correctas = ttk.Frame(self.notebook)
        self.tab_errores = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_correctas, text="Facturas Correctas")
        self.notebook.add(self.tab_errores, text="Facturas con Errores")
        
        col_base = self._obtener_columnas_base()
        
        self.tabla_correctas = self._crear_tabla(self.tab_correctas, col_base + [
            {"nombre": "Observaciones", "ancho": 150, "alineacion": "w", "expandible": True}
        ])
        
        self.tabla_errores = self._crear_tabla(self.tab_errores, col_base + [
            {"nombre": "Errores", "ancho": 150, "alineacion": "w", "expandible": True}
        ])
        
        # Botones
        frame_btns = ttk.Frame(self.frame_contenido)
        frame_btns.pack(fill="x", pady=10)
        
        ttk.Button(frame_btns, text="Nueva Consulta", 
                   command=lambda: self.app.mostrar_frame("seleccion_empresa")).pack(side="right", padx=5)
        
        ttk.Button(frame_btns, text="Exportar a Excel", 
                   command=self._on_exportar).pack(side="right", padx=5)
    
    def _obtener_columnas_base(self):
        return [
            {"nombre": "Núm. Factura", "ancho": 100, "alineacion": "w", "expandible": False},
            {"nombre": "Fecha", "ancho": 100, "alineacion": "center", "expandible": False},
            {"nombre": "NIF", "ancho": 100, "alineacion": "center", "expandible": False},
            {"nombre": "Empresa", "ancho": 300, "alineacion": "w", "expandible": False},
            {"nombre": "Base IVA", "ancho": 75, "alineacion": "e", "expandible": False},
            {"nombre": "Tipo IVA", "ancho": 75, "alineacion": "e", "expandible": False},
            {"nombre": "Cuota IVA", "ancho": 75, "alineacion": "e", "expandible": False},
            {"nombre": "Total", "ancho": 75, "alineacion": "e", "expandible": False}
        ]
    
    def _crear_tabla(self, parent, columnas):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True, padx=5, pady=5)
        tabla = Tabla(frame)
        tabla.pack(fill="both", expand=True)
        tabla.cabecera(columnas)
        return tabla
    
    def inicializar(self):
        # Actualizar información de empresa en la cabecera
        self._actualizar_info_empresa()
        
        facturas_correctas, facturas_errores = self.controlador.obtener_resultados()
        
        self._cargar_datos(self.tabla_correctas, facturas_correctas, lambda f: ", ".join(f.observaciones))
        self._cargar_datos(self.tabla_errores, facturas_errores, lambda f: ", ".join(f.errores))
        
        self.notebook.tab(0, text=f"Facturas Correctas ({len(facturas_correctas)})")
        self.notebook.tab(1, text=f"Facturas con Errores ({len(facturas_errores)})")
    
    def _cargar_datos(self, tabla: Tabla, facturas: list, func_extra):
        datos_tabla = []
        for f in facturas:
            d = f.datos
            fila = [
                d.get(KEY.NUM_FACT, ""), d.get(KEY.FECHA_FACT, ""), d.get(KEY.NIF, ""),
                d.get(KEY.EMPRESA, ""), d.get(KEY.BASE_IVA, ""), d.get(KEY.TIPO_IVA, ""),
                d.get(KEY.CUOTA_IVA, ""), d.get(KEY.TOTAL_FACT, ""),
                func_extra(f)
            ]
            datos_tabla.append(fila)
        tabla.insertar(datos_tabla)

    def _on_exportar(self):
        ruta_orig = self.controlador.obtener_ruta_archivo()
        if not ruta_orig:
            self.mostrar_mensaje("error", "No hay archivo procesado.")
            return

        ruta_base = ruta_orig.rsplit('.', 1)[0]
        try:
            res = self.controlador.exportar_resultados(ruta_base)
            if res:
                msg = f"Exportado a:\n- {res.get('correctas', '')}\n- {res.get('errores', '')}"
                self.mostrar_mensaje("info", msg, "Exportación Exitosa")
            else:
                self.mostrar_mensaje("error", "Error al exportar.")
        except Exception as e:
            self.mostrar_mensaje("error", f"Excepción: {str(e)}")