import dearpygui.dearpygui as dpg
import cv2
import numpy as np
from main import db, historial_qr, actualizar_historial
from generador_qr import QRGenerator
from lector_qr import QRReader
from exportador import QRExporter
from validador import QRValidator
from PIL import ImageColor
import time

class QRApp:
    def __init__(self):
        self.camera_active = False
        self.cap = None
        self.current_qr_image = None
        self.selected_color = "black"
        self.logo_path = ""
        self.historial_data = []
        
        # Configuración inicial de Dear PyGui
        dpg.create_context()
        self.setup_theme()
        self.create_main_window()
        dpg.create_viewport(title='QR Manager', width=1200, height=800)
        dpg.setup_dearpygui()
        dpg.show_viewport()
    
    def setup_theme(self):
        with dpg.theme() as main_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 122, 204))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (40, 40, 40))
                dpg.add_theme_style(dpg.mvStyleStyle_FrameRounding, 5)
                dpg.add_theme_style(dpg.mvStyleStyle_ItemSpacing, 10, 5)
        dpg.bind_theme(main_theme)
    
    def create_main_window(self):
        with dpg.window(tag="Main Window"):
            with dpg.tab_bar():
                # Pestaña Generar QR
                with dpg.tab(label="Generar QR"):
                    self.create_generator_tab()
                
                # Pestaña Leer QR
                with dpg.tab(label="Leer QR"):
                    self.create_reader_tab()
                
                # Pestaña Historial
                with dpg.tab(label="Historial"):
                    self.create_history_tab()
    
    def create_generator_tab(self):
        dpg.add_input_text(tag="qr_content", label="Contenido", width=400)
        dpg.add_color_edit(tag="qr_color", label="Color", default_value=(0, 0, 0))
        dpg.add_input_text(tag="logo_path", label="Ruta del logo", width=400)
        dpg.add_button(label="Generar QR", callback=self.generate_qr)
        dpg.add_image_button(tag="qr_preview", width=300, height=300)
        dpg.add_button(label="Exportar como PNG", callback=lambda: self.export_qr("png"))
        dpg.add_button(label="Exportar como JPG", callback=lambda: self.export_qr("jpg"))
    
    def create_reader_tab(self):
        dpg.add_button(label="Cargar imagen", callback=self.load_image)
        dpg.add_button(label="Iniciar cámara", callback=self.toggle_camera)
        dpg.add_image(tag="camera_feed", width=640, height=480)
        dpg.add_text(tag="qr_result")
    
    def create_history_tab(self):
        dpg.add_input_text(tag="search_text", label="Buscar", width=300)
        dpg.add_button(label="Buscar", callback=self.search_history)
        dpg.add_listbox(tag="historial_list", width=800, num_items=15)
        dpg.add_button(label="Actualizar", callback=self.update_history)
        self.update_history()
    
    def generate_qr(self):
        content = dpg.get_value("qr_content")
        color = self.rgb_to_hex(dpg.get_value("qr_color"))
        logo = dpg.get_value("logo_path")
        
        validator = QRValidator(content)
        if not validator.validar_tipo_dato():
            self.show_error("Error: Contenido no válido")
            return
        
        generator = QRGenerator(content, color=color, logo=logo if logo else None)
        qr_image = generator.generar_qr()
        
        # Convertir imagen para vista previa
        qr_image.save("temp_preview.png")
        width, height = qr_image.size
        self.load_image_texture("temp_preview.png", "qr_preview", width, height)
        self.current_qr_image = qr_image
    
    def export_qr(self, format):
        if not self.current_qr_image:
            self.show_error("Primero genera un QR")
            return
        
        exporter = QRExporter(os.path.expanduser("~/Desktop"))
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        
        try:
            if format == "png":
                exporter.guardar_como_png(self.current_qr_image, f"qr_{timestamp}")
            elif format == "jpg":
                exporter.guardar_como_jpg(self.current_qr_image, f"qr_{timestamp}")
            
            self.show_notification("QR exportado exitosamente")
        except Exception as e:
            self.show_error(f"Error al exportar: {str(e)}")
    
    def toggle_camera(self):
        self.camera_active = not self.camera_active
        if self.camera_active:
            self.cap = cv2.VideoCapture(0)
            dpg.configure_item("camera_feed", show=True)
            self.update_camera_feed()
        else:
            if self.cap:
                self.cap.release()
            dpg.configure_item("camera_feed", show=False)
    
    def update_camera_feed(self):
        if self.camera_active and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # Convertir frame de OpenCV a texture
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.flip(frame, 1)
                decoded = self.read_qr_from_frame(frame)
                
                if decoded:
                    dpg.set_value("qr_result", f"Contenido: {decoded}")
                    self.save_to_history(decoded)
                    self.toggle_camera()
                
                self.load_cv2_texture(frame, "camera_feed")
            
            dpg.render_dearpygui_frame()
            dpg.split_frame()
            dpg.loop.call_soon(self.update_camera_feed)
    
    def read_qr_from_frame(self, frame):
        reader = QRReader("")
        pil_image = Image.fromarray(frame)
        decoded = pyzbar.decode(pil_image)
        return decoded[0].data.decode("utf-8") if decoded else None
    
    def load_image(self):
        file_path = dpg.add_file_dialog(
            directory_selector=False,
            show=True,
            callback=lambda s, d: self.process_selected_image(d.get("file_path_name"))
        )
    
    def process_selected_image(self, file_path):
        if file_path:
            reader = QRReader(file_path)
            result = reader.leer_qr_desde_imagen(file_path)
            dpg.set_value("qr_result", result if result else "No se detectó QR")
            if result:
                self.save_to_history(result)
    
    def save_to_history(self, content):
        fecha = time.strftime("%Y-%m-%d %H:%M:%S")
        db.guardar_historial("leído", content, fecha)
        self.update_history()
    
    def update_history(self):
        actualizar_historial()
        self.historial_data = [f"{r['id']} | {r['tipo']} | {r['contenido'][:50]} | {r['fecha']}" 
                              for r in historial_qr.lista_qr]
        dpg.configure_item("historial_list", items=self.historial_data)
    
    def search_history(self):
        query = dpg.get_value("search_text")
        resultados = historial_qr.buscar_qr(query)
        dpg.configure_item("historial_list", items=[f"{r['id']} | {r['tipo']} | {r['contenido'][:50]}" 
                                                   for r in resultados])
    
    # Helpers para manejo de imágenes
    def load_image_texture(self, path, tag, width, height):
        if dpg.does_item_exist(tag + "_texture"):
            dpg.delete_item(tag + "_texture")
        
        image_data = []
        with Image.open(path) as img:
            image_data = np.array(img.convert("RGBA")).flatten().tolist()
        
        with dpg.texture_registry():
            dpg.add_static_texture(width, height, image_data, tag=tag + "_texture")
        dpg.configure_item(tag, texture_tag=tag + "_texture")
    
    def load_cv2_texture(self, frame, tag):
        if dpg.does_item_exist(tag + "_texture"):
            dpg.delete_item(tag + "_texture")
        
        height, width, _ = frame.shape
        image_data = frame.flatten().tolist()
        
        with dpg.texture_registry():
            dpg.add_dynamic_texture(width, height, image_data, tag=tag + "_texture")
        dpg.configure_item(tag, texture_tag=tag + "_texture")
    
    def rgb_to_hex(self, rgb):
        return "#{:02x}{:02x}{:02x}".format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
    
    def show_error(self, message):
        dpg.configure_item("error_popup", show=True)
        dpg.set_value("error_message", message)
    
    def show_notification(self, message):
        dpg.configure_item("notification_popup", show=True)
        dpg.set_value("notification_message", message)
    
    def run(self):
        while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()
        dpg.destroy_context()

if __name__ == "__main__":
    app = QRApp()
    app.run()
