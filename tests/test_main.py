"""
Pruebas unitarias para el organizador de libros
"""
import unittest
import os
import sys

# Agregar el directorio raíz al path para las importaciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.text_utils import limpiar_texto, extraer_año_fecha, generar_nombre_archivo
from src.utils.validators import validar_archivo_pdf, validar_datos_libro

class TestTextUtils(unittest.TestCase):
    """Pruebas para utilidades de texto"""
    
    def test_limpiar_texto(self):
        """Prueba la limpieza de texto"""
        self.assertEqual(limpiar_texto('Texto|Normal'), 'TextoNormal')
        self.assertEqual(limpiar_texto('Texto con "comillas"'), 'Texto con comillas')
        self.assertEqual(limpiar_texto(None), '')
        self.assertEqual(limpiar_texto('  Texto con espacios  '), 'Texto con espacios')
    
    def test_extraer_año_fecha(self):
        """Prueba la extracción de año de fechas"""
        self.assertEqual(extraer_año_fecha('D:20230101120000'), '2023')
        self.assertEqual(extraer_año_fecha('D:19991231235959'), '1999')
        self.assertEqual(extraer_año_fecha(''), '')
        self.assertEqual(extraer_año_fecha(None), '')
    
    def test_generar_nombre_archivo(self):
        """Prueba la generación de nombres de archivo"""
        nombre = generar_nombre_archivo('García Márquez', 'Cien años de soledad', '1967')
        self.assertEqual(nombre, 'García Márquez - Cien años de soledad (1967).pdf')

class TestValidators(unittest.TestCase):
    """Pruebas para validadores"""
    
    def test_validar_archivo_pdf(self):
        """Prueba la validación de archivos PDF"""
        self.assertTrue(validar_archivo_pdf('libro.pdf'))
        self.assertTrue(validar_archivo_pdf('LIBRO.PDF'))
        self.assertFalse(validar_archivo_pdf('archivo.txt'))
        self.assertFalse(validar_archivo_pdf('imagen.jpg'))
    
    def test_validar_datos_libro(self):
        """Prueba la validación de datos de libro"""
        self.assertTrue(validar_datos_libro('Autor', 'Título', '2023'))
        self.assertFalse(validar_datos_libro('', 'Título', '2023'))
        self.assertFalse(validar_datos_libro('Autor', '', '2023'))
        self.assertFalse(validar_datos_libro('Autor', 'Título', ''))

if __name__ == '__main__':
    unittest.main()
