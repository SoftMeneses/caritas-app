from models.db import Database
from mysql.connector import Error

class Voluntario:
    @staticmethod
    def obtener_voluntarios():
        conexion = Database.crear_conexion()

        cursor = conexion.cursor()
        try:
            cursor.execute('''
                SELECT v.ID_VOLUNTARIO, v.NOMBRE, v.CEDULA, v.TELEFONO, v.CORREO, v.DISPONIBILIDAD,
                    (
                        SELECT MAX(j.FECHA)
                        FROM jornadas_voluntarios jv
                        JOIN jornadas j ON jv.ID_JORNADA = j.ID_JORNADA
                        WHERE jv.ID_VOLUNTARIO = v.ID_VOLUNTARIO AND jv.PARTICIPACION = 1
                    ) AS ULTIMA_JORNADA
                FROM VOLUNTARIOS v
            ''')
            voluntario = cursor.fetchall() 
        except Error as e:
            print(f"Error al ejecutar la consulta: '{e}'")
            voluntario = None
        finally:
            cursor.close()
            conexion.close()
        
        return voluntario  

    @staticmethod
    def insertar_voluntario(voluntario, disponibilidad):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute('SELECT IFNULL(MAX(ID_VOLUNTARIO), 0) + 1 as next_id FROM VOLUNTARIOS')
            next_id = cursor.fetchone()[0]
            cursor.execute('INSERT INTO VOLUNTARIOS (ID_VOLUNTARIO, NOMBRE,CEDULA,CORREO,TELEFONO, DISPONIBILIDAD) VALUES (%s,%s, %s, %s, %s, %s)', 
                        (next_id, voluntario['nombre'], voluntario['cedula'], voluntario['email'], voluntario['telefono'], disponibilidad))
            conexion.commit() 
            return True
        except Error as e:
            print(f"Error al insertar el Voluntario: '{e}'")
            return False
        finally:
            cursor.close()
            conexion.close()
    @staticmethod
    def actualizar_voluntario(voluntario_id, voluntario, disponibilidad):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute('UPDATE VOLUNTARIOS SET nombre=%s, CORREO=%s, telefono=%s, CEDULA=%s, DISPONIBILIDAD=%s WHERE ID_VOLUNTARIO=%s', 
                        (voluntario['nombre'], voluntario['email'], voluntario['telefono'], voluntario['cedula'], disponibilidad, voluntario_id))
            conexion.commit()  
            return True
        except Error as e:
            print(f"Error al actualizar el voluntario: '{e}'")
            return False
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def eliminar_voluntario(voluntario_id):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute('DELETE FROM VOLUNTARIOS WHERE ID_VOLUNTARIO=%s', (voluntario_id,))
            conexion.commit()
            return True
        except Error as e:
            print(f"Error al eliminar el voluntario: '{e}'")
            return False
        finally:
            cursor.close()
            conexion.close()