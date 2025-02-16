import pdfplumber
import re
import pandas as pd

def extraer_informacion_facturas(pdf_path):
    texto_completo = ""
    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if texto:
                texto_completo += texto + "\n"
    
    # Dividir el texto en secciones usando "Fecha emisión" como separador
    secciones = re.split(r"(?=Fecha emisión)", texto_completo)
    
    facturas = []
    
    for seccion in secciones:
        if "Fecha emisión" not in seccion:
            continue
        
        datos_factura = {}
        
        # Número de factura
        num_factura = re.search(r"Nº factura\s*(\d+)", seccion)
        datos_factura["Num. Factura"] = num_factura.group(1) if num_factura else 0
        
        # Fecha de factura y asignar la misma a Fecha Oper.
        fecha = re.search(r"Fecha emisión\s*([\d/]+)", seccion)
        if fecha:
            datos_factura["Fecha Fact."] = fecha.group(1)
            datos_factura["Fecha Oper."] = fecha.group(1)
        else:
            datos_factura["Fecha Fact."] = 0
            datos_factura["Fecha Oper."] = 0
        
        # Concepto fijo "700"
        datos_factura["Concepto"] = 700
        
        # Extraer Base I.V.A.
        base = re.search(r"Base\s*([\d,\.]+)", seccion)
        if base:
            base_str = base.group(1)
            datos_factura["Base I.V.A."] = base_str
            try:
                base_valor = float(base_str.replace(",", "."))
            except:
                base_valor = 0.0
        else:
            datos_factura["Base I.V.A."] = 0
            base_valor = 0.0
        
        # Extraer Cuota I.V.A.
        iva = re.search(r"IVA\s*([\d,\.]+)", seccion)
        if iva:
            iva_str = iva.group(1)
            datos_factura["Cuota I.V.A."] = iva_str
            try:
                iva_valor = float(iva_str.replace(",", "."))
            except:
                iva_valor = 0.0
        else:
            datos_factura["Cuota I.V.A."] = 0
            iva_valor = 0.0
        
        # Calcular % I.V.A. redondeado al entero más cercano
        if base_valor:
            datos_factura["% I.V.A."] = int(round((iva_valor / base_valor) * 100))
        else:
            datos_factura["% I.V.A."] = 0
        
        # Las bases de I.R.P.F. y de R. Equiv. son iguales que Base I.V.A.
        datos_factura["Base I.R.P.F."] = datos_factura["Base I.V.A."]
        datos_factura["Base R. Equiv."] = datos_factura["Base I.V.A."]
        
        # Completar los campos no usados con 0
        datos_factura["% I.R.P.F."] = 0
        datos_factura["Cuota I.R.P.F."] = 0
        datos_factura["% R. Equiv."] = 0
        datos_factura["Cuota R. Equiv."] = 0
        
        # Extraer Total Factura usando primero un patrón más específico.
        total_match = re.search(r"IVA\s*[\d,\.]+\s*Total\s*([\d,\.]+)\s*€", seccion)
        if not total_match:
            total_match = re.search(r"Total\s*([\d,\.]+)\s*€", seccion)
        if total_match:
            total_str = total_match.group(1)
            try:
                total_valor = float(total_str.replace(",", "."))
            except:
                total_valor = 0.0
        else:
            total_valor = 0.0
        datos_factura["Total Factura"] = total_valor  # Este campo se usará solo para la comprobación
        
        # Extraer NIF/DNI y Nombre a partir de la línea después de "logo"
        lines = seccion.splitlines()
        lines = [line.strip() for line in lines if line.strip()]
        if "logo" in lines:
            idx_logo = lines.index("logo")
            if len(lines) > idx_logo + 1:
                linea_nombres = lines[idx_logo + 1]
                if "Pescadería Salvador" in linea_nombres:
                    cliente_nombre = linea_nombres.replace("Pescadería Salvador", "").strip()
                    datos_factura["Nombre"] = cliente_nombre if cliente_nombre else 0
                else:
                    datos_factura["Nombre"] = linea_nombres
            else:
                datos_factura["Nombre"] = 0

            if len(lines) > idx_logo + 3:
                nif_line = lines[idx_logo + 3]
                tokens = nif_line.split()
                if len(tokens) >= 2:
                    datos_factura["NIF/DNI"] = tokens[1]
                else:
                    datos_factura["NIF/DNI"] = 0
            else:
                datos_factura["NIF/DNI"] = 0
        else:
            datos_factura["Nombre"] = 0
            datos_factura["NIF/DNI"] = 0
        
        facturas.append(datos_factura)
    
    return facturas

def main():
    pdf_path = "Las Yucas.pdf"  # Ruta del archivo PDF
    facturas = extraer_informacion_facturas(pdf_path)
    
    # Definir las columnas exactas para el Excel (sin incluir Total Factura)
    columnas = [
        "Num. Factura", "Fecha Fact.", "Fecha Oper.", "Concepto",
        "Base I.V.A.", "% I.V.A.", "Cuota I.V.A.", "Base I.R.P.F.", "% I.R.P.F.", "Cuota I.R.P.F.",
        "Base R. Equiv.", "% R. Equiv.", "Cuota R. Equiv.",
        "NIF/DNI", "Nombre"
    ]
    
    # Crear el DataFrame (sin la columna Total Factura)
    df = pd.DataFrame(facturas, columns=columnas)
    
    # Exportar a Excel
    output_excel = "facturas.xlsx"
    df.to_excel(output_excel, index=False)
    print(f"Se han extraído {len(facturas)} facturas y exportado a {output_excel}")
    
    # Mostrar por consola las facturas con % I.V.A. distinto de 10
    print("Facturas con % I.V.A. distinto de 10:")
    for factura in facturas:
        if factura.get("% I.V.A.", 0) != 10:
            print(
                f"Num. Factura: {factura.get('Num. Factura')}, "
                f"Fecha Fact.: {factura.get('Fecha Fact.')}, "
                f"Base I.V.A.: {factura.get('Base I.V.A.')}, "
                f"Cuota I.V.A.: {factura.get('Cuota I.V.A.')}, "
                f"% I.V.A.: {factura.get('% I.V.A.')}"
            )
    
    # Verificar que la suma de Base I.V.A. + Cuota I.V.A. coincide con el Total Factura
    print("\nFacturas en las que la suma de Base I.V.A. y Cuota I.V.A. NO coincide con el Total Factura:")
    for factura in facturas:
        try:
            base_valor = float(str(factura.get("Base I.V.A.", 0)).replace(",", "."))
            cuota_valor = float(str(factura.get("Cuota I.V.A.", 0)).replace(",", "."))
            total_factura = float(factura.get("Total Factura", 0))
            # Tolerancia de 0.01 para redondeo
            if abs((base_valor + cuota_valor) - total_factura) > 0.01:
                print(
                    f"Num. Factura: {factura.get('Num. Factura')}, "
                    f"Fecha Fact.: {factura.get('Fecha Fact.')}, "
                    f"Base I.V.A.: {factura.get('Base I.V.A.')}, "
                    f"Cuota I.V.A.: {factura.get('Cuota I.V.A.')}, "
                    f"Total Factura: {factura.get('Total Factura')}"
                )
        except Exception as e:
            print(f"Error al procesar la factura {factura.get('Num. Factura')}: {e}")

if __name__ == "__main__":
    main()
