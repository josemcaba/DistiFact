import extractores.conceptos_factura as KEY
import modelo.ft_basicas as fb

class VerificadorFactura:
    def __init__(self, factura: dict):
        """
        Inicializa el verificador para una factura concreta
        """
        self.factura = factura

    def num_factura(self):
        if self.factura[KEY.NUM_FACT] is None:
            return (f"Núm. {KEY.NUM_FACT} no encontrado")
        return False # No hay errores

    def fecha(self, is_eeuu=False):
        if self.factura[KEY.FECHA_FACT] is None:
            return (f"{KEY.FECHA_FACT} no encontrada")

        fecha = fb.validar_fecha(self.factura[KEY.FECHA_FACT], is_eeuu)
        if not fecha:
            return (f"{KEY.FECHA_FACT} incorrecta")

        self.factura[KEY.FECHA_FACT] = fecha
        self.factura[KEY.FECHA_OPER] = fecha
        return False # No hay errores

    def nif(self):
        if self.factura[KEY.NIF] is None:
            return (f"{KEY.NIF} no encontrado")

        if not fb.validar_nif(self.factura[KEY.NIF]):
            return (f"{KEY.NIF} incorrecto")
        return False # No hay errores

    def nombre(self):
        if self.factura[KEY.EMPRESA] is None:
            return (f"{self.factura[KEY.EMPRESA]} no encontrado")
        if len(self.factura[KEY.EMPRESA]) > 40:
            nombreLargo = self.factura[KEY.EMPRESA]
            self.factura[KEY.EMPRESA] = self.factura[KEY.EMPRESA][0:40]
            return (f'"{nombreLargo}" demasiado largo. Máximo 40 caracteres.')
        return False # No hay errores

    def importe(self, concepto):
        if self.factura[concepto] is None:
            return (f"{concepto} no encontrado")

        valor = fb.convertir_a_float(self.factura[concepto])
        if valor is None:
            return (f"{concepto} incorrecto")
        
        self.factura[concepto] = valor
        return False # No hay errores
    
    def calculo_cuota(self, concepto):
        if concepto == KEY.CUOTA_IVA:
            base, tipo, cuota = KEY.BASE_IVA, KEY.TIPO_IVA, KEY.CUOTA_IVA
        elif concepto == KEY.CUOTA_IRPF:
            base, tipo, cuota = KEY.BASE_IRPF, KEY.TIPO_IRPF, KEY.CUOTA_IRPF
        elif concepto == KEY.CUOTA_RE:
            base, tipo, cuota = KEY.BASE_RE, KEY.TIPO_RE, KEY.CUOTA_RE
        base = self.factura[base]
        tipo = self.factura[tipo]
        cuota = self.factura[cuota]
        cuota_calculada = round(base * tipo / 100, 2)
        if abs(cuota_calculada - cuota) >= 0.015:
            return (f"{concepto}={cuota} != Calculado={cuota_calculada}")
        return False # No hay errores

    def calculos_totales(self):
        base = self.factura[KEY.BASE_IVA]
        cuota_iva = self.factura[KEY.CUOTA_IVA]
        cuota_irpf = self.factura[KEY.CUOTA_IRPF]
        cuota_re = self.factura[KEY.CUOTA_RE]
        total = self.factura[KEY.TOTAL_FACT]
        total_calculado = round(base + cuota_iva + cuota_irpf + cuota_re, 2)
        if abs(total_calculado - total) >= 0.015:
            return (f"{KEY.TOTAL_FACT}={total} != Calculado={total_calculado}")
        return False # No hay errores

    def corrige_por_total(self):
        base = self.factura[KEY.BASE_IVA]
        tipo = self.factura[KEY.TIPO_IVA]
        cuota = self.factura[KEY.CUOTA_IVA]
        total = self.factura[KEY.TOTAL_FACT]
        if not (isinstance(total, float) and isinstance(tipo, float)):
            return "Correccion por Total no calculable"
        base_calculada = round(total / (1 + tipo / 100), 2)
        cuota_calculada = round(total - base_calculada, 2)
        self.factura[KEY.BASE_IVA] = base_calculada
        self.factura[KEY.CUOTA_IVA] = cuota_calculada
        self.factura[KEY.BASE_IRPF] = base_calculada
        self.factura[KEY.BASE_RE] = base_calculada
        return (f"Corregido por total: {total} [Base ({base}) y Cuota ({cuota})]")

    def corrige_por_base(self):
        base = self.factura[KEY.BASE_IVA]
        tipo = self.factura[KEY.TIPO_IVA]
        cuota = self.factura[KEY.CUOTA_IVA]
        total = self.factura[KEY.TOTAL_FACT]
        cuota_calculada = round(base * tipo / 100, 2)
        total_calculado = round(base + cuota_calculada, 2)
        self.factura[KEY.CUOTA_IVA] = cuota_calculada
        self.factura[KEY.TOTAL_FACT] = total_calculado
        return (f"Corregido por base: {base} [Cuota ({cuota}) y Total ({total})]") 
