import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime

class SeleccionarEquipos(tk.Toplevel):
    def __init__(self, parent, oficial, ruta_historial, ruta_equipos, callback):
        super().__init__(parent)
        self.title("Seleccionar Equipos para Préstamo")
        self.geometry("1000x600")
        self.resizable(False, False)

        self.oficial = oficial
        self.ruta_historial = ruta_historial
        self.ruta_equipos = ruta_equipos
        self.callback = callback

        self.equipos_seleccionados = []

        self.crear_widgets()
        self.cargar_equipos_disponibles()

    def crear_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        info_frame = ttk.LabelFrame(main_frame, text=" Información del Oficial ", padding="10")
        info_frame.pack(fill=tk.X, pady=5)

        ttk.Label(info_frame, text=f"Nombre: {self.oficial['Nombre']}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Cargo: {self.oficial['Cargo']}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"ID: {self.oficial['ID']}").pack(anchor=tk.W)

        disp_frame = ttk.LabelFrame(main_frame, text=" Equipos Disponibles ", padding="10")
        disp_frame.pack(fill=tk.BOTH, expand=True)

        columns = ["ID_Equipo", "Nombre", "Estado"]
        self.tree_equipos = ttk.Treeview(
            disp_frame,
            columns=columns,
            show="headings",
            selectmode="extended"
        )

        for col in columns:
            self.tree_equipos.heading(col, text=col)
            self.tree_equipos.column(col, width=150)

        scrollbar = ttk.Scrollbar(disp_frame, orient=tk.VERTICAL, command=self.tree_equipos.yview)
        self.tree_equipos.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_equipos.pack(fill=tk.BOTH, expand=True)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        ttk.Button(
            btn_frame,
            text="Agregar Selección",
            command=self.agregar_seleccion
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text="Confirmar Préstamo",
            command=self.confirmar_prestamo
        ).pack(side=tk.RIGHT, padx=5)

        sel_frame = ttk.LabelFrame(main_frame, text=" Equipos Seleccionados ", padding="10")
        sel_frame.pack(fill=tk.BOTH, expand=True)

        self.tree_seleccionados = ttk.Treeview(
            sel_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.tree_seleccionados.heading(col, text=col)
            self.tree_seleccionados.column(col, width=150)

        scrollbar_sel = ttk.Scrollbar(sel_frame, orient=tk.VERTICAL, command=self.tree_seleccionados.yview)
        self.tree_seleccionados.configure(yscrollcommand=scrollbar_sel.set)
        scrollbar_sel.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_seleccionados.pack(fill=tk.BOTH, expand=True)

        ttk.Button(
            sel_frame,
            text="Quitar Selección",
            command=self.quitar_seleccion
        ).pack(pady=5)

    def cargar_equipos_disponibles(self):
        try:
            df = pd.read_excel(self.ruta_equipos)
            df_disponibles = df[df['Estado'] == 'Disponible']

            self.tree_equipos.delete(*self.tree_equipos.get_children())

            for _, row in df_disponibles.iterrows():
                self.tree_equipos.insert("", "end", values=(
                    row['ID_Equipo'],
                    row['Nombre'],
                    row['Estado']
                ))

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los equipos:\n{str(e)}")

    def agregar_seleccion(self):
        seleccionados = self.tree_equipos.selection()

        for item in seleccionados:
            valores = self.tree_equipos.item(item)['values']
            if not any(v[0] == valores[0] for v in self.equipos_seleccionados):
                self.equipos_seleccionados.append(valores)
                self.tree_seleccionados.insert("", "end", values=valores)

    def quitar_seleccion(self):
        seleccionados = self.tree_seleccionados.selection()

        for item in reversed(seleccionados):
            valores = self.tree_seleccionados.item(item)['values']
            self.equipos_seleccionados = [e for e in self.equipos_seleccionados if e[0] != valores[0]]
            self.tree_seleccionados.delete(item)

    def confirmar_prestamo(self):
        if not self.equipos_seleccionados:
            messagebox.showwarning("Advertencia", "Seleccione al menos un equipo")
            return

        try:
            try:
                df_historial = pd.read_excel(self.ruta_historial)
                df_historial['Observaciones'] = df_historial['Observaciones'].astype(str)
            except:
                df_historial = pd.DataFrame({
                    'ID': pd.Series(dtype='str'),
                    'Nombre': pd.Series(dtype='str'),
                    'Cargo': pd.Series(dtype='str'),
                    'ID_Equipo': pd.Series(dtype='str'),
                    'Nombre_Equipo': pd.Series(dtype='str'),
                    'Tipo_Equipo': pd.Series(dtype='str'),
                    'Hora_Prestamo': pd.Series(dtype='datetime64[ns]'),
                    'Hora_Devolucion': pd.Series(dtype='datetime64[ns]'),
                    'Estado': pd.Series(dtype='str'),
                    'Observaciones': pd.Series(dtype='str')
                })

            df_equipos = pd.read_excel(self.ruta_equipos)
            ahora = datetime.now()

            for equipo in self.equipos_seleccionados:
                nuevo_prestamo = {
                    'ID': self.oficial['ID'],
                    'Nombre': self.oficial['Nombre'],
                    'Cargo': self.oficial['Cargo'],
                    'ID_Equipo': equipo[0],
                    'Nombre_Equipo': equipo[1],
                    'Tipo_Equipo': '',
                    'Hora_Prestamo': ahora,
                    'Hora_Devolucion': pd.NaT,
                    'Estado': 'Prestado',
                    'Observaciones': ''
                }

                df_historial.loc[len(df_historial)] = nuevo_prestamo
                df_equipos.loc[df_equipos['ID_Equipo'] == equipo[0], 'Estado'] = 'Prestado'

            df_historial.to_excel(self.ruta_historial, index=False)
            df_equipos.to_excel(self.ruta_equipos, index=False)

            self.callback()
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el préstamo:\n{str(e)}")
