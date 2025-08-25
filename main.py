"""
Punto de entrada principal de la aplicación
"""
import os
import sys
from app import App

# Agregar directorio actual al path para importaciones
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
