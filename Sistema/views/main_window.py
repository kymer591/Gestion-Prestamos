import tkinter as tk
from tkinter import ttk

from views.registrar_oficial import RegistrarOficial
from views.registrar_equipo import RegistrarEquipo
from views.dashboard_prestamos import PrestamoDashboard

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Préstamos de Equipos - Unidad Policial")
        self.geometry("800x600")  # Solo un valor base
        self.state("zoomed")      # ✅ Maximiza la ventana (en Windows)
        self.resizable(True, True)  # ✅ Ahora puede redimensionarse
        
        self.configure(bg='#ecf0f1')
        
        self.crear_widgets()

    
    def crear_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(
            main_frame, 
            text="Sistema de Gestión de Préstamos", 
            style='Large.TLabel'
        ).pack(pady=20)
        
        # Logo (puedes reemplazar con tu propio logo)
        logo_frame = ttk.Frame(main_frame)
        logo_frame.pack(pady=20)
        # Aquí podrías agregar un Label con una imagen si lo deseas
        
        # Botones principales
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(
            button_frame, 
            text="Registrar Oficial", 
            command=self.abrir_registro_oficial,
            style='Primary.TButton',
            width=20
        ).pack(pady=10, fill=tk.X)
        
        ttk.Button(
            button_frame, 
            text="Registrar Equipo", 
            command=self.abrir_registro_equipo,
            style='Primary.TButton',
            width=20
        ).pack(pady=10, fill=tk.X)
        
        ttk.Button(
            button_frame, 
            text="Gestionar Préstamos", 
            command=self.abrir_prestamo,
            style='Success.TButton',
            width=20
        ).pack(pady=10, fill=tk.X)
        
        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(side=tk.BOTTOM, pady=20)
        
        ttk.Label(
            footer_frame, 
            text="Unidad Policial © 2023",
            style='TLabel'
        ).pack()
    
    def abrir_registro_oficial(self):
        ventana = RegistrarOficial(self)
        ventana.grab_set()
    
    def abrir_registro_equipo(self):
        ventana = RegistrarEquipo(self)
        ventana.grab_set()
    
    def abrir_prestamo(self):
        ventana = PrestamoDashboard(self)
        ventana.grab_set()
        