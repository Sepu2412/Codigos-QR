import qrcode
from PIL import Image
import os
import datetime

class QRGenerator:
    def __init__(self, contenido: str, color: str = "black", logo = None, tamaño: int = 300):
        self.contenido: str = contenido
        self.color : str = color
        self.logo : logo
        self.tamaño : int = tamaño

    def generar_qr(self):
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(self.contenido)
        qr.make()
        img = qr.make_image(fill_color=self.color, back_color="white").convert('RGB')
        img = img.resize((self.tamaño, self.tamaño))


    def guardar_qr(self, ruta: str):
        pass

