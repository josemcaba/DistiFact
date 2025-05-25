"""
Script para validar la aplicación DistiFact-OOP-Tkinter.
Este script realiza pruebas básicas para verificar que la aplicación funciona correctamente.
"""
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Agregar directorio actual al path para importaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar componentes de la aplicación
from modelo.empresa import Empresa, EmpresaManager
from modelo.factura import Factura
from modelo.procesador import ProcesadorFacturas
from modelo.clasificador import ClasificadorFacturas
from modelo.exportador import ExportadorExcel
from controlador.controlador import Controlador


class TestDistiFact(unittest.TestCase):
    """Clase para probar la funcionalidad básica de DistiFact."""
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        self.empresa_manager = EmpresaManager()
        self.procesador = ProcesadorFacturas()
        self.clasificador = ClasificadorFacturas()
        self.exportador = ExportadorExcel()
        self.controlador = Controlador()
    
    def test_empresa_manager_carga(self):
        """Prueba la carga de empresas desde el archivo JSON."""
        resultado = self.empresa_manager.cargar_empresas("empresas.json")
        self.assertTrue(resultado)
        self.assertGreater(len(self.empresa_manager.listar_empresas()), 0)
    
    def test_empresa_creacion(self):
        """Prueba la creación de una instancia de Empresa."""
        empresa = Empresa(1, "Test", "B12345678", "PDFtexto", "extractores_Test.py")
        self.assertEqual(empresa.id, 1)
        self.assertEqual(empresa.nombre, "Test")
        self.assertEqual(empresa.nif, "B12345678")
        self.assertEqual(empresa.tipo, "PDFtexto")
        self.assertEqual(empresa.funciones, "extractores_Test.py")
    
    def test_factura_creacion(self):
        """Prueba la creación de una instancia de Factura."""
        datos = {"NumFactura": "F001", "Fecha": "01/01/2023"}
        factura = Factura(1, datos)
        self.assertEqual(factura.num_pagina, 1)
        self.assertEqual(factura.datos, datos)
        self.assertFalse(factura.tiene_errores())
        
        # Agregar error y verificar
        factura.agregar_error("Error de prueba")
        self.assertTrue(factura.tiene_errores())
        self.assertEqual(len(factura.errores), 1)
    
    def test_controlador_inicializacion(self):
        """Prueba la inicialización del controlador."""
        with patch.object(EmpresaManager, 'cargar_empresas', return_value=True):
            resultado = self.controlador.iniciar("empresas.json")
            self.assertTrue(resultado)
    
    def test_controlador_seleccion_empresa(self):
        """Prueba la selección de empresa en el controlador."""
        # Mock para el método obtener_empresa
        empresa_mock = Empresa(1, "Test", "B12345678", "PDFtexto", "extractores_Test.py")
        self.controlador._empresa_manager.obtener_empresa = MagicMock(return_value=empresa_mock)
        
        resultado = self.controlador.seleccionar_empresa(1)
        self.assertTrue(resultado)
        self.assertEqual(self.controlador.obtener_empresa_actual(), empresa_mock)


if __name__ == "__main__":
    unittest.main()
