"""
Paquete de extractores de facturas.

Cada extractor es un módulo independiente que define:
  - ``identificador`` (str): texto que debe aparecer en la página para
    considerarse una factura válida. Las páginas que no contengan este
    texto son descartadas durante el pre-procesamiento.

  - ``extraerDatosFactura(pagina, empresa)`` -> list | tuple
    Extrae los datos de la factura. ``pagina`` es una lista/tupla donde
    ``pagina[0]`` es el número de página (int) y ``pagina[1]`` es el
    contenido textual de la página (str).

    Formatos de retorno soportados:
      1. **[dict, ...]** — Lista de diccionarios (un IVA por dict).
         Usado por extractores con múltiples desgloses de IVA (ej. MERCADONA).
      2. **[num_pag, dict]** — Lista con número de página y diccionario.
         Formato legacy, soportado pero obsoleto.
      3. **[dict]** — Lista con un único diccionario.

    El diccionario de factura usa las claves definidas en
    ``extractores.conceptos_factura`` (KEY).

Cada extractor se carga dinámicamente desde ``modelo/procesador.py``
usando el nombre especificado en ``datos/empresas.json``.
"""
