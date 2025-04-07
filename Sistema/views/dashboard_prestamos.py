import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
from datetime import datetime

class PrestamoDashboard(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("Sistema de Préstamos de Equipos")
        self.geometry("1000x600")

        base_path = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base_path, "..", "data")

        self.ruta_oficiales = os.path.abspath(os.path.join(data_path, "oficiales.xlsx"))
        self.ruta_equipos = os.path.abspath(os.path.join(data_path, "equipos.xlsx"))
        self.ruta_historial = os.path.abspath(os.path.join(data_path, "historial.xlsx"))

        self.oficial_actual = None
        self.historial = self.cargar_historial()

        self.crear_widgets()

    def crear_widgets(self):
        frame_oficial = ttk.LabelFrame(self, text="Buscar Oficial")
        frame_oficial.pack(padx=10, pady=10, fill="x")

        tk.Label(frame_oficial, text="ID de Oficial:").pack(side="left", padx=5)
        self.entry_id_oficial = ttk.Entry(frame_oficial)
        self.entry_id_oficial.pack(side="left", padx=5)
        ttk.Button(frame_oficial, text="Buscar", command=self.buscar_oficial).pack(side="left", padx=5)

        self.label_info_oficial = ttk.Label(frame_oficial, text="")
        self.label_info_oficial.pack(side="left", padx=10)

        frame_botones = ttk.Frame(self)
        frame_botones.pack(pady=5)
        ttk.Button(frame_botones, text="Ver Equipos Disponibles", command=self.ver_equipos_disponibles).pack(side="left", padx=5)

        frame_tabla = ttk.LabelFrame(self, text="Historial del Oficial")
        frame_tabla.pack(padx=10, pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Equipo", "Fecha Préstamo", "Fecha Devolución", "Estado"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self.abrir_gestor_devolucion)

    def buscar_oficial(self):
        id_buscar = self.entry_id_oficial.get()
        try:
            df = pd.read_excel(self.ruta_oficiales)
            oficial = df[df['ID'].astype(str) == str(id_buscar)]

            if not oficial.empty:
                nombre = oficial.iloc[0]['Nombre']
                cargo = oficial.iloc[0]['CARGO']
                self.oficial_actual = (id_buscar, nombre)
                self.label_info_oficial.config(text=f"{cargo} {nombre} (ID: {id_buscar})", foreground="green")
                self.mostrar_historial()
            else:
                self.oficial_actual = None
                self.label_info_oficial.config(text="Oficial no encontrado", foreground="red")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo buscar el oficial:\n{e}")

    def ver_equipos_disponibles(self):
        if not self.oficial_actual:
            messagebox.showwarning("Advertencia", "Primero debe seleccionar un oficial.")
            return

        ventana = tk.Toplevel(self)
        ventana.title("Equipos Disponibles")
        ventana.geometry("600x400")

        tree_equipos = ttk.Treeview(ventana, columns=("ID_Equipo", "Nombre"), show="headings", selectmode="extended")
        tree_equipos.heading("ID_Equipo", text="Código")
        tree_equipos.heading("Nombre", text="Nombre")
        tree_equipos.pack(fill="both", expand=True)

        df = pd.read_excel(self.ruta_equipos)
        disponibles = df[df['Estado'] == "Disponible"]
        for _, row in disponibles.iterrows():
            tree_equipos.insert("", "end", values=(row["ID_Equipo"], row["Nombre"]))

        def confirmar_prestamo():
            seleccionados = tree_equipos.selection()
            if not seleccionados:
                messagebox.showinfo("Aviso", "No se seleccionaron equipos.")
                return

            for item in seleccionados:
                equipo_id = tree_equipos.item(item, "values")[0]
                equipo_nombre = tree_equipos.item(item, "values")[1]
                fecha_prestamo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.historial.loc[len(self.historial)] = [
                    self.oficial_actual[0],
                    self.oficial_actual[1],
                    equipo_id,
                    fecha_prestamo,
                    "",  # Fecha de devolución
                    "Equipo Prestado"
                ]
                df.loc[df["ID_Equipo"] == equipo_id, "Estado"] = "Prestado"

            df.to_excel(self.ruta_equipos, index=False)
            self.guardar_historial()
            self.mostrar_historial()
            ventana.destroy()

        ttk.Button(ventana, text="Confirmar Préstamo", command=confirmar_prestamo).pack(pady=10)

    def mostrar_historial(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        historial_filtrado = self.historial[self.historial["ID"] == self.oficial_actual[0]]
        for _, row in historial_filtrado.iterrows():
            self.tree.insert("", "end", values=tuple(row))

    def abrir_gestor_devolucion(self, event):
        item = self.tree.selection()[0]
        values = self.tree.item(item, "values")

        if values[5] == "Equipo Devuelto":
            messagebox.showinfo("Info", "Este equipo ya fue devuelto.")
            return

        ventana = tk.Toplevel(self)
        ventana.title("Devolución de Equipo")
        ventana.geometry("300x200")

        ttk.Label(ventana, text=f"Equipo: {values[2]}").pack(pady=10)
        ttk.Label(ventana, text=f"Préstamo realizado: {values[3]}").pack()

        def confirmar_devolucion():
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            index = self.historial[
                (self.historial["ID"] == values[0]) &
                (self.historial["Equipo"] == values[2]) &
                (self.historial["Fecha Préstamo"] == values[3])
            ].index

            if not index.empty:
                self.historial.loc[index, "Fecha Devolución"] = now
                self.historial.loc[index, "Estado"] = "Equipo Devuelto"

                df = pd.read_excel(self.ruta_equipos)
                df.loc[df["ID_Equipo"] == values[2], "Estado"] = "Disponible"
                df.to_excel(self.ruta_equipos, index=False)

                self.guardar_historial()
                self.mostrar_historial()
                ventana.destroy()
            else:
                messagebox.showerror("Error", "No se encontró el préstamo para actualizar.")

        ttk.Button(ventana, text="Confirmar Devolución", command=confirmar_devolucion).pack(pady=20)

    def cargar_historial(self):
        if os.path.exists(self.ruta_historial):
            return pd.read_excel(self.ruta_historial)
        return pd.DataFrame(columns=["ID", "Nombre", "Equipo", "Fecha Préstamo", "Fecha Devolución", "Estado"])

    def guardar_historial(self):
        self.historial.to_excel(self.ruta_historial, index=False)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = PrestamoDashboard()
    app.mainloop()
