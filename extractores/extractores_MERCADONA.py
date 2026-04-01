import extractores.conceptos_factura as KEY
import re
import modelo.ft_basicas as fb

# El parámetro identificador es un texto que debe aparecer en la página
# del PDF para ser validada como factura.
# Las páginas que no contengan este texto son descartadas.

identificador="Total Factura"

#########################################################################
#
# EXTRACCION
#
# Se limita exclusivamente a extraer los datos tal como aparecen en las
# facturas intentando evitar cualquier manipulación. Eso se hace en la
# fase de verificación para que sirva en todos los casos
#
def extraerDatosFactura(pagina, empresa):
    pagina = pagina[1]

    # 1. EXTRACCIÓN DE DATOS COMUNES (Cabecera)
    # Estos datos se repiten en todas las líneas de desglose de IVA
    datos_comunes = {}

    # Número de factura
    regex = r"N.\s*Factura:\s*(.*?)\s+"
    datos_comunes[KEY.NUM_FACT] = fb.re_search(regex, pagina)

    # Fecha Factura
    regex = r"Fecha\s*Factura:\s*(.*?)\s+"
    datos_comunes[KEY.FECHA_FACT] = fb.re_search(regex, pagina)
    # datos_comunes[KEY.FECHA_OPER] = datos_comunes[KEY.FECHA_FACT]

    # Concepto fijo
    datos_comunes[KEY.CONCEPTO] = 600

    # Datos de la factura
    datos_comunes[KEY.NIF] = empresa["nif"]
    datos_comunes[KEY.EMPRESA] = empresa["nombre"]
    datos_comunes[KEY.BASE_IVA] = ""
    datos_comunes[KEY.TIPO_IVA] = ""
    datos_comunes[KEY.CUOTA_IVA] = ""
    datos_comunes[KEY.BASE_IRPF] = ""
    datos_comunes[KEY.TIPO_IRPF] = ""
    datos_comunes[KEY.CUOTA_IRPF] = ""
    datos_comunes[KEY.BASE_RE] = ""
    datos_comunes[KEY.TIPO_RE] = ""
    datos_comunes[KEY.CUOTA_RE] = ""
    datos_comunes[KEY.TOTAL_FACT] = ""

    # 2. EXTRACCIÓN DE DESGLOSE DE IVA
    # Lista donde guardaremos cada fila resultante (una por tipo de IVA)
    facturas = []
    facturas.append(datos_comunes)

    # Localizar el bloque donde están los totales       
    # Busca texto entre "Base Imponible...Total...Total Factura"
    regex = r"Base Imponible\s+Cuota\s+Total\s*(.*?)\s*Total\s+Factura"
    match = re.search(regex, pagina, re.DOTALL | re.IGNORECASE)
    if match:
        bloque = match.group(1)

        # Regex para capturar cada línea: % IVA | Base | Cuota | Total Línea
        # Ejemplo línea: 10%  100,50  10,05  110,55
        regex = r"(\d+)%\s+([\d,.]+)\s+([\d,.]+)\s+([\d,.]+)"
        datos = re.findall(regex, bloque)
        if datos:
            facturas = []

        for iva, base, cuota, total in datos:
            # Creamos una COPIA de los datos comunes para esta línea
            factura = datos_comunes.copy()

            factura[KEY.BASE_IVA] = base
            factura[KEY.TIPO_IVA] = iva
            factura[KEY.CUOTA_IVA] = cuota
    
            factura[KEY.BASE_IRPF] = factura[KEY.BASE_IVA]
            factura[KEY.TIPO_IRPF] = 0
            factura[KEY.CUOTA_IRPF] = 0

            factura[KEY.BASE_RE] = factura[KEY.BASE_IVA]
            factura[KEY.TIPO_RE] = 0
            factura[KEY.CUOTA_RE] = 0

            factura[KEY.TOTAL_FACT] = total
            
            # Agregar a la lista de resultados
            facturas.append(factura)
            
    # Devolvemos la lista de diccionarios.
    return(facturas)     
