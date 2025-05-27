import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import os
from datetime import datetime

from generador_qr import QRGenerator
from lector_qr import QRReader
from exportador import QRExporter
from base_datos import DatabaseManager
from historial import QRHistory


class QRApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de QR - Generador y Lector")
        self.geometry("1000x700")
        self.configure(bg="#f0f0f0")

        # Configuración inicial
        self.db = DatabaseManager()
        self.historial = QRHistory()
        self.current_qr_image = None
        self.logo_path = None
        self.camera_active = False
        self.cap = None

        # Configurar estilo
        self._configurar_estilos()

        # Widgets
        self._crear_widgets()
        self._centrar_ventana()
        self._actualizar_historial()

    def _configurar_estilos(self):
        """Configura los estilos para la aplicación"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configurar colores y fuentes
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('TEntry', font=('Arial', 10), padding=5)
        style.configure('TCombobox', font=('Arial', 10), padding=5)
        style.configure('Treeview', font=('Arial', 10), rowheight=25)
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))

        # Estilo para las pestañas
        style.configure('TNotebook', background='#f0f0f0')
        style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'), padding=[10, 5])

    def _centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def _crear_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Notebook (Pestañas)
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Pestaña Generar QR
        tab_generar = ttk.Frame(notebook)
        self._crear_tab_generar(tab_generar)
        notebook.add(tab_generar, text="Generar QR")

        # Pestaña Leer QR
        tab_leer = ttk.Frame(notebook)
        self._crear_tab_leer(tab_leer)
        notebook.add(tab_leer, text="Leer QR")

        # Pestaña Historial
        tab_historial = ttk.Frame(notebook)
        self._crear_tab_historial(tab_historial)
        notebook.add(tab_historial, text="Historial")

    def _crear_tab_generar(self, parent):
        """Crea la interfaz para la pestaña de generación de QR"""
        # Frame principal con padding
        main_frame = ttk.Frame(parent, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame de configuración
        config_frame = ttk.Frame(main_frame)
        config_frame.pack(fill=tk.X, pady=(0, 20))

        # Frame para el contenido
        content_frame = ttk.Frame(config_frame)
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        lbl_contenido = ttk.Label(content_frame, text="Contenido del QR:", font=('Arial', 10, 'bold'))
        lbl_contenido.pack(anchor=tk.W, pady=(0, 5))

        self.entry_contenido = ttk.Entry(content_frame, width=40)
        self.entry_contenido.pack(fill=tk.X, pady=(0, 10))

        # Frame para opciones de diseño
        design_frame = ttk.Frame(config_frame)
        design_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        lbl_color = ttk.Label(design_frame, text="Color del QR:", font=('Arial', 10, 'bold'))
        lbl_color.pack(anchor=tk.W, pady=(0, 5))

        color_frame = ttk.Frame(design_frame)
        color_frame.pack(fill=tk.X)

        self.combo_color = ttk.Combobox(color_frame, values=["Negro", "Rojo", "Azul", "Verde"], width=15)
        self.combo_color.set("Negro")
        self.combo_color.pack(side=tk.LEFT, padx=(0, 10))

        btn_logo = ttk.Button(color_frame, text="Agregar Logo", command=self._seleccionar_logo)
        btn_logo.pack(side=tk.LEFT)

        self.lbl_logo = ttk.Label(design_frame, text="Sin logo seleccionado", foreground="gray")
        self.lbl_logo.pack(anchor=tk.W, pady=(5, 0))

        # Frame para botones de acción
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 20))

        btn_generar = ttk.Button(btn_frame, text="Generar QR", style='Accent.TButton', command=self._generar_qr)
        btn_generar.pack(side=tk.LEFT, padx=5, ipadx=10)

        btn_exportar = ttk.Button(btn_frame, text="Exportar QR", command=self._exportar_qr)
        btn_exportar.pack(side=tk.LEFT, padx=5, ipadx=10)

        # Frame para la vista previa
        preview_frame = ttk.LabelFrame(main_frame, text="Vista Previa", padding=10)
        preview_frame.pack(fill=tk.BOTH, expand=True)

        self.lbl_preview = ttk.Label(preview_frame, text="Genera un QR para ver la vista previa",
                                     foreground="gray", justify=tk.CENTER)
        self.lbl_preview.pack(fill=tk.BOTH, expand=True)

    def _crear_tab_leer(self, parent):
        """Crea la interfaz para la pestaña de lectura de QR"""
        main_frame = ttk.Frame(parent, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame para botones de acción
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 20))

        btn_imagen = ttk.Button(btn_frame, text="Cargar Imagen", command=self._leer_desde_imagen)
        btn_imagen.pack(side=tk.LEFT, padx=5, ipadx=10)

        btn_camara = ttk.Button(btn_frame, text="Usar Cámara", command=self._toggle_camara)
        btn_camara.pack(side=tk.LEFT, padx=5, ipadx=10)

        # Frame para el resultado
        result_frame = ttk.LabelFrame(main_frame, text="Contenido del QR", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        self.lbl_resultado = ttk.Label(result_frame, text="Escanea un código QR para ver su contenido aquí...",
                                       wraplength=400, justify=tk.LEFT, foreground="gray")
        self.lbl_resultado.pack(fill=tk.BOTH, expand=True)

        # Frame de cámara (inicialmente oculto)
        self.camera_frame = ttk.LabelFrame(main_frame, text="Cámara en Vivo", padding=10)

        self.camera_label = ttk.Label(self.camera_frame)
        self.camera_label.pack(pady=5)

        btn_detener = ttk.Button(self.camera_frame, text="Detener Cámara", command=self._toggle_camara)
        btn_detener.pack(pady=5)

    def _crear_tab_historial(self, parent):
        """Crea la interfaz para la pestaña de historial"""
        main_frame = ttk.Frame(parent, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame de búsqueda y filtros
        filter_frame = ttk.Frame(main_frame)
        filter_frame.pack(fill=tk.X, pady=(0, 15))

        lbl_buscar = ttk.Label(filter_frame, text="Buscar:", font=('Arial', 10, 'bold'))
        lbl_buscar.pack(side=tk.LEFT, padx=(0, 5))

        self.entry_buscar = ttk.Entry(filter_frame, width=30)
        self.entry_buscar.pack(side=tk.LEFT, padx=(0, 15))
        self.entry_buscar.bind("<KeyRelease>", self._filtrar_historial)

        lbl_filtro = ttk.Label(filter_frame, text="Filtrar por tipo:", font=('Arial', 10, 'bold'))
        lbl_filtro.pack(side=tk.LEFT, padx=(0, 5))

        self.combo_filtro = ttk.Combobox(filter_frame, values=["Todos", "Generado", "Leído"], state="readonly",
                                         width=10)
        self.combo_filtro.set("Todos")
        self.combo_filtro.pack(side=tk.LEFT, padx=(0, 15))
        self.combo_filtro.bind("<<ComboboxSelected>>", self._filtrar_historial)

        btn_actualizar = ttk.Button(filter_frame, text="Actualizar", command=self._actualizar_historial)
        btn_actualizar.pack(side=tk.RIGHT, padx=5)

        # Frame para el Treeview
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview con scrollbar
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Tipo", "Contenido", "Fecha"), show="headings")
        self.tree.heading("ID", text="ID", anchor=tk.W)
        self.tree.heading("Tipo", text="Tipo", anchor=tk.W)
        self.tree.heading("Contenido", text="Contenido", anchor=tk.W)
        self.tree.heading("Fecha", text="Fecha", anchor=tk.W)

        # Configurar columnas
        self.tree.column("ID", width=50, stretch=tk.NO)
        self.tree.column("Tipo", width=100, stretch=tk.NO)
        self.tree.column("Contenido", width=300)
        self.tree.column("Fecha", width=150, stretch=tk.NO)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Empaquetar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Frame para botones de acción
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(15, 0))

        btn_eliminar = ttk.Button(action_frame, text="Eliminar Selección", command=self._eliminar_registro)
        btn_eliminar.pack(side=tk.LEFT, padx=5)

        btn_limpiar = ttk.Button(action_frame, text="Limpiar Historial", command=self._limpiar_historial)
        btn_limpiar.pack(side=tk.RIGHT, padx=5)

    # Métodos de funcionalidad (se mantienen igual que en tu versión original)
    def _generar_qr(self):
        contenido = self.entry_contenido.get().strip()
        if not contenido:
            messagebox.showerror("Error", "Ingrese contenido para el QR")
            return

        # Mapear nombres de colores a valores hex
        color_map = {
            "Negro": "black",
            "Rojo": "red",
            "Azul": "blue",
            "Verde": "green"
        }
        color = color_map.get(self.combo_color.get(), "black")

        try:
            generador = QRGenerator(contenido, color=color, logo=self.logo_path)
            self.current_qr_image = generador.generar_qr()

            # Mostrar vista previa
            img_tk = ImageTk.PhotoImage(self.current_qr_image.resize((250, 250)))
            self.lbl_preview.configure(image=img_tk, text="")
            self.lbl_preview.image = img_tk

            # Guardar en historial
            fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.db.guardar_historial("generado", contenido, fecha)
            self._actualizar_historial()

            messagebox.showinfo("Éxito", "QR generado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el QR: {str(e)}")

    def _exportar_qr(self):
        if not self.current_qr_image:
            messagebox.showerror("Error", "No hay QR generado para exportar")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("Todos los archivos", "*.*")],
            title="Guardar código QR"
        )

        if file_path:
            try:
                exportador = QRExporter(os.path.dirname(file_path))
                nombre = os.path.splitext(os.path.basename(file_path))[0]

                if file_path.lower().endswith('.png'):
                    exportador.guardar_como_png(self.current_qr_image, nombre)
                else:
                    exportador.guardar_como_jpg(self.current_qr_image, nombre)

                messagebox.showinfo("Éxito", f"QR guardado en:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el QR: {str(e)}")

    def _seleccionar_logo(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg"), ("Todos los archivos", "*.*")],
            title="Seleccionar logo"
        )

        if file_path:
            self.logo_path = file_path
            self.lbl_logo.config(text=os.path.basename(file_path), foreground="black")

    def _leer_desde_imagen(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg"), ("Todos los archivos", "*.*")],
            title="Seleccionar imagen con QR"
        )

        if file_path:
            try:
                lector = QRReader(file_path)
                resultado = lector.leer_qr_desde_imagen(file_path)

                if resultado:
                    self.lbl_resultado.config(text=resultado, foreground="black")

                    # Guardar en historial
                    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    self.db.guardar_historial("leído", resultado, fecha)
                    self._actualizar_historial()
                else:
                    messagebox.showwarning("Advertencia", "No se detectó QR en la imagen")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el QR: {str(e)}")

    def _toggle_camara(self):
        if not self.camera_active:
            self._iniciar_camara()
        else:
            self._detener_camara()

    def _iniciar_camara(self):
        self.camera_active = True
        self.camera_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        self.cap = cv2.VideoCapture(0)
        self._actualizar_frame_camara()

    def _detener_camara(self):
        self.camera_active = False
        self.camera_frame.pack_forget()
        if self.cap:
            self.cap.release()

    def _actualizar_frame_camara(self):
        if self.camera_active and self.cap:
            ret, frame = self.cap.read()
            if ret:
                # Mostrar vista previa
                cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv_image)
                imgtk = ImageTk.PhotoImage(image=img.resize((400, 300)))

                self.camera_label.imgtk = imgtk
                self.camera_label.configure(image=imgtk)

                # Intentar leer QR
                lector = QRReader("")
                resultado = lector.leer_qr_desde_frame(frame)
                if resultado:
                    self.lbl_resultado.config(text=resultado, foreground="black")

                    # Guardar en historial
                    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    self.db.guardar_historial("leído", resultado, fecha)
                    self._actualizar_historial()

                    # Detener cámara
                    self._detener_camara()
                    return

            # Programar próxima actualización
            self.camera_label.after(10, self._actualizar_frame_camara)

    def _actualizar_historial(self):
        # Actualizar lista en memoria
        self.historial.lista_qr.clear()
        registros = self.db.consultar_historial()
        for registro in registros:
            self.historial.lista_qr.append({
                "id": registro[0],
                "tipo": registro[1],
                "contenido": registro[2],
                "fecha": registro[3]
            })

        # Actualizar treeview
        self._filtrar_historial()

    def _filtrar_historial(self, event=None):
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        texto_busqueda = self.entry_buscar.get().lower()
        tipo_filtro = self.combo_filtro.get().lower()

        # Aplicar filtros
        registros_filtrados = []
        for qr in self.historial.lista_qr:
            contenido_coincide = texto_busqueda in qr["contenido"].lower()
            tipo_coincide = (tipo_filtro == "todos") or (qr["tipo"].lower() == tipo_filtro)

            if contenido_coincide and tipo_coincide:
                registros_filtrados.append(qr)

        # Mostrar resultados
        for qr in registros_filtrados:
            self.tree.insert("", tk.END, values=(
                qr["id"],
                qr["tipo"],
                qr["contenido"],
                qr["fecha"]
            ))

    def _eliminar_registro(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un registro")
            return

        item = seleccion[0]
        id_registro = self.tree.item(item, "values")[0]

        try:
            self.db.eliminar_registro(int(id_registro))
            self._actualizar_historial()
            messagebox.showinfo("Éxito", "Registro eliminado")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {str(e)}")

    def _limpiar_historial(self):
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea eliminar todo el historial?"):
            try:
                self.db.limpiar_historial()
                self.historial.limpiar_historial()
                self._actualizar_historial()
                messagebox.showinfo("Éxito", "Historial limpiado")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo limpiar: {str(e)}")


if __name__ == "__main__":
    app = QRApp()
    app.mainloop()