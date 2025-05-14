import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import os
from datetime import datetime
import pandas as pd

from utils.report_generator import ReportGenerator

class InterfazReportes(tk.Toplevel):
    def __init__(self, parent, ruta_historial):
        super().__init__(parent)
        self.title("Generador de Reportes")
        self.geometry("1000x600")
        self.resizable(True, True)
        self.ruta_historial = ruta_historial

        self.report_generator = ReportGenerator(ruta_historial)

        self.crear_widgets()

    def crear_widgets(self):
        filtro_frame = ttk.LabelFrame(self, text="Filtros de Búsqueda")
        filtro_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(filtro_frame, text="Desde:").grid(row=0, column=0, padx=5, pady=5)
        self.desde_entry = DateEntry(filtro_frame, date_pattern='yyyy-mm-dd')
        self.desde_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filtro_frame, text="Hasta:").grid(row=0, column=2, padx=5, pady=5)
        self.hasta_entry = DateEntry(filtro_frame, date_pattern='yyyy-mm-dd')
        self.hasta_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(filtro_frame, text="ID Oficial:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_id = ttk.Entry(filtro_frame)
        self.entry_id.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(filtro_frame, text="Estado:").grid(row=1, column=2, padx=5, pady=5)
        self.estado_combobox = ttk.Combobox(filtro_frame, values=["", "Prestado", "Devuelto"])
        self.estado_combobox.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(filtro_frame, text="Tipo de Equipo:").grid(row=2, column=0, padx=5, pady=5)
        self.tipo_combobox = ttk.Combobox(filtro_frame, values=self.obtener_tipos_equipo())
        self.tipo_combobox.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(filtro_frame, text="Aplicar Filtros", command=self.aplicar_filtros).grid(row=2, column=3, padx=5, pady=5)

        # Vista previa
        self.tree = ttk.Treeview(self, columns=("ID", "Nombre", "Equipo", "Tipo", "Prestamo", "Devolucion", "Estado"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Botones de exportar
        export_frame = ttk.Frame(self)
        export_frame.pack(pady=10)

        ttk.Button(export_frame, text="Exportar a PDF", command=self.exportar_pdf).pack(side=tk.LEFT, padx=10)
        ttk.Button(export_frame, text="Exportar a Excel", command=self.exportar_excel).pack(side=tk.LEFT, padx=10)

    def obtener_tipos_equipo(self):
        try:
            tipos = self.report_generator.df['Tipo_Equipo'].dropna().unique().tolist()
            tipos.insert(0, "")
            return tipos
        except:
            return [""]

    def aplicar_filtros(self):
        try:
            desde = self.desde_entry.get_date()
            hasta = self.hasta_entry.get_date()
            oficial_id = self.entry_id.get().strip() or None
            estado = self.estado_combobox.get().strip() or None
            tipo_equipo = self.tipo_combobox.get().strip() or None

            self.df_filtrado = self.report_generator.filtrar(
                desde=desde,
                hasta=hasta,
                oficial_id=oficial_id,
                estado=estado,
                tipo_equipo=tipo_equipo
            )

            self.tree.delete(*self.tree.get_children())

            for _, row in self.df_filtrado.iterrows():
                self.tree.insert("", "end", values=(
                    row['ID'],
                    row['Nombre'],
                    row['Nombre_Equipo'],
                    row['Tipo_Equipo'],
                    row['Hora_Prestamo'].strftime('%Y-%m-%d') if pd.notnull(row['Hora_Prestamo']) else '',
                    row['Hora_Devolucion'].strftime('%Y-%m-%d') if pd.notnull(row['Hora_Devolucion']) else '',
                    row['Estado']
                ))

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo filtrar datos:{str(e)}")

    def exportar_pdf(self):
        if hasattr(self, 'df_filtrado') and not self.df_filtrado.empty:
            try:
                path = self.report_generator.exportar_pdf(self.df_filtrado)
                messagebox.showinfo("Reporte PDF", f"Reporte generado en:{path}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar PDF:{str(e)}")
        else:
            messagebox.showwarning("Aviso", "Primero aplica los filtros.")

    def exportar_excel(self):
        if hasattr(self, 'df_filtrado') and not self.df_filtrado.empty:
            try:
                path = self.report_generator.exportar_excel(self.df_filtrado)
                messagebox.showinfo("Reporte Excel", f"Reporte generado en:{path}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar Excel:{str(e)}")
        else:
            messagebox.showwarning("Aviso", "Primero aplica los filtros.")
