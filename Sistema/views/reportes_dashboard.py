import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import os

from ..utils.report_generator import filtrar_historial, generar_pdf, generar_excel

class ReportesDashboard(tk.Toplevel):
    def __init__(self, ruta_historial):
        super().__init__()
        self.title("Generador de Reportes")
        self.geometry("900x600")
        self.configure(bg="white")

        self.ruta_historial = ruta_historial

        self.crear_widgets()

    def crear_widgets(self):
        # Filtros
        frame_filtros = tk.LabelFrame(self, text="Filtros", padx=10, pady=10, bg="white")
        frame_filtros.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_filtros, text="Fecha inicio:", bg="white").grid(row=0, column=0)
        self.fecha_inicio = DateEntry(frame_filtros, width=12, background='darkblue', foreground='white', date_pattern='yyyy-mm-dd')
        self.fecha_inicio.grid(row=0, column=1, padx=5)

        tk.Label(frame_filtros, text="Fecha fin:", bg="white").grid(row=0, column=2)
        self.fecha_fin = DateEntry(frame_filtros, width=12, background='darkblue', foreground='white', date_pattern='yyyy-mm-dd')
        self.fecha_fin.grid(row=0, column=3, padx=5)

        tk.Label(frame_filtros, text="CI Oficial:", bg="white").grid(row=0, column=4)
        self.entry_ci = tk.Entry(frame_filtros)
        self.entry_ci.grid(row=0, column=5, padx=5)

        self.btn_filtrar = tk.Button(frame_filtros, text="Filtrar", command=self.aplicar_filtros)
        self.btn_filtrar.grid(row=0, column=6, padx=10)

        # Tabla de vista previa
        self.tabla = ttk.Treeview(self, columns=("fecha_prestamo", "ci", "nombre", "equipo", "estado", "fecha_devolucion"), show="headings")
        for col in self.tabla["columns"]:
            self.tabla.heading(col, text=col.replace("_", " ").capitalize())
            self.tabla.column(col, anchor="center")
        self.tabla.pack(expand=True, fill="both", padx=10, pady=10)

        # Botones de exportación
        frame_botones = tk.Frame(self, bg="white")
        frame_botones.pack(fill="x", pady=10)

        self.btn_pdf = tk.Button(frame_botones, text="Exportar a PDF", command=self.exportar_pdf)
        self.btn_pdf.pack(side="left", padx=10)

        self.btn_excel = tk.Button(frame_botones, text="Exportar a Excel", command=self.exportar_excel)
        self.btn_excel.pack(side="left")

    def aplicar_filtros(self):
        inicio = self.fecha_inicio.get_date()
        fin = self.fecha_fin.get_date()
        ci = self.entry_ci.get().strip()

        self.resultados = filtrar_historial(self.ruta_historial, inicio, fin, ci)

        for row in self.tabla.get_children():
            self.tabla.delete(row)

        for fila in self.resultados:
            self.tabla.insert("", "end", values=fila)

    def exportar_pdf(self):
        if not self.resultados:
            messagebox.showwarning("Sin datos", "Debe filtrar datos antes de exportar.")
            return

        ruta = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if ruta:
            generar_pdf(self.resultados, ruta)
            messagebox.showinfo("Éxito", "PDF generado correctamente.")

    def exportar_excel(self):
        if not self.resultados:
            messagebox.showwarning("Sin datos", "Debe filtrar datos antes de exportar.")
            return

        ruta = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
        if ruta:
            generar_excel(self.resultados, ruta)
            messagebox.showinfo("Éxito", "Archivo Excel generado correctamente.")
