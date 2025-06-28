"""
Colores y estilos para la interfaz de consola
"""

class Colores:
    """Códigos ANSI para colores en consola"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def colorear(texto, color):
    """Aplica color a un texto"""
    return f"{color}{texto}{Colores.ENDC}"

def negrita(texto):
    """Aplica negrita a un texto"""
    return f"{Colores.BOLD}{texto}{Colores.ENDC}"
