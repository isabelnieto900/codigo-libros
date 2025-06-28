# 📚 Organizador de Libros PDF

Herramienta para organizar y gestionar archivos PDF de libros, automatizando el renombrado y la actualización de metadatos.

## 🚀 Características

- ✅ Extracción automática de metadatos de PDFs
- 📝 Renombrado automático con formato estándar
- 🔄 Actualización de metadatos internos
- 🎨 Interfaz colorida e intuitiva
- ⚙️ Configuración flexible

## 📋 Requisitos

- Python 3.8+
- pypdf
- python-dotenv

## 🛠️ Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/codigo-libros.git
cd codigo-libros
```

2. Crea un entorno virtual:
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Configura tu ruta de libros:
```bash
copy .env.example .env
```
Edita `.env` y pon tu ruta real:
```
CARPETA_LIBROS=C:\tu\ruta\a\tus\libros
```

## 🎯 Uso

```bash
python -m src.main
```

## 📁 Estructura del Proyecto

```
codigo-libros/
├── src/                    # Código fuente
│   ├── core/              # Lógica principal
│   ├── ui/                # Interfaz de usuario
│   └── utils/             # Utilidades
├── config/                # Configuración
├── tests/                 # Pruebas
├── .env.example           # Ejemplo de configuración
└── requirements.txt       # Dependencias
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request
