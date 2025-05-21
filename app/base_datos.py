import sqlite3

class DatabaseManager:
    def __init__(self,db_name: str = "qr_historial.db"):
        self.conexion = sqlite3.connect(db_name)
        self.cursor = self.conexion.cursor()
        self._crear_tabla()

    def _crear_tabla(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS historial (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                contenido TEXT NOT NULL,
                fecha TEXT NOT NULL
            )
        ''')
        self.conexion.commit()

    def guardar_historial(self, tipo: str, contenido: str, fecha: str):
        self.cursor.execute('''
                            INSERT INTO historial (tipo, contenido, fecha)
                            VALUES (?, ?, ?)
                        ''', (tipo, contenido, fecha))
        self.conexion.commit()

    def consultar_historial(self) -> list:
        self.cursor.execute('SELECT * FROM historial ORDER BY fecha DESC')
        return self.cursor.fetchall()

    def eliminar_registro(self, id_registro: int):
       pass