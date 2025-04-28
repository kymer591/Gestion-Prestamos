import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
import uuid
from datetime import datetime
from views.seleccionar_equipos import SeleccionarEquipos
from views.gestion_grupo_devolucion import GestionarGrupoDevolucion

class PrestamoDashboard(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("Gestión de Préstamos de Equipos")
        self.geometry("1200x800")
        self.resizable(True, True)

        # Configuración de rutas
        self.configurar_rutas()

        self.oficial_actual = None
        self.crear_widgets()
        self.verificar_archivos()

    def configurar_rutas(self):
        """Configura las rutas de los archivos de datos"""
        base_path = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base_path, "..", "data")

        self.ruta_oficiales = os.path.abspath(os.path.join(data_path, "oficiales.xlsx"))
        self.ruta_equipos = os.path.abspath(os.path.join(data_path, "equipos.xlsx"))
        self.ruta_historial = os.path.abspath(os.path.join(data_path, "historial_prestamos.xlsx"))

    def verificar_archivos(self):
        """Verifica que los archivos necesarios existan y tengan la estructura correcta"""
        try:
            if not os.path.exists(self.ruta_oficiales):
                raise FileNotFoundError("Archivo de oficiales no encontrado")

            if not os.path.exists(self.ruta_equipos):
                raise FileNotFoundError("Archivo de equipos no encontrado")

            if not os.path.exists(self.ruta_historial):
                self.crear_historial_vacio()
            else:
                df = pd.read_excel(self.ruta_historial)
                if 'ID_Grupo' not in df.columns:
                    self.migrar_historial()

        except Exception as e:
            messagebox.showerror("Error", f"Error al verificar archivos:\n{str(e)}")
            self.destroy()

    def crear_historial_vacio(self):
        """Crea un archivo de historial vacío con la estructura correcta"""
        columns = [
            'ID', 'Nombre', 'Cargo', 'ID_Equipo', 'Nombre_Equipo',
            'Tipo_Equipo', 'Hora_Prestamo', 'Hora_Devolucion', 'Estado',
            'Observaciones', 'ID_Grupo'
        ]
        pd.DataFrame(columns=columns).to_excel(self.ruta_historial, index=False)

    def migrar_historial(self):
        """Migra el historial antiguo añadiendo ID_Grupo"""
        try:
            df = pd.read_excel(self.ruta_historial)
            if 'ID_Grupo' not in df.columns:
                df['ID_Grupo'] = [str(uuid.uuid4()) for _ in range(len(df))]
                df.to_excel(self.ruta_historial, index=False)
                messagebox.showinfo("Información", "Historial migrado a nueva versión")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo migrar el historial:\n{str(e)}")

    def crear_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        search_frame = ttk.LabelFrame(main_frame, text="Buscar Oficial", padding="10")
        search_frame.pack(fill=tk.X, pady=5)

        ttk.Label(search_frame, text="ID o Nombre del Oficial:").grid(row=0, column=0, padx=5)
        self.entry_busqueda = ttk.Entry(search_frame, width=30)
        self.entry_busqueda.grid(row=0, column=1, padx=5)

        ttk.Button(search_frame, text="Buscar", command=self.buscar_oficial).grid(row=0, column=2, padx=5)

        self.info_frame = ttk.LabelFrame(main_frame, text="Información del Oficial", padding="10")
        self.info_frame.pack(fill=tk.X, pady=5)

        self.lbl_nombre = ttk.Label(self.info_frame, text="Nombre: ")
        self.lbl_nombre.grid(row=0, column=0, sticky=tk.W, padx=5)

        self.lbl_cargo = ttk.Label(self.info_frame, text="Cargo: ")
        self.lbl_cargo.grid(row=0, column=1, sticky=tk.W, padx=5)

        self.lbl_id = ttk.Label(self.info_frame, text="ID: ")
        self.lbl_id.grid(row=0, column=2, sticky=tk.W, padx=5)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        ttk.Button(btn_frame, text="Nuevo Préstamo", command=self.abrir_ventana_equipos).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.cargar_historial).pack(side=tk.LEFT, padx=5)

        hist_frame = ttk.LabelFrame(main_frame, text="Historial de Préstamos Agrupados", padding="10")
        hist_frame.pack(fill=tk.BOTH, expand=True)

        columnas = ["ID", "Nombre", "Cargo", "Hora_Prestamo", "Total", "Devueltos", "Estado"]
        self.tree_historial = ttk.Treeview(hist_frame, columns=columnas, show="headings", selectmode="browse")

        for col in columnas:
            self.tree_historial.heading(col, text=col)
            self.tree_historial.column(col, width=150)

        scrollbar = ttk.Scrollbar(hist_frame, orient=tk.VERTICAL, command=self.tree_historial.yview)
        self.tree_historial.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_historial.pack(fill=tk.BOTH, expand=True)

        self.tree_historial.bind("<Double-1>", self.abrir_gestion_devolucion_grupal)

    def buscar_oficial(self):
        termino = self.entry_busqueda.get().strip()
        if not termino:
            messagebox.showwarning("Advertencia", "Ingrese un ID o nombre para buscar")
            return

        try:
            df = pd.read_excel(self.ruta_oficiales)
            mask = (df['ID'].astype(str).str.contains(termino)) | (df['Nombre'].str.contains(termino, case=False))
            resultados = df[mask]

            if resultados.empty:
                messagebox.showinfo("Información", "No se encontraron oficiales con ese criterio")
                return

            oficial = resultados.iloc[0]
            self.establecer_oficial_actual(oficial)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo buscar el oficial:\n{str(e)}")

    def establecer_oficial_actual(self, oficial):
        self.oficial_actual = {
            "ID": oficial['ID'],
            "Nombre": oficial['Nombre'],
            "Cargo": oficial['CARGO']
        }

        self.lbl_nombre.config(text=f"Nombre: {oficial['Nombre']}")
        self.lbl_cargo.config(text=f"Cargo: {oficial['CARGO']}")
        self.lbl_id.config(text=f"ID: {oficial['ID']}")

        self.cargar_historial()

    def cargar_historial(self):
        self.tree_historial.delete(*self.tree_historial.get_children())

        if not self.oficial_actual:
            return

        try:
            df = pd.read_excel(self.ruta_historial)
            df['Hora_Prestamo'] = pd.to_datetime(df['Hora_Prestamo'], errors='coerce')
            df_oficial = df[df['ID'] == self.oficial_actual['ID']]
            if df_oficial.empty:
                return

            grupos = df_oficial.groupby('Hora_Prestamo')
            for hora, grupo in grupos:
                total = len(grupo)
                devueltos = grupo['Estado'].str.lower().eq("devuelto").sum()
                estado = "Completado" if total == devueltos else ("Parcial" if devueltos > 0 else "Pendiente")

                self.tree_historial.insert("", "end", values=(
                    grupo.iloc[0]['ID'],
                    grupo.iloc[0]['Nombre'],
                    grupo.iloc[0]['Cargo'],
                    hora.strftime("%Y-%m-%d %H:%M"),
                    total,
                    devueltos,
                    estado
                ))

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar historial:\n{str(e)}")

    def abrir_ventana_equipos(self):
        if not self.oficial_actual:
            messagebox.showwarning("Advertencia", "Primero seleccione un oficial")
            return

        SeleccionarEquipos(
            parent=self,
            oficial=self.oficial_actual,
            ruta_historial=self.ruta_historial,
            ruta_equipos=self.ruta_equipos,
            callback=self.cargar_historial
        )

    def abrir_gestion_devolucion_grupal(self, event):
        seleccion = self.tree_historial.selection()
        if not seleccion:
            return

        item = self.tree_historial.item(seleccion[0])['values']
        hora_str = item[3]
        hora_prestamo = pd.to_datetime(hora_str)

        GestionarGrupoDevolucion(
            parent=self,
            id_oficial=item[0],
            hora_prestamo=hora_prestamo,
            ruta_historial=self.ruta_historial,
            ruta_equipos=self.ruta_equipos,
            callback=self.cargar_historial
        )