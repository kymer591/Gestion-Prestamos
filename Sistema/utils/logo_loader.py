import os
from PIL import Image, ImageTk

def cargar_logo():
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        ruta = os.path.join(base_dir, "Sistema", "assets", "logo.png")
    
        
        print(f"Verificando ruta: {ruta}")
        print(f"¿Existe el archivo? {os.path.exists(ruta)}")
        
        if not os.path.exists(ruta):
            print("❌ Error: El archivo no existe en la ruta especificada")
            return None
            
        # Usa Pillow para cargar la imagen
        from PIL import Image, ImageTk
        img_pil = Image.open(ruta)
        img_tk = ImageTk.PhotoImage(img_pil)
        print("✅ Imagen convertida correctamente a PhotoImage")
        return img_tk
        
    except Exception as e:
        print(f"🚨 Error crítico al cargar imagen: {str(e)}")
        return None