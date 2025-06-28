"""
Programa principal del organizador de libros PDF
"""
import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import CARPETA_LIBROS
from .core.pdf_manager import PDFManager
from .core.file_manager import FileManager
from .ui.display import *
from .ui.menus import *
from .utils.validators import obtener_archivos_pdf, validar_carpeta
from .utils.text_utils import generar_nombre_archivo, limpiar_texto

class OrganizadorLibros:
    """Clase principal del organizador de libros"""
    
    def __init__(self):
        self.pdf_manager = PDFManager()
        self.file_manager = FileManager()
        self.archivos_procesados = 0
        self.archivos_omitidos = 0
    
    def obtener_datos_faltantes(self, campo, actual, archivo, requerido=True):
        """Solicita datos faltantes al usuario"""
        if actual:
            return actual
        
        while True:
            entrada = input(f"📝 [{archivo}] Ingresa {campo} (Enter para omitir): ").strip()
            
            if entrada:
                return limpiar_texto(entrada)
            
            # Si no es requerido, permitir campo vacío
            if not requerido:
                return ""
            
            # Si es requerido, preguntar si usar "Desconocido"
            if confirmar_accion(f"Campo vacío. ¿Usar 'Desconocido_{campo}'?"):
                return f'Desconocido_{campo}'
    
    def procesar_archivo(self, ruta, nombre_archivo):
        """Procesa un archivo PDF individual"""
        try:
            # Extraer información básica
            autor, titulo, año = self.pdf_manager.extraer_info_basica(ruta)
            edicion = ""

            # Mostrar información del archivo
            mostrar_info_archivo(nombre_archivo, autor, titulo, año, edicion)

            # Menú principal
            while True:
                decision = mostrar_menu_principal()

                if decision == 'o':
                    imprimir_advertencia("Archivo omitido")
                    self.archivos_omitidos += 1
                    return True  # Continúa automáticamente al siguiente archivo
                elif decision == 'v':
                    self.pdf_manager.mostrar_metadatos(ruta)
                elif decision == 'c':
                    break
                else:
                    imprimir_error("Opción no válida")
            
            # Procesar metadatos
            if autor and titulo and año:
                sugerido = generar_nombre_archivo(autor, titulo, año)  # Actualiza para incluir edicion si quieres
                print(f"\n💡 Nombre sugerido: {negrita(sugerido)}")

                while True:
                    usar = mostrar_menu_metadatos()

                    if usar == 'v':
                        self.pdf_manager.mostrar_metadatos(ruta)
                    elif usar == 'e':
                        autor = input(f"Autor [{autor}]: ").strip() or autor
                        titulo = input(f"Título [{titulo}]: ").strip() or titulo
                        año = input(f"Año [{año}]: ").strip() or año
                        edicion = input(f"Edición [{edicion}]: ").strip() or edicion
                        break
                    elif usar == 'n':
                        autor = self.obtener_datos_faltantes('autor', '', nombre_archivo)
                        titulo = self.obtener_datos_faltantes('título', '', nombre_archivo)
                        año = self.obtener_datos_faltantes('año', '', nombre_archivo)
                        edicion = self.obtener_datos_faltantes('edición', '', nombre_archivo, requerido=False)
                        break
                    elif usar == 's':
                        break
                    else:
                        imprimir_error("Opción no válida")
            else:
                imprimir_info("Completando datos faltantes...")
                autor = self.obtener_datos_faltantes('autor', autor, nombre_archivo)
                titulo = self.obtener_datos_faltantes('título', titulo, nombre_archivo)
                año = self.obtener_datos_faltantes('año', año, nombre_archivo)
                edicion = self.obtener_datos_faltantes('edición', '', nombre_archivo, requerido=False)

            # Renombrar archivo
            nuevo_nombre = generar_nombre_archivo(autor, titulo, año, edicion)
            nueva_ruta = self.file_manager.renombrar_archivo(ruta, nuevo_nombre)

            # Actualizar metadatos
            if self.pdf_manager.actualizar_metadatos(nueva_ruta, autor, titulo, año, edicion):
                imprimir_exito("Metadatos actualizados correctamente")

            self.archivos_procesados += 1

            # Menú post-proceso
            return self.manejar_post_proceso(nueva_ruta, autor, titulo, año, edicion)

        except Exception as e:
            imprimir_error(f"{nombre_archivo}: {e}")
            return True  # Continúa automáticamente al siguiente archivo
    
    def manejar_post_proceso(self, ruta, autor, titulo, año, edicion):
        """Maneja las acciones después de procesar un archivo"""
        while True:
            post_accion = mostrar_menu_post_proceso()
            
            if post_accion == 'v':
                self.pdf_manager.mostrar_metadatos(ruta)
            elif post_accion == 'c':
                return True
            elif post_accion == 's':
                print(f"\n{negrita('👋 ¡Hasta luego!')}")
                return False
            elif post_accion == 'r':
                print(f"\n📝 Corrigiendo datos...")
                autor = input(f"Autor [{autor}]: ").strip() or autor
                titulo = input(f"Título [{titulo}]: ").strip() or titulo
                año = input(f"Año [{año}]: ").strip() or año
                edicion = input(f"Edición [{edicion}]: ").strip() or edicion

                nuevo_nombre = generar_nombre_archivo(autor, titulo, año, edicion)
                nueva_ruta = self.file_manager.renombrar_archivo(ruta, nuevo_nombre)

                if self.pdf_manager.actualizar_metadatos(nueva_ruta, autor, titulo, año, edicion):
                    imprimir_exito("Metadatos corregidos")

                ruta = nueva_ruta
            else:
                imprimir_error("Opción no válida")
    
    def ejecutar(self):
        """Ejecuta el programa principal"""
        imprimir_titulo(CARPETA_LIBROS)
        
        # Verificar carpeta
        if not validar_carpeta(CARPETA_LIBROS):
            imprimir_error(f"La carpeta no existe: {CARPETA_LIBROS}")
            return
        
        # Obtener archivos PDF
        archivos_pdf = obtener_archivos_pdf(CARPETA_LIBROS)
        
        if not archivos_pdf:
            imprimir_advertencia("No se encontraron archivos PDF en la carpeta")
            return
        
        imprimir_info(f"Se encontraron {len(archivos_pdf)} archivos PDF para procesar")
        imprimir_separador()
        
        # Procesar archivos
        for nombre_archivo in archivos_pdf:
            ruta = os.path.join(CARPETA_LIBROS, nombre_archivo)
            
            if not self.procesar_archivo(ruta, nombre_archivo):
                break
            
            imprimir_separador()
        
        # Mostrar resumen
        mostrar_resumen_final(self.archivos_procesados, self.archivos_omitidos)

def main():
    """Función principal"""
    try:
        organizador = OrganizadorLibros()
        organizador.ejecutar()
    except KeyboardInterrupt:
        print(f"\n\n⚠ Proceso interrumpido por el usuario")
    except Exception as e:
        imprimir_error(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()
