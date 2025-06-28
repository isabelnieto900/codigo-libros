import os
from pypdf import PdfReader, PdfWriter
import re
from datetime import datetime

# =============================================================================
# CONFIGURACIÓN Y CONSTANTES
# =============================================================================

CARPETA = r'C:\Users\laura\OneDrive - Universidad Distrital Francisco José de Caldas\LIBROS2'

# Colores para la consola
class Colores:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def imprimir_titulo():
    """Imprime el título del programa"""
    print(f"\n{Colores.BOLD}{Colores.HEADER}{'='*60}")
    print("📚 ORGANIZADOR DE LIBROS PDF 📚")
    print(f"{'='*60}{Colores.ENDC}")
    print(f"{Colores.OKCYAN}Organizando archivos en: {CARPETA}{Colores.ENDC}\n")

def imprimir_separador():
    """Imprime un separador visual"""
    print(f"{Colores.OKBLUE}{'-'*60}{Colores.ENDC}")

def imprimir_exito(mensaje):
    """Imprime mensaje de éxito en verde"""
    print(f"{Colores.OKGREEN}✓ {mensaje}{Colores.ENDC}")

def imprimir_error(mensaje):
    """Imprime mensaje de error en rojo"""
    print(f"{Colores.FAIL}✗ [ERROR] {mensaje}{Colores.ENDC}")

def imprimir_info(mensaje):
    """Imprime mensaje informativo en azul"""
    print(f"{Colores.OKBLUE}ℹ {mensaje}{Colores.ENDC}")

def imprimir_advertencia(mensaje):
    """Imprime mensaje de advertencia en amarillo"""
    print(f"{Colores.WARNING}⚠ {mensaje}{Colores.ENDC}")

# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def limpiar_texto(texto):
    """Limpia y normaliza texto para nombres de archivo"""
    if texto is None:
        return ''
    texto = texto.strip()
    texto = re.sub(r'[\\/*?:"<>|]', '', texto)
    return texto

def obtener_datos_faltantes(campo, actual, archivo):
    """Solicita datos faltantes al usuario"""
    if actual:
        return actual
    while True:
        entrada = input(f"{Colores.WARNING}📝 [{archivo}] Ingresa {campo}: {Colores.ENDC}").strip()
        if entrada:
            return limpiar_texto(entrada)
        respuesta = input(f"{Colores.FAIL}⚠ Campo vacío. ¿Usar 'Desconocido_{campo}'? (s/n): {Colores.ENDC}").strip().lower()
        if respuesta == 's':
            return f'Desconocido_{campo}'

def mostrar_metadatos(ruta):
    """Muestra los metadatos del PDF de forma organizada"""
    try:
        reader = PdfReader(ruta)
        info = reader.metadata
        
        print(f"\n{Colores.BOLD}{Colores.OKCYAN}📋 METADATOS DEL ARCHIVO{Colores.ENDC}")
        print(f"{Colores.OKCYAN}{'='*40}{Colores.ENDC}")
        
        if info:
            for clave, valor in info.items():
                clave_limpia = clave.replace('/', '').replace('_', ' ').title()
                print(f"{Colores.OKBLUE}{clave_limpia:15}{Colores.ENDC}: {valor}")
        else:
            imprimir_advertencia("No se encontraron metadatos en el archivo")
        
        print(f"{Colores.OKCYAN}{'='*40}{Colores.ENDC}\n")
    except Exception as e:
        imprimir_error(f"No se pudieron leer los metadatos: {e}")

def mostrar_menu_principal():
    """Muestra el menú principal de opciones"""
    print(f"\n{Colores.BOLD}¿Qué deseas hacer con este libro?{Colores.ENDC}")
    print(f"{Colores.OKGREEN}[C]{Colores.ENDC} Continuar procesando")
    print(f"{Colores.WARNING}[O]{Colores.ENDC} Omitir archivo")
    print(f"{Colores.OKBLUE}[V]{Colores.ENDC} Ver metadatos completos")
    return input(f"{Colores.BOLD}Opción: {Colores.ENDC}").strip().lower()

def mostrar_menu_metadatos():
    """Muestra el menú para manejar metadatos encontrados"""
    print(f"\n{Colores.BOLD}¿Cómo proceder con los metadatos encontrados?{Colores.ENDC}")
    print(f"{Colores.OKGREEN}[S]{Colores.ENDC} Usar nombre sugerido")
    print(f"{Colores.WARNING}[E]{Colores.ENDC} Editar datos manualmente")
    print(f"{Colores.FAIL}[N]{Colores.ENDC} Ingresar datos desde cero")
    print(f"{Colores.OKBLUE}[V]{Colores.ENDC} Ver metadatos completos")
    return input(f"{Colores.BOLD}Opción: {Colores.ENDC}").strip().lower()

