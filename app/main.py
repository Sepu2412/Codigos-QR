from generador_qr import QRGenerator
from lector_qr import QRReader
from base_datos import DatabaseManager
from historial import QRHistory
from exportador import QRExporter
from validador import QRValidator  # Nueva clase añadida
import os
import time
from datetime import datetime
from PIL import ImageColor
from interfaz_grafica import QRApp

def color_valido(color: str) -> bool:
    try:
        ImageColor.getrgb(color)
        return True
    except ValueError:
        return False

db = DatabaseManager()
historial_qr = QRHistory()

def actualizar_historial():
    historial_qr.lista_qr.clear()
    for registro in db.consultar_historial():
        historial_qr.lista_qr.append({
            "id": registro[0],
            "tipo": registro[1],
            "contenido": registro[2],
            "fecha": registro[3]
        })

def menu_principal():
    while True:
        print("\n--- Generador y Lector de QR ---")
        print("1. Generar código QR")
        print("2. Leer código QR desde imagen")
        print("3. Ver historial completo")
        print("4. Buscar en historial")
        print("5. Filtrar historial por tipo")
        print("6. Eliminar registro del historial")
        print("7. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            texto = input("Ingresa el texto o URL para el QR: ")
            validador = QRValidator(texto)

            if not validador.validar_tipo_dato():
                print("❌ Entrada no válida. Debe ser un texto.")
                continue

            if not validador.verificar_longitud():
                print("❌ Texto demasiado largo (máx. 300 caracteres).")
                continue

            while True:
                color = input("Color del QR (opcional, default=black): ").strip() or "black"
                if color_valido(color):
                    break
                else:
                    print("⚠️ Color no válido. Ej: black, red, blue...")

            logo = input("Ruta del logo (opcional, dejar vacío si no hay): ") or None

            generador = QRGenerator(texto, color=color, logo=logo)
            imagen_qr = generador.generar_qr()

            escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
            exportador = QRExporter(escritorio)

            print("\n¿Cómo deseas exportar el QR?")
            print("1. Guardar como PNG")
            print("2. Guardar como JPG")
            print("3. Copiar al portapapeles")
            print("4. Todas las anteriores")
            opcion_exportar = input("Selecciona una opción: ")

            nombre_archivo = f"qr_{time.strftime('%Y-%m-%d_%H-%M-%S')}"

            if opcion_exportar == "1":
                exportador.guardar_como_png(imagen_qr, nombre_archivo)
            elif opcion_exportar == "2":
                exportador.guardar_como_jpg(imagen_qr, nombre_archivo)
            elif opcion_exportar == "3":
                exportador.copiar_al_portapapeles(imagen_qr)
            elif opcion_exportar == "4":
                exportador.guardar_como_png(imagen_qr, nombre_archivo)
                exportador.guardar_como_jpg(imagen_qr, nombre_archivo)
                exportador.copiar_al_portapapeles(imagen_qr)
            else:
                print("⚠️ Opción no válida. No se exportó el QR.")

            fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.guardar_historial("generado", texto, fecha)
            actualizar_historial()

        elif opcion == "2":
            ruta_imagen = input("Ruta de la imagen con QR: ")
            lector = QRReader(ruta_imagen)
            resultado = lector.leer_qr_desde_imagen(ruta_imagen)

            if resultado:
                print(f"\nContenido del QR: {resultado}")
                fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                db.guardar_historial("leído", resultado, fecha)
                actualizar_historial()
            else:
                print("⚠️ No se detectó ningún código QR en la imagen.")

        elif opcion == "3":
            actualizar_historial()
            if historial_qr.lista_qr:
                print("\n📜 Historial completo:")
                for registro in historial_qr.lista_qr:
                    print(f"ID: {registro['id']} | Tipo: {registro['tipo']} | Contenido: {registro['contenido']} | Fecha: {registro['fecha']}")
            else:
                print("📭 No hay registros en el historial.")

        elif opcion == "4":
            texto = input("🔎 Ingresa el texto a buscar: ")
            resultados = historial_qr.buscar_qr(texto)
            if resultados:
                print(f"\nResultados encontrados para '{texto}':")
                for r in resultados:
                    print(f"ID: {r['id']} | Tipo: {r['tipo']} | Contenido: {r['contenido']} | Fecha: {r['fecha']}")
            else:
                print("❌ No se encontraron coincidencias.")

        elif opcion == "5":
            tipo = input("📂 Ingresa el tipo (generado/leído): ").lower()
            resultados = historial_qr.filtrar_qr_por_tipo(tipo)
            if resultados:
                print(f"\nCódigos del tipo '{tipo}':")
                for r in resultados:
                    print(f"ID: {r['id']} | Contenido: {r['contenido']} | Fecha: {r['fecha']}")
            else:
                print("❌ No hay registros de ese tipo.")

        elif opcion == "6":
            actualizar_historial()
            if not historial_qr.lista_qr:
                print("📭 No hay registros para eliminar.")
                continue

            for registro in historial_qr.lista_qr:
                print(f"ID: {registro['id']} | Tipo: {registro['tipo']} | Contenido: {registro['contenido']} | Fecha: {registro['fecha']}")

            try:
                id_eliminar = int(input("Ingresa el ID del registro que deseas eliminar: "))
                if any(reg["id"] == id_eliminar for reg in historial_qr.lista_qr):
                    db.eliminar_registro(id_eliminar)
                    print(f"✅ Registro con ID {id_eliminar} eliminado.")
                    actualizar_historial()
                else:
                    print("❌ ID no encontrado.")
            except ValueError:
                print("❌ Entrada inválida. Debes ingresar un número entero.")

        elif opcion == "7":
            print("👋 Saliendo del programa...")
            break

        else:
            print("❌ Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    app = QRApp()
    app.run()
    
    
    #actualizar_historial()
    #menu_principal()
