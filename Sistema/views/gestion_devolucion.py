import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime

def registrar_devolucion(self):
    """Registra la devolución del equipo"""
    observaciones = self.txt_observaciones.get("1.0", tk.END).strip()

    try:
        df_historial = pd.read_excel(self.ruta_historial)
        df_equipos = pd.read_excel(self.ruta_equipos)

        # Verificar que las columnas necesarias existan
        columnas_necesarias = {'ID', 'ID_Equipo', 'Estado', 'Hora_Devolucion', 'Observaciones'}
        if not columnas_necesarias.issubset(df_historial.columns):
            messagebox.showerror("Error", "El archivo de historial no tiene las columnas necesarias.")
            return

        ahora = datetime.now()

        # Filtro para el préstamo pendiente
        mask = (
            (df_historial['ID'] == self.prestamo['ID']) &
            (df_historial['ID_Equipo'] == self.prestamo['ID_Equipo']) &
            (df_historial['Estado'] == 'Prestado')
        )

        if not df_historial[mask].empty:
            df_historial.loc[mask, 'Hora_Devolucion'] = ahora
            df_historial.loc[mask, 'Estado'] = 'Devuelto'
            df_historial['Observaciones'] = df_historial['Observaciones'].astype(str)
            df_historial.loc[mask, 'Observaciones'] = observaciones

            # Actualizar estado del equipo
            if 'ID_Equipo' in df_equipos.columns:
                df_equipos.loc[df_equipos['ID_Equipo'] == self.prestamo['ID_Equipo'], 'Estado'] = 'Disponible'

            df_historial.to_excel(self.ruta_historial, index=False)
            df_equipos.to_excel(self.ruta_equipos, index=False)

            messagebox.showinfo("Éxito", "Devolución registrada correctamente")
            self.callback()
            self.destroy()
        else:
            messagebox.showerror("Error", "No se encontró el préstamo para actualizar")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo registrar la devolución:\n{str(e)}")

    def __init__(self, parent, prestamo, ruta_historial, ruta_equipos, callback):
        super().__init__(parent)
        self.title("Gestión de Devolución")
        self.geometry("600x400")
        self.resizable(False, False)
        
        self.prestamo = prestamo
        self.ruta_historial = ruta_historial
        self.ruta_equipos = ruta_equipos
        self.callback = callback
        
        self.crear_widgets()
    
    def crear_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Información del préstamo
        info_frame = ttk.LabelFrame(main_frame, text=" Información del Préstamo ", padding="10")
        info_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(info_frame, text=f"Oficial: {self.prestamo['Nombre']}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Cargo: {self.prestamo['Cargo']}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"ID Oficial: {self.prestamo['ID']}").pack(anchor=tk.W)
        
        ttk.Label(info_frame, text=f"Equipo: {self.prestamo['Nombre_Equipo']}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Tipo: {self.prestamo['Tipo_Equipo']}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"ID Equipo: {self.prestamo['ID_Equipo']}").pack(anchor=tk.W)
        
        ttk.Label(info_frame, text=f"Fecha préstamo: {self.prestamo['Hora_Prestamo']}").pack(anchor=tk.W)
        
        # Observaciones
        obs_frame = ttk.LabelFrame(main_frame, text=" Observaciones ", padding="10")
        obs_frame.pack(fill=tk.X, pady=10)
        
        self.txt_observaciones = tk.Text(obs_frame, height=5, width=50)
        self.txt_observaciones.pack(fill=tk.BOTH, expand=True)
        
        # Botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            btn_frame, 
            text="Cancelar", 
            command=self.destroy,
            style='Danger.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Registrar Devolución", 
            command=self.registrar_devolucion,
            style='Success.TButton'
        ).pack(side=tk.RIGHT, padx=5)
    
    def registrar_devolucion(self):
        """Registra la devolución del equipo"""
        observaciones = self.txt_observaciones.get("1.0", tk.END).strip()
        
        try:
            # Leer archivos
            df_historial = pd.read_excel(self.ruta_historial)
            df_equipos = pd.read_excel(self.ruta_equipos)
            
            # Obtener fecha y hora actual
            ahora = datetime.now()
            
            # Actualizar historial
            mask = (
                (df_historial['ID'] == self.prestamo['ID']) & 
                (df_historial['ID_Equipo'] == self.prestamo['ID_Equipo']) & 
                (df_historial['Estado'] == 'Prestado')
            )
            
            if not df_historial[mask].empty:
                df_historial.loc[mask, 'Hora_Devolucion'] = ahora
                df_historial.loc[mask, 'Estado'] = 'Devuelto'
                df_historial.loc[mask, 'Observaciones'] = observaciones
                
                # Actualizar estado del equipo
                mask_equipo = df_equipos['ID'] == self.prestamo['ID_Equipo']
                df_equipos.loc[mask_equipo, 'Estado'] = 'Disponible'
                
                # Guardar cambios
                df_historial.to_excel(self.ruta_historial, index=False)
                df_equipos.to_excel(self.ruta_equipos, index=False)
                
                messagebox.showinfo("Éxito", "Devolución registrada correctamente")
                self.callback()
                self.destroy()
            else:
                messagebox.showerror("Error", "No se encontró el préstamo para actualizar")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la devolución:\n{str(e)}")