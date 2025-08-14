"""
Módulo que contiene la clase Factura para representar una factura.
"""
from typing import Dict, Any, Optional


class Factura:
    """
    Clase que representa una factura con sus atributos.
    """
    def __init__(self, num_pagina: int, datos: Dict[str, Any]):
        """
        Inicializa una instancia de Factura.
        
        Args:
            num_pagina: Número de página donde se encontró la factura
            datos: Diccionario con los datos de la factura
        """
        self._num_pagina = num_pagina
        self._datos = datos
        self._errores = []
        self._observaciones = []
        self._error_numerico = False
    
    @property
    def num_pagina(self) -> int:
        """Retorna el número de página de la factura."""
        return self._num_pagina
    
    @property
    def datos(self) -> Dict[str, Any]:
        """Retorna los datos de la factura."""
        return self._datos
    
    @property
    def errores(self) -> list:
        """Retorna los errores de la factura."""
        return self._errores
    
    @property
    def observaciones(self) -> list:
        """Retorna las observaciones de la factura."""
        return self._observaciones
    
    @property
    def error_numerico(self) -> int:
        """Retorna si hay error numérico en la factura."""
        return self._error_numerico

    def set_error_numerico(self) -> None:
        """
        Activa el flag de error numérico
        """
        self._error_numerico = True

    def agregar_error(self, error: str) -> None:
        """
        Agrega un error a la factura.
        
        Args:
            error: Descripción del error
        """
        if not self.tiene_errores():
            self._errores.append(f'<<Pag. {self._num_pagina}>> {error}')
        else:
            self._errores.append(f' {error}')
    
    def agregar_observacion(self, observacion: str) -> None:
        """
        Agrega una observación a la factura.
        
        Args:
            observacion: Descripción de la observación
        """
        self._observaciones.append(f'<<Pag. {self._num_pagina}>> {observacion}')
    
    def tiene_errores(self) -> bool:
        """
        Verifica si la factura tiene errores.
        
        Returns:
            True si tiene errores, False en caso contrario
        """
        return len(self._errores) > 0
    
    def get_valor(self, clave: str) -> Any:
        """
        Obtiene un valor específico de la factura.
        
        Args:
            clave: Clave del valor a obtener
            
        Returns:
            Valor asociado a la clave o None si no existe
        """
        return self._datos.get(clave)
    
    def set_valor(self, clave: str, valor: Any) -> None:
        """
        Establece un valor en la factura.
        
        Args:
            clave: Clave del valor a establecer
            valor: Valor a establecer
        """
        self._datos[clave] = valor
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte la factura a un diccionario.
        
        Returns:
            Diccionario con los datos de la factura
        """
        resultado = self._datos.copy()
        if self._errores:
            resultado["Errores"] = ", ".join(self._errores)
        if self._observaciones:
            resultado["Observaciones"] = ", ".join(self._observaciones)
        return resultado
