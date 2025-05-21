from typing import List, Dict, Any
from datetime import datetime

class QRHistory:
    def __init__(self):
        self.lista_qr: List[Dict[str, Any]] = []

    def buscar_qr(self, texto: str) -> list:
        return [qr for qr in self.lista_qr if texto.lower() in qr.get("contenido", "").lower()]

    def filtrar_qr_por_tipo(self, tipo: str) -> list:
        pass

    def limpiar_historial(self):
       pass
