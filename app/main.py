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