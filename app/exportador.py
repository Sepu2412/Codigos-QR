from PIL import Image
import os


class QRExporter:
    def __init__(self, ruta_guardado: str):
        self.ruta_guardado = ruta_guardado

    def guardar_como_png(self, imagen_qr: Image.Image, nombre_archivo: str):
        ruta_completa = os.path.join(self.ruta_guardado, f"{nombre_archivo}.png")
        imagen_qr.save(ruta_completa, format='PNG')
        print(f"✅ QR guardado como PNG en: {ruta_completa}")

    def guardar_como_jpg(self, imagen_qr: Image.Image, nombre_archivo: str):
        if imagen_qr.mode != 'RGB':
            imagen_qr = imagen_qr.convert('RGB')
        ruta_completa = os.path.join(self.ruta_guardado, f"{nombre_archivo}.jpg")
        imagen_qr.save(ruta_completa, format='JPEG')
        print(f"✅ QR guardado como JPG en: {ruta_completa}")

