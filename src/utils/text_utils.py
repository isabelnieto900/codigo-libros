"""
Utilidades para manejo de texto
"""
import re
from config.settings import CARACTERES_PROHIBIDOS

def limpiar_texto(texto):
    """Limpia y normaliza texto para nombres de archivo"""
    if texto is None:
        return ''
    texto = texto.strip()
    texto = re.sub(CARACTERES_PROHIBIDOS, '', texto)
    return texto

def extraer_año_fecha(fecha):
    """Extrae el año de una fecha de metadatos"""
    if not fecha:
        return ''
    match = re.search(r'D:(\d{4})', fecha)
    return match.group(1) if match else ''

def generar_nombre_archivo(autor, titulo, año, edicion=None):
    """Genera un nombre de archivo estandarizado"""
    nombre = f'{autor} - {titulo}'
    if edicion and edicion.strip():  # Solo agrega edición si no está vacía
        nombre += f' ({edicion} ed.)'
    nombre += f' ({año}).pdf'
    return nombre

def validar_año(año):
    """Valida que el año sea un número de 4 dígitos"""
    if not año:
        return False
    return bool(re.match(r'^\d{4}$', str(año)))
