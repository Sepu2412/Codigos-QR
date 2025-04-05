# Proyecto: Aplicación de Gestión de Códigos QR

## Introducción

Los códigos QR se han convertido en una herramienta esencial para compartir información de manera rápida y eficiente. Se utilizan ampliamente en distintos contextos como accesos a eventos, pagos digitales, redes Wi-Fi, menús interactivos, entre otros.

Este proyecto tiene como objetivo desarrollar una aplicación de escritorio que permita generar, leer y gestionar códigos QR mediante una interfaz gráfica intuitiva, incluyendo funcionalidades como historial, exportación, personalización y validaciones.

---

## Descripción General del Proyecto

La aplicación permite crear códigos QR personalizados con información variada como URLs, textos, contactos y credenciales Wi-Fi. También permite escanear códigos desde una imagen o cámara en tiempo real.  
Todos los QR procesados (generados o leídos) se almacenan en un historial, el cual puede ser consultado, filtrado o exportado por el usuario.

---

## Funcionalidades Principales

1. **Generación de Códigos QR**: Creación de códigos a partir de diferentes tipos de datos.
2. **Personalización de QR**: Opción para cambiar color y añadir un logotipo.
3. **Lectura desde Imagen**: Permite cargar archivos de imagen para detectar QR.
4. **Escaneo en Tiempo Real**: Utiliza la cámara del equipo para leer códigos en vivo.
5. **Historial de Uso**: Registra cada código QR generado o leído con su respectiva fecha y hora.
6. **Búsqueda y Filtros**: El usuario puede buscar registros por tipo o fecha.
7. **Exportación y Compartición**: Se pueden guardar los códigos como imagen o copiarlos al portapapeles.
8. **Validación y Manejo de Errores**: Verificación de entradas, formatos compatibles y errores de lectura.

---

## Estructura del Proyecto

El sistema está dividido en clases que representan distintos módulos funcionales:

### 1. QRGenerator
Encargada de generar el código QR a partir del contenido ingresado.  
Atributos como contenido, color, logo y tamaño son definidos por el usuario.  
Métodos: `generar_qr()`, `guardar_qr()`.

### 2. QRReader
Módulo de lectura que puede cargar archivos o activar la cámara.  
Métodos: `leer_qr_desde_imagen()`, `leer_qr_desde_camara()`.

### 3. DatabaseManager
Gestor de base de datos SQLite. Maneja la conexión y las operaciones.  
Métodos: `guardar_historial()`, `consultar_historial()`, `eliminar_registro()`.

### 4. QRHistory
Encapsula los datos del historial de QR y permite filtrarlos o limpiarlos.  
Métodos: `buscar_qr()`, `filtrar_qr_por_tipo()`, `limpiar_historial()`.

### 5. QRExporter
Módulo de exportación que permite guardar los códigos en formato imagen o copiarlos.  
Métodos: `guardar_como_png()`, `guardar_como_jpg()`, `copiar_al_portapapeles()`.

### 6. QRValidator
Válida los datos que el usuario intenta convertir en QR.  
Métodos: `validar_tipo_dato()`, `verificar_longitud()`.

### 7. MainApp
Interfaz gráfica construida con tkinter. Organiza las vistas principales y llama a los demás módulos.  
Métodos: `iniciar_interfaz()`, `mostrar_historial()`, `mostrar_notificacion()`.

---

## Requisitos Funcionales

- Generar códigos QR con distintos tipos de contenido.
- Leer códigos QR desde una imagen o cámara.
- Almacenar historial con fecha, tipo y contenido.
- Exportar los códigos generados.
- Permitir personalización estética del QR.
- Buscar y filtrar datos del historial.
- Validar entradas y manejar errores de forma adecuada.

---

## Tecnologías y Librerías Utilizadas


- `tkinter` para interfaz gráfica
- `datetime` para fechas de creación de los QR
- `sqlite3` para base de datos local




