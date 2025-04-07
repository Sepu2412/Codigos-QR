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
        self.qr_img = None

    def generar_qr(self):
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(self.contenido)
        qr.make()
        img = qr.make_image(fill_color=self.color, back_color="white").convert('RGB')
        img = img.resize((self.tamaño, self.tamaño))

        if self.logo:
            try:
                logo_img = Image.open(self.logo)
                logo_img = logo_img.resize((self.tamaño // 4, self.tamaño // 4))
                pos = ((img.size[0] - logo_img.size[0]) // 2, (img.size[1] - logo_img.size[1]) // 2)
                img.paste(logo_img, pos)
            except Exception as e:
                print(f"Error al cargar el logo: {e}")


        self.qr_img = img
        return img


    def guardar_qr(self, ruta: str):
        pass

