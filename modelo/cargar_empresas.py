"""
Módulo que contiene las clases relacionadas con la gestión de empresas.
"""
import json
from typing import Dict, Optional, Tuple, Any
from pathlib import Path

class Empresa:
    def __init__(self, id_empresa: int, nombre: str, nif: str, tipo: str, funciones: str):
        """
        Inicializa una instancia de Empresa.
        
        Args:
            id_empresa: Identificador único de la empresa
            nombre: Nombre de la empresa
            nif: NIF de la empresa
            tipo: Tipo de documento que maneja (PDFtexto, PDFimagen, excel)
            funciones: Nombre del módulo que contiene las funciones extractoras
        """
        self._id = id_empresa
        self._nombre = nombre
        self._nif = nif
        self._tipo = tipo
        self._funciones = funciones
    
    @property
    def id(self) -> int:
        """Retorna el ID de la empresa."""
        return self._id
    
    @property
    def nombre(self) -> str:
        """Retorna el nombre de la empresa."""
        return self._nombre
    
    @property
    def nif(self) -> str:
        """Retorna el NIF de la empresa."""
        return self._nif
    
    @property
    def tipo(self) -> str:
        """Retorna el tipo de documento que maneja la empresa."""
        return self._tipo
    
    @property
    def funciones(self) -> str:
        """Retorna el nombre del módulo de funciones extractoras."""
        return self._funciones
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte la instancia a un diccionario.
        
        Returns:
            Diccionario con los atributos de la empresa
        """
        return {
            "id": self._id,
            "nombre": self._nombre,
            "nif": self._nif,
            "tipo": self._tipo,
            "funciones": self._funciones
        }
    
    def to_tuple(self) -> Tuple:
        """
        Convierte la instancia a una tupla.
        
        Returns:
            Tupla con los atributos de la empresa
        """ 
        return tuple((
            self._id,
            self._nif,
            self._nombre,
            self._tipo,
            self._funciones))
    
    def __str__(self) -> str:
        """Representación en cadena de la empresa."""
        return f"{self._nombre} ({self._nif})"


class EmpresasManager:
    """
    Clase que gestiona la carga y manipulación de empresas.
    """
    def __init__(self):
        """Inicializa el gestor de empresas con un diccionario vacío."""
        self._empresas = {}
    
    def cargar_empresas(self, file_json) -> bool:
        """
        Carga las empresas desde un archivo JSON.
        
        Args:
            ruta_json: Ruta al archivo JSON con los datos de empresas
            
        Returns:
            True si la carga fue exitosa, False en caso contrario
        """
        try:
            self.ruta_json = Path("datos") / Path(file_json)
            with open(self.ruta_json, 'r', encoding='utf-8') as archivo:
                datos_json = json.load(archivo)
            
            # Convertimos la key a entero y creamos objetos Empresa
            self._empresas = {}
            for key, values in datos_json.items():
                id_empresa = int(key)
                self._empresas[id_empresa] = Empresa(
                    id_empresa=id_empresa,
                    nombre=values['nombre'],
                    nif=values['nif'],
                    tipo=values['tipo'],
                    funciones=values['funciones']
                )
            return True       
        except:
            return False

    
    def seleccionar_empresa(self, id_empresa: int) -> Optional[Empresa]:
        """
        Obtiene una empresa por su ID.
        
        Args:
            id_empresa: ID de la empresa a obtener
            
        Returns:
            Instancia de Empresa si existe, None en caso contrario
        """
        return self._empresas.get(id_empresa)
    
    def listar_empresas(self) -> Tuple:
        """
        Retorna el listado de empresas.
        
        Returns:
            Tuplas con las empresas cargadas
        """

        self._listado = []
        for empresa in self._empresas.values():
            self._listado.append(empresa.to_tuple())
        return self._listado
    
    def __len__(self) -> int:
        """Retorna la cantidad de empresas cargadas."""
        return len(self._empresas)
