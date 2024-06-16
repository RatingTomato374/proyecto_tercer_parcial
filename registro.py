import sqlite3
import cv2
from tkinter import simpledialog, Tk, messagebox
import numpy as np

# Función para capturar la imagen del usuario
def capture_image(username):
    # Inicializar la cámara
    cam = cv2.VideoCapture(0)
    # Crear una ventana para mostrar la imagen
    cv2.namedWindow("Capture Image")

    while True:
        # Leer un frame de la cámara
        ret, frame = cam.read()
        # Mostrar el frame en la ventana
        cv2.imshow("Capture Image", frame)
        # Si no se puede leer el frame, salir del bucle
        if not ret:
            break
        # Leer una tecla presionada
        k = cv2.waitKey(1)
        # Si se presiona la tecla Esc, salir del bucle
        if k % 256 == 27:
            break
        # Si se presiona la tecla Space, capturar la imagen
        elif k % 256 == 32:
            # Crear el nombre de la imagen con el username
            img_name = f"imagenes/{username}.png"
            # Guardar la imagen en el disco
            cv2.imwrite(img_name, frame)
            print(f"Imagen {img_name} guardada!")
            break

    # Liberar recursos de la cámara
    cam.release()
    cv2.destroyAllWindows()
    return img_name

# Función para detectar y extraer la cara de una imagen
def detect_face(image_path):
    # Cargar el clasificador de caras
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # Leer la imagen
    image = cv2.imread(image_path)
    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Detectar caras en la imagen
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Si no se detecta ninguna cara, regresar None
    if len(faces) == 0:
        return None
    
    # Extraer la cara (asumimos que hay solo una cara en la imagen)
    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        return face
    return None

# Función para comparar dos caras
def compare_faces(face1, face2):
    # Crear un objeto ORB para detectar características
    orb = cv2.ORB_create()
    # Detectar características en las dos caras
    kp1, des1 = orb.detectAndCompute(face1, None)
    kp2, des2 = orb.detectAndCompute(face2, None)

    # Crear un objeto BFMatcher para comparar características
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    # Encontrar coincidencias entre las características
    matches = bf.match(des1, des2)

    # Si no se encuentran coincidencias, regresar False
    if len(matches) == 0:
        return False

    # Calcular la distancia promedio entre las coincidencias
    distances = [m.distance for m in matches]
    avg_distance = sum(distances) / len(distances)
    # Regresar True si la distancia promedio es menor que 40
    return avg_distance < 40

# Función de registro
def register():
    # Conectar a la base de datos
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Crear una ventana para pedir el username y contraseña
    root = Tk()
    root.withdraw()

    # Pedir el username
    username = simpledialog.askstring("Registro", "Nombre de usuario")
    if not username:
        return

    # Verificar si el nombre de usuario ya existe
    c.execute('SELECT * FROM users WHERE username=?', (username,))
    if c.fetchone():
        messagebox.showerror("Error", "El nombre de usuario ya está registrado.")
        conn.close()
        return

    # Pedir la contraseña
    password = simpledialog.askstring("Registro", "Contraseña", show='*')
    if not password:
        return

    # Capturar la imagen del usuario
    img_name = capture_image(username)
    new_face = detect_face(img_name)
    
    # Si no se detecta ninguna cara, mostrar un error
    if new_face is None:
        messagebox.showerror("Error", "No se detectó ninguna cara en la imagen.")
        conn.close()
        return
    
    # Codificar la cara en bytes
    new_face_encoded = cv2.imencode('.png', new_face)[1].tobytes()

    # Verificar si la cara ya existe
    c.execute('SELECT username, image FROM users')
    users = c.fetchall()

    for user in users:
        stored_img = np.frombuffer(user[1], np.uint8)
        stored_face = cv2.imdecode(stored_img, cv2.IMREAD_GRAYSCALE)
        
        if stored_face is not None and compare_faces(new_face, stored_face):
            messagebox.showerror("Error", "La cara ya está registrada.")
            conn.close()
            return

    c.execute('INSERT INTO users (username, password, image) VALUES (?, ?, ?)', 
              (username, password, new_face_encoded))
    conn.commit()
    conn.close()
    messagebox.showinfo("Éxito", "Usuario registrado exitosamente")

# Para ejecutar la función de registro
if __name__ == "__main__":
    register()
