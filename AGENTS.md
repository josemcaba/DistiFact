# AGENTS.md — DistiFact

Python + Tkinter app that reads supplier invoices in PDF/Excel format and generates
an Excel file with the fiscal data needed to account for each invoice (base, IVA
quota, IRPF, Recargo de Equiparabilidad, totals, NIF, etc.). Invoices are
extracted via regex (PDF-text / Excel) or OCR (PDF-image), then verified and
validated for arithmetic correctness before export.

## Entry point


```bash
python main.py
```

`DistiFact_GUI.py` was removed (dead code, never imported).

## Architecture (MVC)

```
controlador/     → Controlador (orquesta modelo + vista)
modelo/          → ProcesadorFacturas, ClasificadorFacturas, VerificadorFactura,
                   ExportadorExcel, ft_basicas, ExtractorImagenes, ExtractorTexto
vista/           → App(tk.Tk) + 4 navegable frames
extractores/     → 19 módulos dinámicos (uno por empresa)
datos/           → empresas.json, rectangulos.json (ROI + Tesseract config)
tests/           → 63 tests (pytest)
```

Each extractor module must define:
- `identificador` (str): text filter for valid PDF pages.
- `extraerDatosFactura(pagina, empresa)` → returns `[num_pag, dict]` or `[dict1, dict2, ...]`.

## Key commands

```bash
python3 -m pytest tests/ -v          # run all 63 tests
python3 main.py                       # start GUI (requires $DISPLAY)
```

No linter, typechecker, or formatter is configured. Run `pytest` before committing.

## Dependencies

System: Tesseract OCR (`apt install tesseract-ocr`), poppler (optional).

Python (see `requirements.txt`):
- pdfplumber, PyMuPDF (fitz), PyPDF2
- pytesseract, opencv-python, pillow, numpy, screeninfo
- openpyxl, pandas

## Conventions

- Extractores import `ft_basicas` as `fb` (unified alias).
- Modelo uses `logging.getLogger(__name__)` — no bare `print()` in fallback paths.
- `Controlador._mensaje_callback` is initialized in `__init__` and set via `configurar_callbacks()`.

## Gotchas

- `empresas.json` keys are strings that become `int` IDs.
- `rectangulos.json` NIF keys must match exactly (e.g. `"A17001231"`, not `"ES A17001231"`).
- `frame_proceso.py` calls `controlador.obtener_ruta_archivo()` which may return `None` — guard with `if not ruta_archivo` before `len()`.
