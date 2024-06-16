import sqlite3
import cv2
from tkinter import simpledialog, Tk, messagebox
import numpy as np

# Función para capturar la imagen del usuario
def capture_image(username):
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Capture Image")

    while True:
        ret, frame = cam.read()
        cv2.imshow("Capture Image", frame)
        if not ret:
            break
        k = cv2.waitKey(1)
        if k % 256 == 27:  # Presionar Esc para cerrar
            break
        elif k % 256 == 32:  # Presionar Space para capturar
            img_name = f"imagenes/{username}.png"
            cv2.imwrite(img_name, frame)
            print(f"Imagen {img_name} guardada!")
            break

    cam.release()
    cv2.destroyAllWindows()
    return img_name

# Función para detectar y extraer la cara de una imagen
def detect_face(image_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 0:
        return None
    
    # Extraer la cara (asumimos que hay solo una cara en la imagen)
    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        return face
    return None

# Función para comparar dos caras
def compare_faces(face1, face2):
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(face1, None)
    kp2, des2 = orb.detectAndCompute(face2, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)

    if len(matches) == 0:
        return False

    distances = [m.distance for m in matches]
    avg_distance = sum(distances) / len(distances)
    return avg_distance < 40  # Umbral de distancia promedio

# Función de registro
def register():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    root = Tk()
    root.withdraw()

    username = simpledialog.askstring("Registro", "Nombre de usuario")
    if not username:
        return

    # Verificar si el nombre de usuario ya existe
    c.execute('SELECT * FROM users WHERE username=?', (username,))
    if c.fetchone():
        messagebox.showerror("Error", "El nombre de usuario ya está registrado.")
        conn.close()
        return

    password = simpledialog.askstring("Registro", "Contraseña", show='*')
    if not password:
        return

    img_name = capture_image(username)
    new_face = detect_face(img_name)
    
    if new_face is None:
        messagebox.showerror("Error", "No se detectó ninguna cara en la imagen.")
        conn.close()
        return
    
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
