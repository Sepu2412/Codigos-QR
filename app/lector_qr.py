from PIL import Image
import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np

class QRReader:
    def __init__(self, imagen:str):
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

        except Exception as e:
            return f"Error al leer el QR: {e}"

    def leer_qr_desde_camara(self) -> str:
        cap = cv2.VideoCapture(0)
        try:
            while True:
                ret, frame = cap.read()
                if not ret: break
                
                decoded = pyzbar.decode(Image.fromarray(
                    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                ))
                
                if decoded:
                    return decoded[0].data.decode("utf-8")
                
                cv2.imshow('QR Scanner', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()
        return "No se detectó código QR"
    
