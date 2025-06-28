"""
Gestión de archivos PDF y sus metadatos
"""
from pypdf import PdfReader, PdfWriter
from datetime import datetime
import os
from ..ui.display import imprimir_error, imprimir_advertencia
from ..ui.colors import Colores, colorear, negrita

class PDFManager:
    """Manejador de archivos PDF"""
    
    def __init__(self):
        pass
    
    def leer_metadatos(self, ruta):
        """Lee los metadatos de un archivo PDF"""
        try:
            reader = PdfReader(ruta)
            return reader.metadata or {}
        except Exception as e:
            imprimir_error(f"Error al leer metadatos: {e}")
            return {}
    
    def mostrar_metadatos(self, ruta):
        """Muestra los metadatos del PDF de forma organizada"""
        try:
            metadatos = self.leer_metadatos(ruta)
            
            print(f"\n{negrita(colorear('📋 METADATOS DEL ARCHIVO', Colores.OKCYAN))}")
            print(f"{colorear('='*40, Colores.OKCYAN)}")
            
            if metadatos:
                for clave, valor in metadatos.items():
                    clave_limpia = clave.replace('/', '').replace('_', ' ').title()
                    print(f"{colorear(f'{clave_limpia:15}', Colores.OKBLUE)}: {valor}")
            else:
                imprimir_advertencia("No se encontraron metadatos en el archivo")
            
            print(f"{colorear('='*40, Colores.OKCYAN)}\n")
        except Exception as e:
            imprimir_error(f"No se pudieron mostrar los metadatos: {e}")
    
    def actualizar_metadatos(self, ruta, autor, titulo, año, edicion):
        """Actualiza los metadatos internos del PDF"""
        try:
            reader = PdfReader(ruta)
            writer = PdfWriter()
            
            for page in reader.pages:
                writer.add_page(page)
            
            writer.add_metadata({
                "/Author": autor,
                "/Title": titulo,
                "/Subject": f"Edición: {edicion}" if edicion else "",
                "/CreationDate": f"D:{año}0101000000",
                "/ModDate": f"D:{datetime.now().strftime('%Y%m%d%H%M%S')}"
            })
            
            with open(ruta, "wb") as f_out:
                writer.write(f_out)
            
            return True
        except Exception as e:
            imprimir_error(f"No se pudieron actualizar los metadatos: {e}")
            return False
    
    def extraer_info_basica(self, ruta):
        """Extrae información básica del PDF"""
        from ..utils.text_utils import limpiar_texto, extraer_año_fecha
        
        metadatos = self.leer_metadatos(ruta)
        
        autor = limpiar_texto(metadatos.get('/Author', ''))
        titulo = limpiar_texto(metadatos.get('/Title', ''))
        fecha = limpiar_texto(metadatos.get('/CreationDate', ''))
        año = extraer_año_fecha(fecha)
        
        return autor, titulo, año
