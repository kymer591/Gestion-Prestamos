import tkinter as tk
import os
import sys

sys.path.append(os.path.dirname(__file__))

from views.login import LoginWindow
from views.main_window import MainWindow
from styles.style import configure_styles



from views.login import LoginWindow

def main():
    root = tk.Tk()
    root.withdraw()  # Evita la ventana blanca
    configure_styles()

    base_path = os.path.dirname(os.path.abspath(__file__))
    ruta_usuarios = os.path.join(base_path, "data", "usuarios.xlsx")

    def iniciar_aplicacion():
        app = MainWindow()
        app.mainloop()

    LoginWindow(ruta_usuarios=ruta_usuarios, on_success=iniciar_aplicacion)
    root.mainloop()

if __name__ == "__main__":
    main()
