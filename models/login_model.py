from models.db import Database
from mysql.connector import Error

class Usuario:
    @staticmethod
    def verificar_usuario(usuario, password):
        conexion = Database.crear_conexion()
        if conexion is None:
            return None, None  # Si no se pudo conectar, retorna None

        cursor = conexion.cursor()
        try:
            # Comparación case sensitive usando BINARY
            cursor.execute('SELECT u.*, p.nombre AS perfil FROM usuarios u JOIN perfiles p ON u.perfil_id = p.id WHERE BINARY u.usuario=%s AND BINARY u.password=%s', (usuario, password))
            user = cursor.fetchone()
        except Error as e:
            print(f"Error al ejecutar la consulta: '{e}'")
            user = None
        finally:
            cursor.close()
            conexion.close()
        
        return user 

    @staticmethod
    def autenticar(usuario, password):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor(dictionary=True)
        # Comparación case sensitive usando BINARY
        cursor.execute("""
            SELECT u.ID, u.USUARIO, u.PERFIL_ID, p.NOMBRE as perfil,
                p.CONSULTA, p.INSERTAR, p.MODIFICAR,P.ELIMINAR, p.TOTAL
            FROM usuarios u
            JOIN perfiles p ON u.PERFIL_ID = p.ID
            WHERE BINARY u.USUARIO = %s AND BINARY u.PASSWORD = %s
        """, (usuario, password))
        user = cursor.fetchone()
        cursor.close()
        conexion.close()
        if user:
            # Convierte los permisos a booleanos
            user["consulta"] = bool(user["CONSULTA"])
            user["insertar"] = bool(user["INSERTAR"])
            user["modificar"] = bool(user["MODIFICAR"])
            user["eliminar"] = bool(user["ELIMINAR"])
            user["total"] = bool(user["TOTAL"])
            return user
        return None