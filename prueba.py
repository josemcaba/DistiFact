import pdfplumber
import re

def extraer_informacion_facturas(pdf_path):
    # Abrir el PDF y concatenar todo el texto de sus páginas
    with pdfplumber.open(pdf_path) as pdf:
        texto_completo = "\n".join(
            pagina.extract_text() for pagina in pdf.pages if pagina.extract_text()
        )

    # Dividir el texto en secciones usando "Enlaza Soluciones" como separador
    secciones = re.split(r"(?=Enlaza Soluciones)", texto_completo)
    
    facturas = []
    
    for seccion in secciones:
        # Procesar la sección solo si contiene "Número de Factura"
        if "Número de Factura" not in seccion:
            continue

        factura = {}

        # --- Extraer Número de Factura (solo dígitos, sin "Fact-") ---
        m = re.search(r"Número de Factura.*?Titulo\s*\n\s*Fact-(\d+)", seccion, re.DOTALL)
        factura["Número de factura"] = m.group(1) if m else "No encontrado"

        # --- Extraer Fecha de Facturación ---
        m = re.search(r"Fecha de Facturación\s+Fecha de Vencimiento\s*\n\s*(\d{2}/\d{2}/\d{4})", seccion, re.DOTALL)
        if m:
            factura["Fecha de facturación"] = m.group(1)
        else:
            m = re.search(r"Fecha de Facturación\s*\n\s*(\d{2}/\d{2}/\d{4})", seccion, re.DOTALL)
            factura["Fecha de facturación"] = m.group(1) if m else "No encontrada"

        # --- Extraer datos del Cliente ---
        # Buscamos la sección "Datos Cliente" y recogemos las líneas siguientes hasta una línea vacía.
        cliente_info = []
        lineas = seccion.splitlines()
        idx_cliente = None
        for i, linea in enumerate(lineas):
            if "Datos Cliente" in linea:
                idx_cliente = i
                break
        if idx_cliente is not None:
            for linea in lineas[idx_cliente+1:]:
                if linea.strip() == "":
                    break
                cliente_info.append(linea.strip())
        if cliente_info:
            # Se asume que el primer elemento es el nombre del cliente
            nombre_cliente = cliente_info[0]
            # Eliminar la cadena "Gregorio Aranda García" (insensible a mayúsculas) del nombre
            nombre_cliente = re.sub(r"(?i)gregorio aranda garcía", "", nombre_cliente).strip()
            factura["Nombre del cliente"] = nombre_cliente

            # --- Extraer NIF/DNI del cliente ---
            nif_cliente = None
            # Buscamos en cada línea del bloque un patrón que coincida con 9 caracteres alfanuméricos,
            # descartando el valor "25693621E" (insensible a mayúsculas)
            for linea in cliente_info:
                m_nif = re.search(r"\b[A-Z0-9]{9}\b", linea, re.IGNORECASE)
                if m_nif:
                    candidato = m_nif.group(0).upper()
                    if candidato != "25693621E":
                        nif_cliente = candidato
                        break
            # Si no se encontró ningún NIF válido, se asigna "No encontrado"
            factura["NIF/DNI del cliente"] = nif_cliente if nif_cliente else "No encontrado"
        else:
            factura["Nombre del cliente"] = "No encontrado"
            factura["NIF/DNI del cliente"] = "No encontrado"

        # --- Extraer Subtotal ---
        m = re.search(r"Subtotal\s+([\d,\.]+)", seccion)
        factura["Subtotal"] = m.group(1) if m else "No encontrado"

        # --- Extraer Tipo de IVA (%) ---
        m = re.search(r"IVA\s*\((\d+)%\)", seccion)
        factura["Tipo de IVA (%)"] = m.group(1) + "%" if m else "No encontrado"

        # --- Extraer Total IVA ---
        m = re.search(r"IVA\s*\(\d+%\)\s+([\d,\.]+)", seccion)
        factura["Total IVA"] = m.group(1) if m else "No encontrado"

        # --- Extraer Total factura ---
        # Se toma la última aparición de "Total" seguida de un importe.
        matches = re.findall(r"Total\s+([\d,\.]+)", seccion)
        factura["Total factura"] = matches[-1] if matches else "No encontrado"

        facturas.append(factura)
    
    return facturas

# Ejemplo de uso:
pdf_path = "3.pdf"  # Asegúrate de tener el archivo "3.pdf" en el directorio actual
facturas = extraer_informacion_facturas(pdf_path)

# Mostrar los resultados en formato texto:
for f in facturas:
    print("\n-------------------------")
    for clave, valor in f.items():
        print(f"{clave}: {valor}")


