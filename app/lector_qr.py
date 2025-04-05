class QRReader:
    def __init__(self, imagen:str, camara: bool = False):
        self.imagen: str = imagen
        self.camara: bool = camara

    def leer_qr_desde_imagen(self, ruta_imagen: str) -> str:
        pass

    def leer_qr_desde_camara(self) -> str:
        pass