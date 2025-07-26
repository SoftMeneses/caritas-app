from models.db import Database
from mysql.connector import Error

class UsuariosPerfilesModel:

    # --- PERFILES ---
    @staticmethod
    def obtener_perfiles():
        conexion = Database.crear_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("SELECT * FROM perfiles")
        perfiles = cursor.fetchall()
        cursor.close()
        conexion.close()
        return perfiles

    @staticmethod
    def agregar_perfil(nombre, permisos):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute(
                "INSERT INTO perfiles (NOMBRE, CONSULTA, MODIFICAR, INSERTAR, ELIMINAR, TOTAL) VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    nombre,
                    int(permisos.get("consulta", False)),
                    int(permisos.get("modificar", False)),
                    int(permisos.get("insertar", False)),
                    int(permisos.get("eliminar", False)),
                    int(permisos.get("total", False)),
                )
            )
            conexion.commit()
            return True
        except Exception as e:
            print("Error al agregar perfil:", e)
            return False
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def actualizar_perfil(perfil_id, nombre, permisos):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute(
                "UPDATE perfiles SET NOMBRE=%s, CONSULTA=%s, MODIFICAR=%s, INSERTAR=%s, ELIMINAR=%s, TOTAL=%s WHERE ID=%s",
                (
                    nombre,
                    int(permisos.get("consulta", False)),
                    int(permisos.get("modificar", False)),
                    int(permisos.get("insertar", False)),
                    int(permisos.get("eliminar", False)),
                    int(permisos.get("total", False)),
                    perfil_id
                )
            )
            conexion.commit()
            return True
        except Exception as e:
            print("Error al actualizar perfil:", e)
            return False
        finally:
            cursor.close()
            conexion.close()
            
    @staticmethod
    def eliminar_perfil(perfil_id):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor(dictionary=True)
        try:
            # Verificar si el perfil tiene usuarios asociados
            cursor.execute("SELECT COUNT(*) as count FROM usuarios WHERE PERFIL_ID = %s", (perfil_id,))
            resultado = cursor.fetchone()
            if resultado and resultado["count"] > 0:
                return False  # No se puede eliminar, hay usuarios asociados

            cursor.execute("DELETE FROM perfiles WHERE ID = %s", (perfil_id,))
            conexion.commit()
            return True
        except Exception as e:
            print("Error al eliminar perfil:", e)
            return False
        finally:
            cursor.close()
            conexion.close()

    # --- USUARIOS ---
    @staticmethod
    def obtener_usuarios():
        conexion = Database.crear_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.ID, u.USUARIO as nombre, u.EMAIL as email, u.PERFIL_ID as perfil_id, p.NOMBRE as perfil, u.PASSWORD as password,
                CONCAT(
                    IF(p.CONSULTA, 'Consultar/', ''),
                    IF(p.INSERTAR, 'Insertar/', ''),
                    IF(p.MODIFICAR, 'Modificar/', ''),
                    IF(p.TOTAL, 'Total', '')
                ) as permisos
            FROM usuarios u
            JOIN perfiles p ON u.PERFIL_ID = p.ID
        """)
        usuarios = cursor.fetchall()
        cursor.close()
        conexion.close()
        for u in usuarios:
            u["permisos"] = u["permisos"].rstrip("/")
        return usuarios

    @staticmethod
    def agregar_usuario(usuario):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor(dictionary=True)
        try:
            # Obtener el último ID y sumarle 1
            cursor.execute("SELECT IFNULL(MAX(ID), 0) + 1 as next_id FROM usuarios")
            next_id = cursor.fetchone()["next_id"]
            cursor.execute(
                "INSERT INTO usuarios (ID, USUARIO, EMAIL, PERFIL_ID, PASSWORD) VALUES (%s, %s, %s, %s, %s)",
                (
                    next_id,
                    usuario["nombre"],
                    usuario["email"],
                    usuario["perfil_id"],
                    usuario.get("password", "1234")  # Por defecto
                )
            )
            conexion.commit()
            return True
        except Exception as e:
            print("Error al agregar usuario:", e)
            return False
        finally:
            cursor.close()
            conexion.close()
    @staticmethod
    def actualizar_usuario(usuario_id, datos):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute(
                "UPDATE usuarios SET USUARIO=%s, EMAIL=%s, PERFIL_ID=%s, PASSWORD=%s WHERE ID=%s",
                (
                    datos["nombre"],
                    datos["email"],
                    datos["perfil_id"],
                    datos["password"],
                    usuario_id
                )
            )
            conexion.commit()
            return True
        except Exception as e:
            print("Error al actualizar usuario:", e)
            return False
        finally:
            cursor.close()
            conexion.close()



    @staticmethod
    def eliminar_usuario(usuario_id):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute("DELETE FROM usuarios WHERE ID = %s", (usuario_id,))
            conexion.commit()
            return True
        except Exception as e:
            print("Error al eliminar usuario:", e)
            return False
        finally:
            cursor.close()
            conexion.close()

