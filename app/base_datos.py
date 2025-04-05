import sqlite3

class DatabasaManager:
    def __init__(self,db_name: str = "qr_historial.db"):
        self.conexion = sqlite3.connect(db_name)
        self.cursor = self.conexion.cursor()

    def guardar_historial(self, tipo: str, contenido: str, fecha: str):
        pass

    def consultar_historial(self) -> list:
        pass

    def eliminar_registro(self, id_registro: int):
        pass