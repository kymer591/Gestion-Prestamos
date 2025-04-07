import tkinter as tk
from tkinter import ttk
from .registrar_oficial import RegistrarOficial
from .registrar_equipo import RegistrarEquipo
from .dashboard_prestamos import PrestamoDashboard  # ✅ Importación corregida

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Préstamos de Equipos")
        self.geometry("600x400")

        ttk.Label(self, text="Sistema de Préstamos", font=("Arial", 16)).pack(pady=20)

        ttk.Button(self, text="Registrar Oficial", command=self.abrir_registro_oficial).pack(pady=5)
        ttk.Button(self, text="Registrar Equipo", command=self.abrir_registro_equipo).pack(pady=5)
        ttk.Button(self, text="Realizar Préstamo", command=self.abrir_prestamo).pack(pady=5)  # ✅ Ya incluye búsqueda

    def abrir_registro_oficial(self):
        ventana = RegistrarOficial(self)
        ventana.grab_set()

    def abrir_registro_equipo(self):
        ventana = RegistrarEquipo(self)
        ventana.grab_set()

    def abrir_prestamo(self):
        ventana = PrestamoDashboard(self)  # ✅ Ahora la búsqueda de oficiales está dentro
        ventana.grab_set()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
