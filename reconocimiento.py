import cv2
import sqlite3
import numpy as np

def recognize_face():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Recognize Face")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Error: No se pudo acceder a la cámara")
            break

        cv2.imshow("Recognize Face", frame)
        k = cv2.waitKey(1)
        if k % 256 == 27:  # Presionar Esc para cerrar
            break
        elif k % 256 == 32:  # Presionar Space para capturar y reconocer
            img_name = "temp.png"
            cv2.imwrite(img_name, frame)
            print(f"Imagen {img_name} guardada para reconocimiento!")
            break

    cam.release()
    cv2.destroyAllWindows()

    # Cargar la imagen temporal
    temp_img = cv2.imread(img_name, 0)

    # Comparar con las imágenes almacenadas
    c.execute('SELECT username, image FROM users')
    users = c.fetchall()

    for user in users:
        stored_img = np.frombuffer(user[1], np.uint8)
        stored_img = cv2.imdecode(stored_img, cv2.IMREAD_GRAYSCALE)
        
        # Utilizar comparación de histogramas u otros métodos de reconocimiento
        res = cv2.matchTemplate(temp_img, stored_img, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)

        if max_val > 0.9:  # Umbral de coincidencia
            print(f"Usuario reconocido: {user[0]}")
            return user[0]

    print("No se reconoció ningún usuario")
    return None