def mostrar_menu_post_proceso():
    """Muestra el menú después de procesar un archivo"""
    print(f"\n{Colores.BOLD}¿Qué deseas hacer ahora?{Colores.ENDC}")
    print(f"{Colores.OKGREEN}[C]{Colores.ENDC} Continuar con el siguiente archivo")
    print(f"{Colores.OKBLUE}[V]{Colores.ENDC} Ver metadatos actualizados")
    print(f"{Colores.WARNING}[R]{Colores.ENDC} Recorregir datos de este archivo")
    print(f"{Colores.FAIL}[S]{Colores.ENDC} Salir del programa")
    return input(f"{Colores.BOLD}Opción: {Colores.ENDC}").strip().lower()

def extraer_año_fecha(fecha):
    """Extrae el año de una fecha de metadatos"""
    if not fecha:
        return ''
    match = re.search(r'D:(\d{4})', fecha)
    return match.group(1) if match else ''

def mostrar_info_archivo(nombre, autor, titulo, año):
    """Muestra la información extraída del archivo de forma organizada"""
    print(f"\n{Colores.BOLD}{Colores.HEADER}📄 {nombre}{Colores.ENDC}")
    print(f"{Colores.OKBLUE}Autor:  {Colores.ENDC}{autor or f'{Colores.FAIL}NO ENCONTRADO{Colores.ENDC}'}")
    print(f"{Colores.OKBLUE}Título: {Colores.ENDC}{titulo or f'{Colores.FAIL}NO ENCONTRADO{Colores.ENDC}'}")
    print(f"{Colores.OKBLUE}Año:    {Colores.ENDC}{año or f'{Colores.FAIL}NO ENCONTRADO{Colores.ENDC}'}")

def actualizar_metadatos_pdf(ruta, autor, titulo, año):
    """Actualiza los metadatos internos del PDF"""
    try:
        reader = PdfReader(ruta)
        writer = PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
        
        writer.add_metadata({
            "/Author": autor,
            "/Title": titulo,
            "/CreationDate": f"D:{año}0101000000",
            "/ModDate": f"D:{datetime.now().strftime('%Y%m%d%H%M%S')}"
        })
        
        with open(ruta, "wb") as f_out:
            writer.write(f_out)
        
        return True
    except Exception as e:
        imprimir_error(f"No se pudieron actualizar los metadatos: {e}")
        return False

def confirmar_continuar():
    """Pregunta si continuar con el siguiente archivo"""
    respuesta = input(f"{Colores.WARNING}¿Continuar con el siguiente libro? (s/n): {Colores.ENDC}").strip().lower()
    return respuesta == 's'

# =============================================================================
# PROGRAMA PRINCIPAL
# =============================================================================

