"""
Tests para las funciones básicas de utilidad en modelo/ft_basicas.py.
Cobertura: convertir_a_float, validar_fecha, validar_nif/dni/nie/cif, re_search, re_search_multiple.
"""
import pytest
from modelo.ft_basicas import (
    convertir_a_float,
    validar_fecha,
    validar_nif,
    validar_dni,
    validar_nie,
    validar_cif,
    re_search,
    re_search_multiple,
)


# ---------------------------------------------------------------------------
# convertir_a_float
# ---------------------------------------------------------------------------

class TestConvertirAFloat:
    def test_numero_con_punto(self):
        assert convertir_a_float("123.45") == 123.45

    def test_numero_con_coma(self):
        assert convertir_a_float("123,45") == 123.45

    def test_numero_con_euro(self):
        assert convertir_a_float("123,45€") == 123.45

    def test_numero_con_separador_miles_punto(self):
        # "1.234,56" -> 1234.56 (elimina puntos excepto el último)
        assert convertir_a_float("1.234,56") == 1234.56

    def test_numero_invalido(self):
        assert convertir_a_float("abc") is None

    def test_numero_vacio(self):
        assert convertir_a_float("") is None

    def test_entrada_none(self):
        assert convertir_a_float(None) is None


# ---------------------------------------------------------------------------
# validar_fecha
# ---------------------------------------------------------------------------

class TestValidarFecha:
    def test_fecha_dd_mm_aaaa(self):
        assert validar_fecha("15/06/2024") == "15/06/2024"

    def test_fecha_d_m_aa(self):
        assert validar_fecha("1/5/24") == "01/05/2024"

    def test_fecha_con_guiones(self):
        assert validar_fecha("15-06-2024") is False

    def test_fecha_invalida(self):
        assert validar_fecha("32/13/2024") is False

    def test_fecha_eeuu(self):
        assert validar_fecha("06/15/2024", is_eeuu=True) == "15/06/2024"


# ---------------------------------------------------------------------------
# validar_nif / dni / nie / cif
# ---------------------------------------------------------------------------

class TestValidarNIF:
    # DNI válido: 12345678Z (verificado manualmente)
    def test_dni_valido(self):
        assert validar_dni("12345678Z") is True

    def test_dni_invalido(self):
        assert validar_dni("12345678X") is False

    def test_nie_valido(self):
        assert validar_nie("X1234567L") is True

    def test_nie_invalido(self):
        assert validar_nie("X1234567X") is False

    def test_cif_valido_letra_a(self):
        assert validar_cif("A58832593") is True

    def test_cif_invalido(self):
        assert validar_cif("A58832599") is False

    def test_nif_completo_valido(self):
        assert validar_nif("12345678Z") is True

    def test_nif_nie_completo_valido(self):
        assert validar_nif("X1234567L") is True

    def test_nif_cif_completo_valido(self):
        assert validar_nif("A58832593") is True

    def test_nif_formato_invalido(self):
        assert validar_nif("abc") is False

    def test_nif_vacio(self):
        assert validar_nif("") is False


# ---------------------------------------------------------------------------
# re_search / re_search_multiple
# ---------------------------------------------------------------------------

class TestReSearch:
    def test_re_search_encontrado(self):
        assert re_search(r"Total\s*([\d,.]+)", "Total 123,45") == "123,45"

    def test_re_search_no_encontrado(self):
        assert re_search(r"Total\s*([\d,.]+)", "No hay total") is None

    def test_re_search_multiple_grupos(self):
        resultado = re_search_multiple(r"([\d.]+)\s+(\d+)", "100.00 21")
        assert resultado == ["100.00", "21"]

    def test_re_search_multiple_no_encontrado(self):
        assert re_search_multiple(r"([\d.]+)\s+(\d+)", "no hay numeros") is None

    def test_re_search_multiple_un_grupo(self):
        # lastindex == 1, devuelve [grupo1]
        resultado = re_search_multiple(r"(\d+)", "12345")
        assert resultado == ["12345"]
