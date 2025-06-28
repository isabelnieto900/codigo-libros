"""
Gestión de archivos y directorios
"""
import os
from ..ui.display import imprimir_exito, imprimir_error, imprimir_info

class FileManager:
    """Manejador de archivos y directorios"""
    
    def __init__(self):
        pass
    
    def renombrar_archivo(self, ruta_actual, nuevo_nombre):
        """Renombra un archivo"""
        try:
            directorio = os.path.dirname(ruta_actual)
            nueva_ruta = os.path.join(directorio, nuevo_nombre)
            
            if ruta_actual == nueva_ruta:
                imprimir_info("El archivo ya tiene el nombre correcto")
                return nueva_ruta
            
            os.rename(ruta_actual, nueva_ruta)
            nombre_actual = os.path.basename(ruta_actual)
            imprimir_exito(f"Renombrado: {nombre_actual} → {nuevo_nombre}")
            return nueva_ruta
        except Exception as e:
            imprimir_error(f"Error al renombrar archivo: {e}")
            return ruta_actual
    
    def verificar_archivo_existe(self, ruta):
        """Verifica si un archivo existe"""
        return os.path.exists(ruta) and os.path.isfile(ruta)
    
    def obtener_nombre_archivo(self, ruta):
        """Obtiene el nombre del archivo sin la ruta"""
        return os.path.basename(ruta)
    
    def obtener_directorio(self, ruta):
        """Obtiene el directorio de un archivo"""
        return os.path.dirname(ruta)
