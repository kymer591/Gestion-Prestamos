import tkinter as tk
from tkinter import ttk

class RegistrarEquipo(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Registrar Equipo")
        self.geometry("400x300")

        ttk.Label(self, text="Nombre del Equipo:").pack(pady=5)
        self.nombre_entry = ttk.Entry(self)
        self.nombre_entry.pack(pady=5)

        ttk.Label(self, text="Código QR:").pack(pady=5)
        self.codigo_qr_entry = ttk.Entry(self)
        self.codigo_qr_entry.pack(pady=5)

        ttk.Label(self, text="Estado:").pack(pady=5)
        self.estado_combo = ttk.Combobox(self, values=["Disponible", "En Préstamo"])
        self.estado_combo.pack(pady=5)
        self.estado_combo.current(0)

        ttk.Button(self, text="Guardar", command=self.guardar_equipo).pack(pady=20)

    def guardar_equipo(self):
        nombre = self.nombre_entry.get()
        codigo_qr = self.codigo_qr_entry.get()
        estado = self.estado_combo.get()
        print(f"Guardando equipo: {nombre}, QR: {codigo_qr}, Estado: {estado}")
