# Importación de módulos necesarios
import sqlite3  # para interactuar con la base de datos SQLite
from tkinter import simpledialog  # para crear diálogos de entrada de usuario

# Función para manejar el proceso de inicio de sesión
def login():
    # Establecer conexión a la base de datos
    conn = sqlite3.connect('users.db')  # conexión a la base de datos users.db
    c = conn.cursor()  # crear un cursor para interactuar con la base de datos

    # Solicitar credenciales de usuario
    username = simpledialog.askstring("Login", "Nombre de usuario")  # solicitar nombre de usuario
    password = simpledialog.askstring("Login", "Contraseña", show='*')  # solicitar contraseña (mostrar como asteriscos)

    # Verificar credenciales en la base de datos
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))  # consulta SQL para buscar usuario
    if c.fetchone():  # si se encuentra un usuario que coincida
        print("Inicio de sesión exitoso")  # imprimir mensaje de éxito
    else:
        print("Nombre de usuario o contraseña incorrectos")  # imprimir mensaje de error

    # Cerrar la conexión a la base de datos
    conn.close()  # liberar recursos