from generador_qr import QRGenerator
from lector_qr import QRReader
import os
import time

def menu_principal():
    while True:
        print("\n--- Generador y Lector de QR ---")
        print("1. Generar código QR")
        print("2. Leer código QR desde imagen")
        print("3. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            texto = input("Ingresa el texto o URL para el QR: ")
            color = input("Color del QR (opcional, default=black): ") or "black"
            logo = input("Ruta del logo (opcional, dejar vacío si no hay): ") or None

            generador = QRGenerator(texto, color=color, logo=logo)
            generador.generar_qr()

            # Guardar automáticamente en el Escritorio
            escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
            nombre_archivo = f"qr_{time.strftime('%Y-%m-%d_%H-%M-%S')}.png"
            ruta = os.path.join(escritorio, nombre_archivo)

            generador.guardar_qr(ruta)

        elif opcion == "2":
            ruta_imagen = input("Ruta de la imagen con QR: ")
            lector = QRReader(ruta_imagen)
            resultado = lector.leer_qr_desde_imagen(ruta_imagen)
            print(f"\nContenido del QR: {resultado}")

        elif opcion == "3":
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu_principal()
