# Sistema de Registro y Acceso con Reconocimiento Facial

## Descripción del Proyecto

Este proyecto implementa un sistema de registro y acceso utilizando reconocimiento facial. Los usuarios pueden registrarse capturando una foto, y luego iniciar sesión utilizando su rostro o credenciales tradicionales (nombre de usuario y contraseña). Además, se incluye la funcionalidad para dar de baja usuarios existentes.

## Requisitos del Sistema

- Python 3.10+
- Librerías de Python:
  - `opencv-python`
  - `Pillow`
  - `tkinter`
  - `numpy`
- Base de datos SQLite para almacenamiento de usuarios e imágenes

## Instalación

### Paso 1: Clonar el repositorio

```bash
1.- git clone <URL-del-repositorio>  
2.- cd proyecto_tercer_parcial  
3.- Cuando se descarga el proyecto, dentro de la carpeta proyecto_tercer_parcial, crear una carpeta que se llame imagenes  
4.- Despues de crear la carpeta, abrimos la terminal (Powershell)  
5.- Dentro de la terminal, movernos hasta la carpeta del proyecto  
6.- Cuando estemos en la carpeta, creamos el ambiente virtual con el comnando:  python -m venv env  
7.- Despues activamos el ambiente con el comando:  .\env\Scripts\activate  
8.- Instalamos los requerimientos con el comando:  pip install -r requirements.txt  
9.- Cuando esten instalados los requerimientos, creamos la base de datos ejecutando el comando:  python database_setup.py  
10.- Una vez creada la base de datos ejecutamos el programa con: python main.py  
