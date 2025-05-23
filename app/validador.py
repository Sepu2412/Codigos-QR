class QRValidator:
    def __init__(self, datos_entrada: str):
        self.datos_entrada = datos_entrada

    def validar_tipo_dato(self) -> bool:
        return isinstance(self.datos_entrada, str) and self.datos_entrada.strip() != ""

    def verificar_longitud(self, max_length: int = 300) -> bool:
        pass
