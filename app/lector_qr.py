
from PIL import Image
import cv2
import pyzbar.pyzbar as pyzbar


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

    def leer_qr_desde_camara(self, callback=None) -> str | None:
        cap = cv2.VideoCapture(0)
        try:
            while True:
                ret, frame = cap.read()
                if not ret: break

                decoded = pyzbar.decode(Image.fromarray(
                    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                ))

                if decoded and callback:
                    callback(decoded[0].data.decode("utf-8"))
                    break

                cv2.imshow('QR Scanner', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()
        return None

    def leer_qr_desde_frame(self, frame) -> str | None:
        try:
            imagen_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            decoded = pyzbar.decode(imagen_pil)
            return decoded[0].data.decode("utf-8") if decoded else None
        except Exception as e:
            print(f"Error al leer frame: {e}")
            return None

