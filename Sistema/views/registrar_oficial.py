import tkinter as tk
from tkinter import ttk

class RegistrarOficial(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Registrar Oficial")
        self.geometry("400x300")

        ttk.Label(self, text="Nombre:").pack(pady=5)
        self.nombre_entry = ttk.Entry(self)
        self.nombre_entry.pack(pady=5)

        ttk.Label(self, text="Número de Identidad:").pack(pady=5)
        self.id_entry = ttk.Entry(self)
        self.id_entry.pack(pady=5)

        ttk.Button(self, text="Guardar", command=self.guardar_oficial).pack(pady=20)

    def guardar_oficial(self):
        nombre = self.nombre_entry.get()
        identidad = self.id_entry.get()
        print(f"Guardando oficial: {nombre} - {identidad}")
