"""
Para ejecutar estos tests debe lanzarse el siguiente comando en la consola:
    python -m unittest test_funciones_comunes

El siguiente comando lanzaría todos los tests del directorio
    python -m unittest discover
"""

import unittest
import funciones_comunes as ft

class TestArea(unittest.TestCase):
    def test_float(self):
        self.assertAlmostEqual(ft.convertir_a_float("25"), 25.0)
        self.assertAlmostEqual(ft.convertir_a_float("25.3"), 25.3)
        self.assertAlmostEqual(ft.convertir_a_float("25,3"), 25.3)
        self.assertAlmostEqual(ft.convertir_a_float("0025,30"), 25.3)
        self.assertAlmostEqual(ft.convertir_a_float("  25.3 "), 25.3)
        self.assertAlmostEqual(ft.convertir_a_float("2 5,3"), 0.0)
        self.assertAlmostEqual(ft.convertir_a_float(""), 0.0)
        
    def test_nif(self):
        self.assertAlmostEqual(ft.validar_nif("12345678A"), False)
        self.assertAlmostEqual(ft.validar_nif("123X5678Z"), False)
        self.assertAlmostEqual(ft.validar_nif("12345678Z"), True)
        self.assertAlmostEqual(ft.validar_nif("25076670z"), False)
        self.assertAlmostEqual(ft.validar_nif("X1234567L"), True)
        self.assertAlmostEqual(ft.validar_nif("x1234567L"), False)
        self.assertAlmostEqual(ft.validar_nif("Y1234567X"), True)
        self.assertAlmostEqual(ft.validar_nif("Z1234567R"), True)
        self.assertAlmostEqual(ft.validar_nif("K1234567D"), True)
        self.assertAlmostEqual(ft.validar_nif("K1234567d"), False)
