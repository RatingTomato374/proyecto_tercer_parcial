# Importar módulos necesarios
import sqlite3  # para operaciones de base de datos
import os  # para operaciones de sistema de archivos
from tkinter import (
    simpledialog,  # para diálogos simples
    Tk,  # para crear la ventana principal
    messagebox,  # para mostrar mensajes emergentes
    Listbox,  # para crear una lista desplegable
    Scrollbar,  # para crear una barra de desplazamiento
    Toplevel,  # para crear una ventana emergente
    Button,  # para crear un botón
    RIGHT,  # para especificar el lado derecho de un widget
    Y,  # para especificar la dirección vertical
    BOTH,  # para especificar ambas direcciones horizontal y vertical
    END  # para especificar el final de una lista desplegable
)

# Definir una función para recuperar todos los usuarios registrados
def get_users():
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Ejecutar una consulta SQL para recuperar todos los nombres de usuario de la tabla users
    c.execute('SELECT username FROM users')
    
    # Recuperar todos los resultados y extraer los nombres de usuario
    users = [user[0] for user in c.fetchall()]
    
    # Cerrar la conexión a la base de datos
    conn.close()
    
    # Devolver la lista de nombres de usuario
    return users

# Definir una función para eliminar un usuario
def delete_user():
    # Definir una función anidada para manejar la selección de usuario
    def on_user_select(event):
        # Obtener el nombre de usuario seleccionado de la lista desplegable
        selected_user = user_listbox.get(user_listbox.curselection())
        
        # Llamar a la función confirm_delete para confirmar la eliminación
        confirm_delete(selected_user)
    
    # Definir una función anidada para confirmar la eliminación
    def confirm_delete(username):
        # Preguntar al usuario si está seguro de eliminar al usuario
        if messagebox.askyesno("Confirmación", f"¿Estás seguro de que quieres eliminar al usuario '{username}'?"):
            # Conectar a la base de datos SQLite
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            
            # Eliminar al usuario de la base de datos
            c.execute('DELETE FROM users WHERE username=?', (username,))
            conn.commit()
            
            # Eliminar el archivo de imagen del usuario (si existe)
            img_path = f"imagenes/{username}.png"
            if os.path.exists(img_path):
                os.remove(img_path)
            
            # Cerrar la conexión a la base de datos
            conn.close()
            
            # Mostrar un mensaje de éxito
            messagebox.showinfo("Éxito", f"Usuario '{username}' dado de baja exitosamente")
            
            # Eliminar al usuario de la lista desplegable
            user_listbox.delete(user_listbox.curselection())
    
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Crear una ventana principal (oculta por ahora)
    root = Tk()
    root.withdraw()
    
    # Obtener la lista de usuarios registrados
    users = get_users()
    
    # Si no hay usuarios registrados, mostrar un mensaje y salir
    if not users:
        messagebox.showinfo("Información", "No hay usuarios registrados.")
        return
    
    # Crear una ventana emergente para eliminar usuarios
    top = Toplevel(root)
    top.title("Seleccionar Usuario para Dar de Baja")
    top.geometry("300x250")
    
    # Crear una barra de desplazamiento para la lista desplegable
    scrollbar = Scrollbar(top)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    # Crear una lista desplegable para mostrar los usuarios registrados
    user_listbox = Listbox(top, yscrollcommand=scrollbar.set)
    for user in users:
        user_listbox.insert(END, user)
    user_listbox.pack(pady=10, padx=10, fill=BOTH, expand=True)
    
    # Enlazar la lista desplegable con la función on_user_select
    user_listbox.bind('<<ListboxSelect>>', on_user_select)
    
    # Configurar la barra de desplazamiento para trabajar con la lista desplegable
    scrollbar.config(command=user_listbox.yview)
    
    # Iniciar el bucle de eventos de la GUI
    top.mainloop()

# Para ejecutar la función de baja de usuarios
if __name__ == "__main__":
    delete_user()
