"""
Tests para el extractor MERCADONA.
El extractor retorna múltiples facturas (una por tipo de IVA).
"""
import pytest
import extractores.conceptos_factura as KEY
from extractores.extractores_MERCADONA import extraerDatosFactura, identificador


class TestIdentificador:
    def test_identificador_es_total_factura(self):
        assert identificador == "Total Factura"


class TestExtraccionMercadona:
    def test_factura_basica_sin_iva_desglosado(self):
        """Cuando no hay bloque de desglose de IVA, retorna una sola factura con datos comunes."""
        texto = (
            "Nº Factura: 12345\n"
            "Fecha Factura: 15/06/2024\n"
            "Total Factura\n"
        )
        pagina = [1, texto]
        empresa = {"id": 16, "nombre": "MERCADONA, S.A.", "nif": "A46103834", "tipo": "PDFtexto", "funciones": "extractores_MERCADONA.py"}
        res = extraerDatosFactura(pagina, empresa)
        assert isinstance(res, list)
        assert len(res) >= 1
        factura = res[-1]  # última factura
        assert factura[KEY.NUM_FACT] == "12345"
        assert factura[KEY.FECHA_FACT] == "15/06/2024"
        assert factura[KEY.CONCEPTO] == 600
        assert factura[KEY.NIF] == "A46103834"
        assert factura[KEY.EMPRESA] == "MERCADONA, S.A."

    def test_factura_con_multiples_ivas(self):
        """El extractor DEBE retornar una factura por cada tipo de IVA encontrado."""
        texto = (
            "Nº Factura: ABC123\n"
            "Fecha Factura: 10/03/2024\n"
            "Base Imponible    Cuota    Total     10%  100,00  10,00  110,00   21%  200,00  42,00  242,00\n"
            "Total Factura\n"
        )
        pagina = [1, texto]
        empresa = {"id": 16, "nombre": "MERCADONA, S.A.", "nif": "A46103834", "tipo": "PDFtexto", "funciones": "extractores_MERCADONA.py"}
        res = extraerDatosFactura(pagina, empresa)
        assert isinstance(res, list)
        assert len(res) == 2  # una factura por IVA (10% y 21%)
        # Cada factura debe tener los datos comunes
        for f in res:
            assert f[KEY.NUM_FACT] == "ABC123"
            assert f[KEY.FECHA_FACT] == "10/03/2024"
            assert f[KEY.NIF] == "A46103834"
            assert f[KEY.EMPRESA] == "MERCADONA, S.A."

    def test_factura_usa_nif_empresa(self):
        """El extractor DEBE usar empresa['nif'] y empresa['nombre'], no hardcodear."""
        texto = "Nº Factura: X1\nFecha Factura: 01/01/2024\nTotal Factura\n"
        empresa = {"nif": "NIFTEST", "nombre": "NombreTest"}
        res = extraerDatosFactura([1, texto], empresa)
        assert res[0][KEY.NUM_FACT] == "X1"
        assert res[0][KEY.NIF] == "NIFTEST"
        assert res[0][KEY.EMPRESA] == "NombreTest"
