"""
Configuración principal del programa
"""
import os

# Ruta de la carpeta de libros (usando variable de entorno)
CARPETA_LIBROS = os.getenv('CARPETA_LIBROS', r'C:\ruta\por\defecto\libros')

# Extensiones de archivo válidas
EXTENSIONES_VALIDAS = ['.pdf']

# Configuración de metadatos
METADATOS_REQUERIDOS = ['Author', 'Title', 'CreationDate']

# Patrones de limpieza para nombres de archivo
CARACTERES_PROHIBIDOS = r'[\\/*?:"<>|]'

# Configuración de formato de nombres
FORMATO_NOMBRE = '{autor} - {titulo} ({año}).pdf'
