from tkinter import *
from registro import register
from reconocimiento import recognize_face
from login import login
from baja_usuario import delete_user

# Crear GUI principal
root = Tk()
root.title("Sistema de Acceso")

ancho_pantalla = root.winfo_screenwidth()
alto_pantalla = root.winfo_screenheight()

ancho_ventana = 300
alto_ventana = 250

x = (ancho_pantalla - ancho_ventana) // 2
y = (alto_pantalla - alto_ventana) // 2

root.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

root.resizable(False, False)

register_btn = Button(root, text="Registrar Usuario", command=register)
register_btn.pack(pady=10)

recognize_btn = Button(root, text="Reconocer Rostro", command=recognize_face)
recognize_btn.pack(pady=10)

login_btn = Button(root, text="Iniciar Sesión", command=login)
login_btn.pack(pady=10)

delete_user_btn = Button(root, text="Dar de Baja Usuario", command=delete_user)
delete_user_btn.pack(pady=10)

root.mainloop()
