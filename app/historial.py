from typing import List, Dict, Any


class QRHistory:
    def __init__(self):
        self.lista_qr: List[Dict[str, Any]] = []

    def buscar_qr(self, texto: str) -> list:
        return [qr for qr in self.lista_qr if texto.lower() in qr.get("contenido", "").lower()]

    def filtrar_qr_por_tipo(self, tipo: str) -> list:
        return [qr for qr in self.lista_qr if qr.get("tipo", "").lower() == tipo.lower()]

    def limpiar_historial(self):
        self.lista_qr.clear()
