from PIL import Image
import pyzbar.pyzbar as pyzbar

class QRReader:
    def __init__(self, imagen:str, '''camara: bool = False'''):
        self.imagen: str = imagen
        '''self.camara: bool = camara'''

    def leer_qr_desde_imagen(self, ruta_imagen: str) -> str:
        try:
            img = Image.open(ruta_imagen)
            decoded = pyzbar.decode(img)
            if decoded:
                return decoded[0].data.decode("utf-8")
            else:
                return "No se pudo encontrar ningún código QR en la imagen."

    def leer_qr_desde_camara(self) -> str:
        pass
