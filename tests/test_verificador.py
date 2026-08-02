"""
Tests para el modelo/verificador.py.
Cobertura: num_factura, fecha, nif, nombre, importe, calculo_cuota, calculos_totales.

Nota: El verificador opera sobre un dict de factura. Los importes deben ser
floats (el método importe() los convierte, pero para testear calculos_totales
directamente usamos floats desde el inicio).
"""
import pytest
import extractores.conceptos_factura as KEY
from modelo.verificador import VerificadorFactura


def _factura_base():
    """Crea un diccionario de factura base para pruebas con importes como float."""
    return {
        KEY.NUM_FACT: "F001",
        KEY.FECHA_FACT: "15/06/2024",
        KEY.NIF: "12345678Z",
        KEY.EMPRESA: "Empresa Test S.L.",
        KEY.BASE_IVA: 100.00,
        KEY.TIPO_IVA: 21.0,
        KEY.CUOTA_IVA: 21.00,
        KEY.BASE_IRPF: 100.00,
        KEY.TIPO_IRPF: 0.0,
        KEY.CUOTA_IRPF: 0.00,
        KEY.BASE_RE: 100.00,
        KEY.TIPO_RE: 0.0,
        KEY.CUOTA_RE: 0.00,
        KEY.TOTAL_FACT: 121.00,
    }


class TestNumFactura:
    def test_num_factura_presente(self):
        v = VerificadorFactura(_factura_base())
        assert v.num_factura() is False

    def test_num_factura_none(self):
        v = VerificadorFactura(_factura_base())
        v.factura[KEY.NUM_FACT] = None
        assert "no encontrado" in v.num_factura()


class TestFecha:
    def test_fecha_valida(self):
        v = VerificadorFactura(_factura_base())
        assert v.fecha() is False
        assert v.factura[KEY.FECHA_FACT] == "15/06/2024"

    def test_fecha_none(self):
        v = VerificadorFactura(_factura_base())
        v.factura[KEY.FECHA_FACT] = None
        assert "no encontrada" in v.fecha()

    def test_fecha_invalida(self):
        v = VerificadorFactura(_factura_base())
        v.factura[KEY.FECHA_FACT] = "32/13/2024"
        assert "incorrecta" in v.fecha()


class TestNIF:
    def test_nif_valido(self):
        v = VerificadorFactura(_factura_base())
        assert v.nif() is False

    def test_nif_none(self):
        v = VerificadorFactura(_factura_base())
        v.factura[KEY.NIF] = None
        assert "no encontrado" in v.nif()

    def test_nif_con_espacios(self):
        v = VerificadorFactura(_factura_base())
        v.factura[KEY.NIF] = " 12345678 Z "
        assert v.nif() is False
        assert v.factura[KEY.NIF] == "12345678Z"

    def test_nif_es_prefijo(self):
        v = VerificadorFactura(_factura_base())
        v.factura[KEY.NIF] = "ES12345678Z"
        assert v.nif() is False
        assert v.factura[KEY.NIF] == "12345678Z"


class TestImporte:
    def test_importe_valido(self):
        v = VerificadorFactura(_factura_base())
        assert v.importe(KEY.BASE_IVA) is False
        assert v.factura[KEY.BASE_IVA] == 100.0

    def test_importe_string_numero(self):
        """El importe debe convertir strings a float."""
        v = VerificadorFactura(_factura_base())
        v.factura[KEY.BASE_IVA] = "100,50"
        assert v.importe(KEY.BASE_IVA) is False
        assert v.factura[KEY.BASE_IVA] == 100.5

    def test_importe_none(self):
        v = VerificadorFactura(_factura_base())
        v.factura[KEY.BASE_IVA] = None
        assert "no encontrado" in v.importe(KEY.BASE_IVA)

    def test_importe_invalido(self):
        v = VerificadorFactura(_factura_base())
        v.factura[KEY.BASE_IVA] = "abc"
        assert "incorrecto" in v.importe(KEY.BASE_IVA)


class TestCalculosTotales:
    def test_total_correcto(self):
        v = VerificadorFactura(_factura_base())
        # 100 + 21 - 0 + 0 = 121
        assert v.calculos_totales() is False

    def test_total_incorrecto(self):
        v = VerificadorFactura(_factura_base())
        v.factura[KEY.TOTAL_FACT] = 200.00
        assert "!= Calculado" in v.calculos_totales()


class TestCalculoCuota:
    def test_cuota_iva_correcta(self):
        v = VerificadorFactura(_factura_base())
        assert v.calculo_cuota(KEY.CUOTA_IVA) is False
