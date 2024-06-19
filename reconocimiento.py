import cv2
import sqlite3
import numpy as np

def draw_guides(frame):
    # Dimensiones del frame
    height, width = frame.shape[:2]

    # Coordenadas del centro
    center_x, center_y = width // 2, height // 2

    # Tamaño del rectángulo de guía
    box_size = 200

    # Coordenadas del rectángulo
    top_left = (center_x - box_size // 2, center_y - box_size // 2)
    bottom_right = (center_x + box_size // 2, center_y + box_size // 2)

    # Dibujar el rectángulo de guía
    cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

    # Dibujar líneas guía (opcional)
    cv2.line(frame, (center_x, 0), (center_x, height), (0, 255, 0), 1)
    cv2.line(frame, (0, center_y), (width, center_y), (0, 255, 0), 1)

    return frame

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

        # Dibujar guías en el frame
        frame_with_guides = draw_guides(frame)

        # Mostrar el frame actual en la ventana
        cv2.imshow("Reconocer Rostro", frame_with_guides)
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

    # Cargar la imagen temporal y convertirla a escala de grises
    temp_img = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)
    if temp_img is None:
        print("Error: No se pudo cargar la imagen temporal.")
        return None

    # Consultar la base de datos para obtener las imágenes de los usuarios
    c.execute('SELECT username, image FROM users')
    users = c.fetchall()

    # Iterar sobre los usuarios y comparar la imagen temporal con cada una de ellas
    recognized_user = None
    for user in users:
        stored_img_data = user[1]
        stored_img = np.frombuffer(stored_img_data, np.uint8)
        stored_img = cv2.imdecode(stored_img, cv2.IMREAD_GRAYSCALE)

        # Comprobación de la coincidencia utilizando ORB y BFMatcher
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(temp_img, None)
        kp2, des2 = orb.detectAndCompute(stored_img, None)

        if des1 is not None and des2 is not None:
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.match(des1, des2)
            matches = sorted(matches, key=lambda x: x.distance)
            
            # Umbral para considerar una coincidencia
            good_matches = [m for m in matches if m.distance < 50]

            if len(good_matches) > 10:
                recognized_user = user[0]
                print(f"Usuario reconocido: {recognized_user}")
                break

    if recognized_user is None:
        print("No se reconoció ningún usuario")
    conn.close()
    return recognized_user

if __name__ == "__main__":
    recognized_user = recognize_face()
    if recognized_user:
        print(f"Usuario reconocido: {recognized_user}")
    else:
        print("No se pudo reconocer ningún usuario.")
