import mysql.connector
from mysql.connector import Error

def crear_conexion():
    conexion = None
    try:
        conexion = mysql.connector.connect(
            host='localhost', 
            user='caritas',  
            password='caritas',  
            database='caritas',
            port=3307
        )
        print("Conexión a la base de datos exitosa")
    except Error as e:
        print(f"Error: '{e}'")

    return conexion

def verificar_usuario(usuario, password):
    conexion = crear_conexion()
    if conexion is None:
        return None, None  # Si no se pudo conectar, retorna None

    cursor = conexion.cursor()
    try:
        cursor.execute('SELECT u.*, r.nombre AS rol FROM usuarios u JOIN roles r ON u.rol_id = r.id WHERE u.usuario=%s AND u.password=%s', (usuario, password))
        user = cursor.fetchone()
    except Error as e:
        print(f"Error al ejecutar la consulta: '{e}'")
        user = None
    finally:
        cursor.close()
        conexion.close()
    
    return user 