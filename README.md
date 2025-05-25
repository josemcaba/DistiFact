# Documentación de Refactorización de DistiFact-GUI a OOP con Tkinter

## Introducción

Este documento describe la refactorización completa de la aplicación DistiFact-GUI, transformándola de una aplicación de consola a una aplicación gráfica utilizando Tkinter y siguiendo rigurosamente el paradigma de programación orientada a objetos (OOP).

## Cambios Principales

1. **Arquitectura Modelo-Vista-Controlador (MVC)**
   - Separación clara entre la lógica de negocio (Modelo), la interfaz de usuario (Vista) y la coordinación (Controlador)
   - Estructura de directorios organizada por responsabilidades

2. **Programación Orientada a Objetos**
   - Conversión de funciones procedurales a clases con responsabilidades específicas
   - Encapsulamiento de datos y comportamientos
   - Uso de propiedades y métodos para acceso controlado a atributos
   - Implementación de herencia para reutilización de código

3. **Interfaz Gráfica con Tkinter**
   - Reemplazo de interacciones por consola con componentes gráficos
   - Implementación de navegación entre pantallas
   - Visualización de datos en tablas y controles gráficos
   - Manejo de eventos de usuario a través de callbacks

4. **Mejoras Adicionales**
   - Procesamiento asíncrono para operaciones largas
   - Manejo mejorado de errores y excepciones
   - Validación de datos de entrada
   - Feedback visual del progreso de operaciones

## Estructura del Proyecto

```
DistiFact-OOP-Tkinter/
├── modelo/                  # Lógica de negocio
│   ├── __init__.py
│   ├── empresa.py           # Clases Empresa y EmpresaManager
│   ├── factura.py           # Clase Factura
│   ├── procesador.py        # Clase ProcesadorFacturas
│   ├── clasificador.py      # Clase ClasificadorFacturas
│   └── exportador.py        # Clase ExportadorExcel
├── vista/                   # Interfaz gráfica
│   ├── __init__.py
│   ├── app.py               # Ventana principal
│   ├── frame_base.py        # Clase base para frames
│   ├── frame_empresa.py     # Selección de empresa
│   ├── frame_archivo.py     # Selección de archivo
│   ├── frame_proceso.py     # Procesamiento
│   └── frame_resultados.py  # Visualización de resultados
├── controlador/             # Coordinación
│   ├── __init__.py
│   └── controlador.py       # Clase Controlador
├── main.py                  # Punto de entrada
├── test_distifact.py        # Pruebas unitarias
└── [archivos auxiliares]    # Módulos y datos originales
```

## Clases Principales

### Modelo

1. **Empresa**: Representa una empresa con sus atributos (id, nombre, nif, tipo, funciones)
2. **EmpresaManager**: Gestiona la carga y manipulación de empresas desde JSON
3. **Factura**: Representa una factura con sus datos, errores y observaciones
4. **ProcesadorFacturas**: Procesa archivos PDF o Excel para extraer facturas
5. **ClasificadorFacturas**: Clasifica facturas en correctas y con errores
6. **ExportadorExcel**: Exporta facturas a archivos Excel

### Vista

1. **App**: Ventana principal que gestiona la navegación entre frames
2. **FrameBase**: Clase base para todos los frames de la aplicación
3. **FrameSeleccionEmpresa**: Permite seleccionar una empresa
4. **FrameSeleccionArchivo**: Permite seleccionar un archivo a procesar
5. **FrameProcesamiento**: Muestra el progreso del procesamiento
6. **FrameResultados**: Muestra los resultados del procesamiento

### Controlador

1. **Controlador**: Coordina la interacción entre el modelo y la vista

## Flujo de la Aplicación

1. La aplicación inicia mostrando el frame de selección de empresa
2. El usuario selecciona una empresa y avanza al frame de selección de archivo
3. El usuario selecciona un archivo y confirma para iniciar el procesamiento
4. La aplicación muestra el progreso del procesamiento en tiempo real
5. Al completar el procesamiento, se muestran los resultados en tablas
6. El usuario puede exportar los resultados a Excel o iniciar una nueva consulta

## Requisitos

- Python 3.6 o superior
- Tkinter (incluido en la mayoría de instalaciones de Python)
- Bibliotecas: pdfplumber, PyMuPDF (fitz), pandas, openpyxl

## Instalación de Dependencias

```bash
pip install pdfplumber PyMuPDF pandas openpyxl
```

## Ejecución

```bash
python main.py
```

## Notas Adicionales

- Se mantiene la compatibilidad con los archivos de datos existentes (empresas.json, rectangulos.json)
- Los módulos extractores específicos de cada empresa se utilizan sin modificaciones
- La aplicación es más robusta ante errores y proporciona mejor feedback al usuario
- La interfaz gráfica mejora significativamente la experiencia de usuario
