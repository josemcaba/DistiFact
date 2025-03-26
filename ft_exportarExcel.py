import conceptos_factura as KEY
import pandas as pd
from ft_mensajes_POO import msg

def exportar_a_excel(facturas_correctas, facturas_con_errores, excel_path):
    """
    Exporta las facturas correctas y con errores a archivos Excel separados.
    """
    columnas = [
        KEY.NUM_FACT, KEY.FECHA_FACT, KEY.FECHA_OPER, KEY.CONCEPTO,
        KEY.BASE_IVA, KEY.TIPO_IVA, KEY.CUOTA_IVA, 
        KEY.BASE_IRPF, KEY.TIPO_IRPF, KEY.CUOTA_IRPF,
        KEY.BASE_RE, KEY.TIPO_RE, KEY.CUOTA_RE,
        KEY.NIF, KEY.EMPRESA
    ]

    # Exportar facturas correctas
    if facturas_correctas:
        df_correctas = pd.DataFrame(facturas_correctas, columns=columnas + ["Observaciones"])
        df_correctas = df_correctas.sort_values(by=columnas[0])
        df_correctas.to_excel(excel_path.replace(".xlsx", "_correctas.xlsx"), index=False)
        msg.info(f"Se han exportado {len(facturas_correctas)} facturas correctas.")
    else:
        msg.info("No hay facturas correctas para exportar.")

    # Exportar facturas con errores
    if facturas_con_errores:
        df_errores = pd.DataFrame(facturas_con_errores, columns=columnas + ["Errores"])
        df_errores = df_errores.sort_values(by=columnas[0])
        df_errores.to_excel(excel_path.replace(".xlsx", "_errores.xlsx"), index=False)
        msg.info(f"Se han exportado {len(facturas_con_errores)} facturas con errores.")
    else:
        msg.info("No hay facturas con errores para exportar.")