def main():
    imprimir_titulo()
    
    # Verificar que la carpeta existe
    if not os.path.exists(CARPETA):
        imprimir_error(f"La carpeta no existe: {CARPETA}")
        return
    
    archivos_pdf = [f for f in os.listdir(CARPETA) if f.lower().endswith('.pdf')]
    
    if not archivos_pdf:
        imprimir_advertencia("No se encontraron archivos PDF en la carpeta")
        return
    
    imprimir_info(f"Se encontraron {len(archivos_pdf)} archivos PDF para procesar")
    imprimir_separador()
    
    archivos_procesados = 0
    archivos_omitidos = 0
    
    for nombre_archivo in archivos_pdf:
        ruta = os.path.join(CARPETA, nombre_archivo)
        
        try:
            reader = PdfReader(ruta)
            info = reader.metadata
            
            # Extraer metadatos
            autor = limpiar_texto(info.get('/Author', ''))
            titulo = limpiar_texto(info.get('/Title', ''))
            fecha = limpiar_texto(info.get('/CreationDate', ''))
            año = extraer_año_fecha(fecha)
            
            # Mostrar información del archivo
            mostrar_info_archivo(nombre_archivo, autor, titulo, año)
            
            # Menú principal
            while True:
                decision = mostrar_menu_principal()
                
                if decision == 'o':
                    imprimir_advertencia("Archivo omitido")
                    archivos_omitidos += 1
                    break
                elif decision == 'v':
                    mostrar_metadatos(ruta)
                elif decision == 'c':
                    break
                else:
                    imprimir_error("Opción no válida")
            
            if decision == 'o':
                if not confirmar_continuar():
                    break
                continue
            
            # Procesar archivo
            if autor and titulo and año:
                sugerido = f'{autor} - {titulo} ({año}).pdf'
                print(f"\n{Colores.OKGREEN}💡 Nombre sugerido: {Colores.BOLD}{sugerido}{Colores.ENDC}")
                
                while True:
                    usar = mostrar_menu_metadatos()
                    
                    if usar == 'v':
                        mostrar_metadatos(ruta)
                    elif usar == 'e':
                        autor = input(f"Autor [{autor}]: ").strip() or autor
                        titulo = input(f"Título [{titulo}]: ").strip() or titulo
                        año = input(f"Año [{año}]: ").strip() or año
                        break
                    elif usar == 'n':
                        autor = obtener_datos_faltantes('autor', '', nombre_archivo)
                        titulo = obtener_datos_faltantes('título', '', nombre_archivo)
                        año = obtener_datos_faltantes('año', '', nombre_archivo)
                        break
                    elif usar == 's':
                        break
                    else:
                        imprimir_error("Opción no válida")
            else:
                imprimir_info("Completando datos faltantes...")
                autor = obtener_datos_faltantes('autor', autor, nombre_archivo)
                titulo = obtener_datos_faltantes('título', titulo, nombre_archivo)
                año = obtener_datos_faltantes('año', año, nombre_archivo)
            
            # Generar nuevo nombre
            nuevo_nombre = f'{autor} - {titulo} ({año}).pdf'
            nueva_ruta = os.path.join(CARPETA, nuevo_nombre)
            
            # Renombrar archivo si es necesario
            if nombre_archivo != nuevo_nombre:
                os.rename(ruta, nueva_ruta)
                imprimir_exito(f"Renombrado: {nombre_archivo} → {nuevo_nombre}")
            else:
                imprimir_info("El archivo ya tiene el nombre correcto")
            
            # Actualizar metadatos
            if actualizar_metadatos_pdf(nueva_ruta, autor, titulo, año):
                imprimir_exito("Metadatos actualizados correctamente")
            
            archivos_procesados += 1
            
            # Menú post-proceso
            while True:
                post_accion = mostrar_menu_post_proceso()
                
                if post_accion == 'v':
                    mostrar_metadatos(nueva_ruta)
                elif post_accion == 'c':
                    break
                elif post_accion == 's':
                    print(f"\n{Colores.BOLD}👋 ¡Hasta luego!{Colores.ENDC}")
                    return
                elif post_accion == 'r':
                    print(f"\n{Colores.WARNING}📝 Corrigiendo datos...{Colores.ENDC}")
                    autor = input(f"Autor [{autor}]: ").strip() or autor
                    titulo = input(f"Título [{titulo}]: ").strip() or titulo
                    año = input(f"Año [{año}]: ").strip() or año
                    
                    nuevo_nombre_corregido = f'{autor} - {titulo} ({año}).pdf'
                    nueva_ruta_corregida = os.path.join(CARPETA, nuevo_nombre_corregido)
                    
                    if os.path.basename(nueva_ruta) != nuevo_nombre_corregido:
                        os.rename(nueva_ruta, nueva_ruta_corregida)
                        imprimir_exito(f"Renombrado: {os.path.basename(nueva_ruta)} → {nuevo_nombre_corregido}")
                        nueva_ruta = nueva_ruta_corregida
                    
                    if actualizar_metadatos_pdf(nueva_ruta, autor, titulo, año):
                        imprimir_exito("Metadatos corregidos")
                else:
                    imprimir_error("Opción no válida")
        
        except Exception as e:
            imprimir_error(f"{nombre_archivo}: {e}")
            if not confirmar_continuar():
                break
        
        imprimir_separador()
    
    # Resumen final
    print(f"\n{Colores.BOLD}{Colores.HEADER}📊 RESUMEN FINAL{Colores.ENDC}")
    print(f"{Colores.OKGREEN}✓ Archivos procesados: {archivos_procesados}{Colores.ENDC}")
    print(f"{Colores.WARNING}⚠ Archivos omitidos: {archivos_omitidos}{Colores.ENDC}")
    print(f"{Colores.BOLD}🎉 ¡Proceso completado!{Colores.ENDC}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colores.WARNING}⚠ Proceso interrumpido por el usuario{Colores.ENDC}")
    except Exception as e:
        imprimir_error(f"Error inesperado: {e}")
