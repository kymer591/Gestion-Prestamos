import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
from datetime import datetime

class GestionDevolucion(tk.Toplevel):
    def __init__(self, parent, prestamo_info):
        super().__init__(parent)
        self.title("Gestión de Devolución")
        self.geometry("400x300")

        self.prestamo_info = prestamo_info

        tk.Label(self, text=f"Oficial: {prestamo_info['Nombre']} ({prestamo_info['ID']})").pack(pady=5)
        tk.Label(self, text=f"Equipo: {prestamo_info['Equipo']} - {prestamo_info['NombreEquipo']}").pack(pady=5)
        tk.Label(self, text=f"Fecha préstamo: {prestamo_info['FechaHoraPrestamo']}").pack(pady=5)

        ttk.Button(self, text="Registrar Devolución", command=self.registrar_devolucion).pack(pady=20)

    def registrar_devolucion(self):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(base_path, "..", "data")
            ruta_historial = os.path.join(data_path, "historial_prestamos.xlsx")
            ruta_equipos = os.path.join(data_path, "equipos.xlsx")

            df_historial = pd.read_excel(ruta_historial)
            df_equipos = pd.read_excel(ruta_equipos)

            # Actualizar historial
            idx = df_historial[(df_historial['ID'] == self.prestamo_info['ID']) &
                               (df_historial['Equipo'] == self.prestamo_info['Equipo']) &
                               (pd.isna(df_historial['HoraDevolucion']))].index

            if not idx.empty:
                df_historial.at[idx[0], 'HoraDevolucion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                df_historial.at[idx[0], 'Estado'] = "Equipo Devuelto"

                # Actualizar equipo a disponible
                df_equipos.loc[df_equipos['ID_Equipo'] == self.prestamo_info['Equipo'], 'Estado'] = 'Disponible'

                df_historial.to_excel(ruta_historial, index=False)
                df_equipos.to_excel(ruta_equipos, index=False)

                messagebox.showinfo("Éxito", "Equipo devuelto correctamente.")
                self.destroy()
            else:
                messagebox.showwarning("Aviso", "Este equipo ya fue devuelto.")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la devolución:\n{e}")
