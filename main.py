# Importar módulos necesarios
from tkinter import *  # Importar todo desde la biblioteca tkinter
from registro import register  # Importar función register desde el módulo registro
from reconocimiento import recognize_face  # Importar función recognize_face desde el módulo reconocimiento
from login import login  # Importar función login desde el módulo login
from baja_usuario import delete_user  # Importar función delete_user desde el módulo baja_usuario

# Crear GUI principal
root = Tk()  # Crear una instancia de la clase Tk, que es la ventana principal
root.title("Sistema de Acceso")  # Establecer título de la ventana

# Obtener ancho y alto de la pantalla
ancho_pantalla = root.winfo_screenwidth()  # Obtener ancho de la pantalla
alto_pantalla = root.winfo_screenheight()  # Obtener alto de la pantalla

# Establecer ancho y alto de la ventana
ancho_ventana = 300  # Ancho de la ventana
alto_ventana = 250  # Alto de la ventana

# Calcular posición de la ventana en la pantalla
x = (ancho_pantalla - ancho_ventana) // 2  # Coordenada x para centrar la ventana
y = (alto_pantalla - alto_ventana) // 2  # Coordenada y para centrar la ventana

# Establecer geometría de la ventana
root.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")  # Establecer tamaño y posición de la ventana

# Deshabilitar redimensionamiento de la ventana
root.resizable(False, False)  # No permitir cambiar el tamaño de la ventana

# Crear botones
register_btn = Button(root, text="Registrar Usuario", command=register)  # Botón para registrar usuario
register_btn.pack(pady=10)  # Agregar botón a la ventana con un padding de 10 píxeles

recognize_btn = Button(root, text="Reconocer Rostro", command=recognize_face)  # Botón para reconocer rostro
recognize_btn.pack(pady=10)  # Agregar botón a la ventana con un padding de 10 píxeles

login_btn = Button(root, text="Iniciar Sesión", command=login)  # Botón para iniciar sesión
login_btn.pack(pady=10)  # Agregar botón a la ventana con un padding de 10 píxeles

delete_user_btn = Button(root, text="Dar de Baja Usuario", command=delete_user)  # Botón para dar de baja usuario
delete_user_btn.pack(pady=10)  # Agregar botón a la ventana con un padding de 10 píxeles

# Iniciar bucle principal de la GUI
root.mainloop()  # Iniciar el bucle principal de la GUI