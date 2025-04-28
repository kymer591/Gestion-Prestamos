def configure_styles():
    """Configura los estilos visuales de la aplicación"""
    import tkinter.ttk as ttk
    
    style = ttk.Style()
    
    # Fuentes
    font_normal = ('Helvetica', 10)
    font_title = ('Helvetica', 12, 'bold')
    font_large = ('Helvetica', 14)
    
    # Colores
    primary_color = '#2c3e50'
    secondary_color = '#3498db'
    success_color = '#27ae60'
    danger_color = '#e74c3c'
    light_bg = '#ecf0f1'
    
    # Configuración general
    style.configure('.', font=font_normal, background=light_bg)
    
    # Configuración de widgets específicos
    style.configure('TFrame', background=light_bg)
    style.configure('TLabel', background=light_bg)
    style.configure('TButton', padding=6)
    style.configure('Primary.TButton', foreground='white', background=primary_color)
    style.configure('Success.TButton', foreground='white', background=success_color)
    style.configure('Danger.TButton', foreground='white', background=danger_color)
    
    style.configure('Title.TLabel', font=font_title, foreground=primary_color)
    style.configure('Large.TLabel', font=font_large, foreground=primary_color)
    
    style.configure('Treeview', rowheight=25)
    style.configure('Treeview.Heading', font=('Helvetica', 10, 'bold'))
    style.map('Treeview', background=[('selected', secondary_color)])