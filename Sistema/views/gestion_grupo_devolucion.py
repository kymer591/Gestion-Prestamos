import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime

class GestionarGrupoDevolucion(tk.Toplevel):
    def __init__(self, parent, id_oficial, hora_prestamo, ruta_historial, ruta_equipos, callback):
        super().__init__(parent)
        self.title("Gestión de Devoluciones Grupales")
        self.geometry("900x500")
        self.resizable(False, False)

        self.id_oficial = str(id_oficial)
        self.hora_prestamo = hora_prestamo
        self.ruta_historial = ruta_historial
        self.ruta_equipos = ruta_equipos
        self.callback = callback

        self.df_historial = pd.read_excel(self.ruta_historial)
        self.df_historial['Hora_Prestamo'] = pd.to_datetime(self.df_historial['Hora_Prestamo'], errors='coerce')

        self.df_equipos = pd.read_excel(self.ruta_equipos)

        self.crear_widgets()
        self.cargar_prestamos()

    def crear_widgets(self):
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(
            frame,
            columns=("ID_Equipo", "Nombre_Equipo", "Estado", "Observaciones"),
            show="headings",
            selectmode="extended"
        )
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Botones
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Marcar como Devuelto", command=self.devolver_seleccionados).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cerrar", command=self.destroy).pack(side=tk.RIGHT, padx=5)

    def cargar_prestamos(self):
        self.tree.delete(*self.tree.get_children())

        # Formatear para comparar solo hasta el minuto
        hora_str = self.hora_prestamo.strftime('%Y-%m-%d %H:%M')

        grupo = self.df_historial[
            (self.df_historial['ID'].astype(str) == self.id_oficial) &
            (self.df_historial['Hora_Prestamo'].dt.strftime('%Y-%m-%d %H:%M') == hora_str)
        ]

        if grupo.empty:
            messagebox.showinfo("Sin resultados", "No se encontraron préstamos para este grupo.")
            return

        self.grupo_actual = grupo.copy()

        for _, row in grupo.iterrows():
            self.tree.insert("", "end", values=(
                row["ID_Equipo"],
                row["Nombre_Equipo"],
                row["Estado"],
                row.get("Observaciones", "")
            ))

    def devolver_seleccionados(self):
        seleccionados = self.tree.selection()
        if not seleccionados:
            messagebox.showwarning("Advertencia", "Seleccione al menos un equipo para devolver.")
            return

        ahora = datetime.now()
        hora_str = self.hora_prestamo.strftime('%Y-%m-%d %H:%M')

        for item in seleccionados:
            id_equipo = self.tree.item(item)["values"][0]

            mask = (
                (self.df_historial["ID"].astype(str) == self.id_oficial) &
                (self.df_historial["ID_Equipo"] == id_equipo) &
                (self.df_historial["Hora_Prestamo"].dt.strftime('%Y-%m-%d %H:%M') == hora_str)
            )

            self.df_historial.loc[mask, "Estado"] = "Devuelto"
            self.df_historial.loc[mask, "Hora_Devolucion"] = ahora
            self.df_historial['Observaciones'] = self.df_historial['Observaciones'].astype(str)
            self.df_historial.loc[mask, "Observaciones"] += " Devolución registrada."

            # Actualizar estado del equipo
            if "ID_Equipo" in self.df_equipos.columns:
                self.df_equipos.loc[self.df_equipos["ID_Equipo"] == id_equipo, "Estado"] = "Disponible"

        self.df_historial.to_excel(self.ruta_historial, index=False)
        self.df_equipos.to_excel(self.ruta_equipos, index=False)

        messagebox.showinfo("Éxito", "Devoluciones registradas correctamente.")
        self.callback()
        self.destroy()
