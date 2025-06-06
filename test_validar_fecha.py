"""
Para ejecutar estos tests debe lanzarse el siguiente comando en la consola:
    python -m unittest test_validar_fecha

El siguiente comando lanzaría todos los tests del directorio
    python -m unittest discover
"""

import unittest
from ft_procesarFacturas import validar_fecha

class TestArea(unittest.TestCase):
    
    def test_fecha(self):
        self.assertAlmostEqual(validar_fecha("30/02/2024"), False)
        self.assertAlmostEqual(validar_fecha("28/02/24"), "28/02/2024")
        self.assertAlmostEqual(validar_fecha("8/2/24"), "08/02/2024")
        self.assertAlmostEqual(validar_fecha("02/28/24"), False)
        self.assertAlmostEqual(validar_fecha("02/28/24", is_eeuu=True), "28/02/2024")
        self.assertAlmostEqual(validar_fecha("28/02/024"), False)
