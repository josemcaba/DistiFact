"""
Módulo que contiene la clase ClasificadorFacturas para clasificar facturas correctas o con errores.
"""
from typing import List, Tuple, Dict, Any
import conceptos_factura as KEY
import modelo.verificadores as verificar
from modelo.factura import Factura


class ClasificadorFacturas:
    """
    Clase que clasifica facturas en correctas y con errores.
    """
    def __init__(self):
        """Inicializa el clasificador de facturas."""
        pass
    
    def clasificar(self, facturas: List[Factura]) -> Tuple[List[Factura], List[Factura]]:
        """
        Clasifica las facturas en correctas y con errores.
        
        Args:
            facturas: Lista de facturas a clasificar
            
        Returns:
            Tupla con dos listas: (facturas_correctas, facturas_con_errores)
        """
        facturas_correctas = []
        facturas_con_errores = []

        vistos = {}
        for factura in facturas:
            # Detectamos duplicados por número de factura
            numero = factura.datos[KEY.NUM_FACT]
            if not numero:
                continue
            if numero in vistos:
                factura.agregar_error(f"Número de factura duplicado: {numero}")
                vistos[numero].agregar_error(f"Número de factura duplicado: {numero}")
            else:
                vistos[numero] = factura

        for factura in facturas:
            # Verificamos los campos de la factura
            self._verificar_campos(factura)
            
            # Clasificamos según si tiene errores
            if factura.tiene_errores():
                facturas_con_errores.append(factura)
            else:
                facturas_correctas.append(factura)

        return facturas_correctas, facturas_con_errores
    
    def _verificar_campos(self, factura: Factura) -> None:
        """
        Verifica los campos de una factura y agrega errores u observaciones.
        
        Args:
            factura: Factura a verificar
        """
        datos = factura.datos
        
        # Verificar número de factura
        error = verificar.num_factura(datos)
        if error:
            factura.agregar_error(error)
        
        # Verificar fecha
        error = verificar.fecha(datos)
        if error:
            factura.agregar_error(error)
        
        # Verificar NIF
        error = verificar.nif(datos)
        if error:
            factura.agregar_error(error)
        
        # Verificar nombre
        error = verificar.nombre(datos)
        if error:
            if "demasiado largo" in error:
                factura.agregar_observacion(error)
            else:
                factura.agregar_error(error)
        
        # Verificar importes
        conceptos = [
            KEY.BASE_IVA, KEY.TIPO_IVA, KEY.CUOTA_IVA,
            KEY.BASE_IRPF, KEY.TIPO_IRPF, KEY.CUOTA_IRPF,
            KEY.BASE_RE, KEY.TIPO_RE, KEY.CUOTA_RE, 
            KEY.TOTAL_FACT
        ]
        
        for concepto in conceptos:
            error = verificar.importe(datos, concepto)
            if error:
                if concepto == KEY.TOTAL_FACT:
                    factura.agregar_observacion(error)
                else:
                    factura.agregar_error(error)
        
        # Verificar cálculos de cuotas
        conceptos_cuota = [KEY.CUOTA_IVA, KEY.CUOTA_IRPF, KEY.CUOTA_RE]
        for concepto in conceptos_cuota:
            error = verificar.calculo_cuota(datos, concepto)
            if error:
                factura.agregar_error(error)
        
        # Verificar cálculos totales
        error = verificar.calculos_totales(datos)
        if error:
            factura.agregar_error(error)
