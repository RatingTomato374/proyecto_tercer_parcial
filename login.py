import sqlite3
from tkinter import simpledialog

def login():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    username = simpledialog.askstring("Login", "Nombre de usuario")
    password = simpledialog.askstring("Login", "Contraseña", show='*')
    
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    if c.fetchone():
        print("Inicio de sesión exitoso")
    else:
        print("Nombre de usuario o contraseña incorrectos")

    conn.close()
