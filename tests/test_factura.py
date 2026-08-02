"""
Tests para el modelo/factura.py.
Cobertura: constructor, getters, agregar_error, agregar_observacion,
tiene_errores, get/set_valor, to_dict, __repr__, __eq__.
"""
import pytest
import extractores.conceptos_factura as KEY
from modelo.factura import Factura


class TestFacturaConstructor:
    def test_creacion_basica(self):
        f = Factura(5, {KEY.NUM_FACT: "F001"})
        assert f.num_pagina == 5
        assert f.datos[KEY.NUM_FACT] == "F001"
        assert f.errores == []
        assert f.observaciones == []

    def test_no_tiene_errores_inicialmente(self):
        f = Factura(1, {})
        assert not f.tiene_errores()


class TestFacturaErrores:
    def test_agregar_error_un_solo(self):
        f = Factura(3, {})
        f.agregar_error("Campo X no encontrado")
        assert f.tiene_errores()
        assert len(f.errores) == 1
        assert "Pag. 3" in f.errores[0]

    def test_agregar_error_multiple(self):
        f = Factura(3, {})
        f.agregar_error("Error 1")
        f.agregar_error("Error 2")
        assert len(f.errores) == 2
        # El segundo error no lleva el prefijo de página
        assert "Pag. 3" in f.errores[0]
        assert "Pag. 3" not in f.errores[1]

    def test_observaciones_se_agregan(self):
        f = Factura(1, {})
        f.agregar_observacion("Nombre demasiado largo")
        assert len(f.observaciones) == 1
        assert f.tiene_errores() is False  # observaciones no son errores


class TestFacturaGettersSetters:
    def test_get_valor_existente(self):
        f = Factura(1, {KEY.NUM_FACT: "F123", KEY.TOTAL_FACT: 100.0})
        assert f.get_valor(KEY.NUM_FACT) == "F123"

    def test_get_valor_inexistente(self):
        f = Factura(1, {})
        assert f.get_valor("NoExiste") is None

    def test_set_valor(self):
        f = Factura(1, {})
        f.set_valor(KEY.NUM_FACT, "F456")
        assert f.datos[KEY.NUM_FACT] == "F456"


class TestFacturaToDict:
    def test_to_dict_sin_errores(self):
        f = Factura(1, {KEY.NUM_FACT: "F1"})
        d = f.to_dict()
        assert d[KEY.NUM_FACT] == "F1"
        assert "Errores" not in d

    def test_to_dict_con_errores(self):
        f = Factura(2, {KEY.NUM_FACT: "F2"})
        f.agregar_error("Error de prueba")
        d = f.to_dict()
        assert d[KEY.NUM_FACT] == "F2"
        assert "Errores" in d
        assert "Error de prueba" in d["Errores"]


class TestFacturaRepr:
    def test_repr_basico(self):
        f = Factura(7, {KEY.NUM_FACT: "F7", KEY.EMPRESA: "Test", KEY.TOTAL_FACT: 100.0})
        r = repr(f)
        assert "Factura" in r
        assert "página=7" in r
        assert "F7" in r
        assert "OK" in r

    def test_repr_con_error(self):
        f = Factura(1, {KEY.NUM_FACT: "F1"})
        f.agregar_error("fallo")
        r = repr(f)
        assert "ERROR" in r


class TestFacturaEq:
    def test_igualdad_misma_factura(self):
        f1 = Factura(1, {KEY.NUM_FACT: "X"})
        f2 = Factura(1, {KEY.NUM_FACT: "X"})
        assert f1 == f2

    def test_diferencia_pagina(self):
        f1 = Factura(1, {KEY.NUM_FACT: "X"})
        f2 = Factura(2, {KEY.NUM_FACT: "X"})
        assert f1 != f2

    def test_diferencia_datos(self):
        f1 = Factura(1, {KEY.NUM_FACT: "X"})
        f2 = Factura(1, {KEY.NUM_FACT: "Y"})
        assert f1 != f2
