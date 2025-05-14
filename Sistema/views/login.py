import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from PIL import Image, ImageTk
import os
from utils.logo_loader import cargar_logo


class LoginWindow(tk.Tk):
    def __init__(self, ruta_usuarios=None, on_success=None):
        super().__init__()

        self.title("Login - Sistema de Préstamo de Equipos")
        self.configure(bg="#e6f2e6")
        self.state("zoomed")  # ✅ Maximizada sin fullscreen
        self.resizable(True, True)

        self.archivo_usuarios = ruta_usuarios or os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "usuarios.xlsx"))
        self.on_success = on_success

        self.verificar_archivo_usuarios()
        self.configurar_interfaz()

    def verificar_archivo_usuarios(self):
        if not os.path.exists(self.archivo_usuarios):
            df = pd.DataFrame(columns=["Usuario", "Password"])
            df.to_excel(self.archivo_usuarios, index=False)
    def test_imagen():
        img = cargar_logo()
        if img:
            print(f"✔ Tipo correcto: {type(img)}")  # Debe ser <class 'PIL.ImageTk.PhotoImage'>
            root = tk.Tk()
            lbl = tk.Label(root, image=img)
            lbl.image = img  # Mantener referencia
            lbl.pack()
            root.mainloop()
        else:
            print("❌ Fallo al cargar imagen")

    def configurar_interfaz(self):
        #self.logo_tk = cargar_logo()
        #if self.logo_tk:
        #    print("✔ Imagen cargada, creando Label...")
        #    self.lbl_logo = tk.Label(self, image=self.logo_tk, bg="#e6f2e6")
        #    self.lbl_logo.image = self.logo_tk  # ✅ IMPORTANTE: mantener referencia
        #    self.lbl_logo.place(relx=0.5, rely=0.1, anchor="center")
        
        #else:
        #    print("⚠️ Usando placeholder - Logo no cargado")
        #    lbl_error = tk.Label(
        #    self, 
        #    text="LOGO NO DISPONIBLE",
        #    fg="red",
        #    bg="#e6f2e6"
         #   )
          #  lbl_error.place(relx=0.5, rely=0.1, anchor="center")

        # Marco de login
        marco = tk.Frame(self, bg="#d0e5d0", bd=2, relief="ridge")
        marco.place(relx=0.5, rely=0.55, anchor="center", width=400, height=300)

        fuente_etiquetas = ("Segoe UI", 14, "bold")

        tk.Label(marco, text="Usuario", bg="#d0e5d0", font=fuente_etiquetas).place(relx=0.5, rely=0.2, anchor="center")
        self.entry_usuario = tk.Entry(marco, font=("Segoe UI", 12), justify="center")
        self.entry_usuario.place(relx=0.5, rely=0.35, anchor="center", width=250)

        tk.Label(marco, text="Contraseña", bg="#d0e5d0", font=fuente_etiquetas).place(relx=0.5, rely=0.5, anchor="center")
        self.entry_contrasena = tk.Entry(marco, show="*", font=("Segoe UI", 12), justify="center")
        self.entry_contrasena.place(relx=0.5, rely=0.65, anchor="center", width=250)

        btn_login = tk.Button(marco, text="Iniciar Sesión", font=("Segoe UI", 12), bg="#7fbf7f", fg="white", command=self.verificar_login)
        btn_login.place(relx=0.5, rely=0.85, anchor="center")

    def verificar_login(self):
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        try:
            df = pd.read_excel(self.archivo_usuarios)
            df.columns = df.columns.str.strip()

            if 'Usuario' not in df.columns or 'Password' not in df.columns:
                messagebox.showerror("Error", "El archivo de usuarios no tiene las columnas requeridas: 'Usuario' y 'Password'")
                return

            validacion = df[
                (df['Usuario'].astype(str).str.strip().str.lower() == usuario.lower()) &
                (df['Password'].astype(str).str.strip() == contrasena)
            ]

            if not validacion.empty:
                self.destroy()
                if self.on_success:
                    self.on_success()
                else:
                    from .main_window import MainWindow
                    MainWindow().mainloop()
            else:
                messagebox.showerror("Error", "Credenciales inválidas")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo verificar el login:\n{e}")
