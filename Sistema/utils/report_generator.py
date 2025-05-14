import os
import pandas as pd
from datetime import datetime
from fpdf import FPDF

class ReportGenerator:
    def __init__(self, ruta_historial):
        self.ruta_historial = ruta_historial
        if not os.path.exists(ruta_historial):
            raise FileNotFoundError("No se encontró el archivo de historial de préstamos")
        self.df = pd.read_excel(ruta_historial)
        self.df['Hora_Prestamo'] = pd.to_datetime(self.df['Hora_Prestamo'], errors='coerce')
        self.df['Hora_Devolucion'] = pd.to_datetime(self.df['Hora_Devolucion'], errors='coerce')

    def _generar_nombre_archivo(self, extension):
        ahora = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre = f"reporte_{ahora}.{extension}"

        carpeta = os.path.join(os.path.dirname(self.ruta_historial), "reportes")
        os.makedirs(carpeta, exist_ok=True)

        return os.path.join(carpeta, nombre)

    def filtrar(self, desde=None, hasta=None, oficial_id=None, estado=None, tipo_equipo=None):
        df = self.df.copy()

        if desde:
            df = df[df['Hora_Prestamo'] >= pd.to_datetime(desde)]
        if hasta:
            df = df[df['Hora_Prestamo'] <= pd.to_datetime(hasta)]
        if oficial_id:
            df = df[df['ID'].astype(str) == str(oficial_id)]
        if estado:
            df = df[df['Estado'].str.lower() == estado.lower()]
        if tipo_equipo:
            df = df[df['Tipo_Equipo'].str.lower() == tipo_equipo.lower()]

        return df

    def exportar_excel(self, df_filtrado, ruta_destino=None):
        if not ruta_destino:
            ruta_destino = self._generar_nombre_archivo("xlsx")
        df_filtrado.to_excel(ruta_destino, index=False)
        return ruta_destino

    def exportar_pdf(self, df_filtrado, ruta_destino=None, titulo="Reporte de Préstamos"):
        if not ruta_destino:
            ruta_destino = self._generar_nombre_archivo("pdf")

        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, titulo, ln=True, align='C')
        pdf.ln(10)

        columnas = ["ID", "Nombre", "ID_Equipo", "Nombre_Equipo", "Tipo_Equipo", "Hora_Prestamo", "Hora_Devolucion", "Estado"]
        col_widths = [25, 50, 25, 50, 40, 35, 35, 25]

        pdf.set_font("Arial", 'B', 10)
        for i, col in enumerate(columnas):
            pdf.cell(col_widths[i], 8, col, border=1)
        pdf.ln()

        pdf.set_font("Arial", '', 9)
        for _, row in df_filtrado.iterrows():
            pdf.cell(col_widths[0], 8, str(row["ID"]), border=1)
            pdf.cell(col_widths[1], 8, str(row["Nombre"])[0:30], border=1)
            pdf.cell(col_widths[2], 8, str(row["ID_Equipo"]), border=1)
            pdf.cell(col_widths[3], 8, str(row["Nombre_Equipo"])[0:30], border=1)
            pdf.cell(col_widths[4], 8, str(row["Tipo_Equipo"])[0:20], border=1)
            pdf.cell(col_widths[5], 8, row["Hora_Prestamo"].strftime('%Y-%m-%d') if pd.notnull(row["Hora_Prestamo"]) else '', border=1)
            pdf.cell(col_widths[6], 8, row["Hora_Devolucion"].strftime('%Y-%m-%d') if pd.notnull(row["Hora_Devolucion"]) else '', border=1)
            pdf.cell(col_widths[7], 8, str(row["Estado"])[0:10], border=1)
            pdf.ln()

        pdf.output(ruta_destino)


def generar_reporte(ruta_historial, desde=None, hasta=None, oficial_id=None, estado=None, tipo_equipo=None, tipo_archivo="pdf", ruta_destino="reporte.pdf"):
    rg = ReportGenerator(ruta_historial)
    df_filtrado = rg.filtrar(desde, hasta, oficial_id, estado, tipo_equipo)

    if tipo_archivo == "pdf":
        rg.exportar_pdf(df_filtrado, ruta_destino)
    elif tipo_archivo == "excel":
        rg.exportar_excel(df_filtrado, ruta_destino)
    else:
        raise ValueError("Tipo de archivo no válido: usa 'pdf' o 'excel'")
