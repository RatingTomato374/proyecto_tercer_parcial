import sqlite3
import os
from tkinter import simpledialog, Tk, messagebox, Listbox, Scrollbar, Toplevel, Button, RIGHT, Y, BOTH, END

def get_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT username FROM users')
    users = [user[0] for user in c.fetchall()]
    conn.close()
    return users

def delete_user():
    def on_user_select(event):
        selected_user = user_listbox.get(user_listbox.curselection())
        confirm_delete(selected_user)

    def confirm_delete(username):
        if messagebox.askyesno("Confirmación", f"¿Estás seguro de que quieres eliminar al usuario '{username}'?"):
            conn = sqlite3.connect('users.db')
            c = conn.cursor()

            # Eliminar el usuario de la base de datos
            c.execute('DELETE FROM users WHERE username=?', (username,))
            conn.commit()

            # Eliminar la imagen del usuario (opcional)
            img_path = f"imagenes/{username}.png"
            if os.path.exists(img_path):
                os.remove(img_path)

            conn.close()
            messagebox.showinfo("Éxito", f"Usuario '{username}' dado de baja exitosamente")
            user_listbox.delete(user_listbox.curselection())

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    root = Tk()
    root.withdraw()

    users = get_users()
    if not users:
        messagebox.showinfo("Información", "No hay usuarios registrados.")
        return

    top = Toplevel(root)
    top.title("Seleccionar Usuario para Dar de Baja")
    top.geometry("300x250")

    scrollbar = Scrollbar(top)
    scrollbar.pack(side=RIGHT, fill=Y)

    user_listbox = Listbox(top, yscrollcommand=scrollbar.set)
    for user in users:
        user_listbox.insert(END, user)
    user_listbox.pack(pady=10, padx=10, fill=BOTH, expand=True)
    user_listbox.bind('<<ListboxSelect>>', on_user_select)

    scrollbar.config(command=user_listbox.yview)

    top.mainloop()

# Para ejecutar la función de baja de usuarios
if __name__ == "__main__":
    delete_user()
