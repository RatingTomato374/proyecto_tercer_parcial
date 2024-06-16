import cv2
import sqlite3
import numpy as np

def recognize_face():
    # Conectar a la base de datos de usuarios
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Inicializar la cámara
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Reconocer Rostro")

    # Bucle principal para capturar frames de la cámara
    while True:
        ret, frame = cam.read()
        if not ret:
            print("Error: No se pudo acceder a la cámara")
            break

        # Mostrar el frame actual en la ventana
        cv2.imshow("Reconocer Rostro", frame)
        k = cv2.waitKey(1)
        if k % 256 == 27:  # Presionar Esc para cerrar
            break
        elif k % 256 == 32:  # Presionar Space para capturar y reconocer
            img_name = "temp.png"
            cv2.imwrite(img_name, frame)
            print(f"Imagen {img_name} guardada para reconocimiento!")
            break

    # Liberar recursos de la cámara
    cam.release()
    cv2.destroyAllWindows()

    # Cargar la imagen temporal
    temp_img = cv2.imread(img_name, 0)

    # Consultar la base de datos para obtener las imágenes de los usuarios
    c.execute('SELECT username, image FROM users')
    users = c.fetchall()

    # Iterar sobre los usuarios y comparar la imagen temporal con cada una de ellas
    for user in users:
        stored_img = np.frombuffer(user[1], np.uint8)
        stored_img = cv2.imdecode(stored_img, cv2.IMREAD_GRAYSCALE)
        
        # Utilizar comparación de histogramas u otros métodos de reconocimiento
        res = cv2.matchTemplate(temp_img, stored_img, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)

        # Verificar si la coincidencia es lo suficientemente alta
        if max_val > 0.9:  # Umbral de coincidencia
            print(f"Usuario reconocido: {user[0]}")
            return user[0]

    print("No se reconoció ningún usuario")
    return None