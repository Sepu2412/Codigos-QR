class QRGenerator:
    def __init__(self, contenido: str, color: str = "black", logo = None, tamaño: int = 300):
        self.contenido: str = contenido
        self.color : str = color
        self.logo : logo
        self.tamaño : int = tamaño

    def generar_qr(self):
        pass

    def guardar_qr(self, ruta: str):
        pass

