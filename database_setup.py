import sqlite3

# Conectar a la base de datos (se creará si no existe)
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Crear tabla de usuarios
c.execute('''
          CREATE TABLE IF NOT EXISTS users
          (username TEXT PRIMARY KEY, password TEXT, image BLOB)
          ''')
conn.commit()
conn.close()

print("Base de datos configurada exitosamente")
