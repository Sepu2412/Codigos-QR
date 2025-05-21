from generador_qr import QRGenerator
from lector_qr import QRReader
from base_datos import DatabaseManager
import os
import time
from datetime import datetime
from PIL import ImageColor



def color_valido(color: str) -> bool:
    try:
        ImageColor.getrgb(color)
        return True
    except ValueError:
        return False



db = DatabaseManager()


def menu_principal():
    while True:
        print("\n--- Generador y Lector de QR ---")
        print("1. Generar código QR")
        print("2. Leer código QR desde imagen")
        print("3. Ver historial")
        print("4. Eliminar registro del historial")
        print("5. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            texto = input("Ingresa el texto o URL para el QR: ")

            # Validar color
            while True:
                color = input("Color del QR (opcional, default=black): ").strip() or "black"
                if color_valido(color):
                    break
                else:
                    print("⚠️ Color no válido. Ej: black, red, blue...")

            logo = input("Ruta del logo (opcional, dejar vacío si no hay): ") or None

            generador = QRGenerator(texto, color=color, logo=logo)
            generador.generar_qr()

            escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
            nombre_archivo = f"qr_{time.strftime('%Y-%m-%d_%H-%M-%S')}.png"
            ruta = os.path.join(escritorio, nombre_archivo)
            generador.guardar_qr(ruta)

            print(f"✅ Código QR guardado en: {ruta}")

            # Guardar en la base de datos
            fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.guardar_historial("generado", texto, fecha)

        elif opcion == "2":
            ruta_imagen = input("Ruta de la imagen con QR: ")
            lector = QRReader(ruta_imagen)
            resultado = lector.leer_qr_desde_imagen(ruta_imagen)

            if resultado:
                print(f"\nContenido del QR: {resultado}")

                # Guardar en la base de datos
                fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                db.guardar_historial("leído", resultado, fecha)
            else:
                print("⚠️ No se detectó ningún código QR en la imagen.")

        elif opcion == "3":
            historial = db.consultar_historial()
            if historial:
                print("\n📜 Historial de códigos QR:")
                for registro in historial:
                    print(f"ID: {registro[0]} | Tipo: {registro[1]} | Contenido: {registro[2]} | Fecha: {registro[3]}")
            else:
                print("📭 No hay registros en el historial.")

        elif opcion == "4":
            historial = db.consultar_historial()
            if not historial:
                print("📭 No hay registros para eliminar.")
                continue

            print("\n📜 Historial de códigos QR:")
            for registro in historial:
                print(f"ID: {registro[0]} | Tipo: {registro[1]} | Contenido: {registro[2]} | Fecha: {registro[3]}")

            try:
                id_eliminar = int(input("Ingresa el ID del registro que deseas eliminar: "))
                # Verificar que el ID existe
                if any(reg[0] == id_eliminar for reg in historial):
                    db.eliminar_registro(id_eliminar)
                    print(f"✅ Registro con ID {id_eliminar} eliminado.")
                else:
                    print("❌ ID no encontrado en el historial.")
            except ValueError:
                print("❌ Entrada inválida. Debes ingresar un número entero.")

        elif opcion == "5":
            print("👋 Saliendo del programa...")
            break

        else:
            print("❌ Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    menu_principal()

