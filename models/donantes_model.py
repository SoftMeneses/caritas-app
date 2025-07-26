from models.db import Database
from mysql.connector import Error

class Donante:
    @staticmethod
    def obtener_donantes():
        conexion = Database.crear_conexion()

        cursor = conexion.cursor()
        try:
            cursor.execute('SELECT ID_DONANTE, NOMBRE, TELEFONO, CORREO, CEDULA, DIRECCION,IFNULL((SELECT MAX(FECHA) FROM DONACIONES WHERE DONANTE_ID = ID_DONANTE),"Sin Donacion" )AS ULTIMA_DONACION FROM DONANTES')
            donante = cursor.fetchall() 
        except Error as e:
            print(f"Error al ejecutar la consulta: '{e}'")
            donante = None
        finally:
            cursor.close()
            conexion.close()
        
        return donante  


    @staticmethod
    def insertar_donante(donante):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute('SELECT IFNULL(MAX(ID_DONANTE), 0) + 1 as next_id FROM DONANTES')
            next_id = cursor.fetchone()[0]
            cursor.execute('INSERT INTO DONANTES (ID_DONANTE, NOMBRE,CORREO,TELEFONO,CEDULA, DIRECCION) VALUES (%s, %s, %s,%s, %s, %s)', 
                        (next_id, donante['nombre'], donante['email'], donante['telefono'],donante['cedula'],donante['direccion']))
            conexion.commit() 
            return True
        except Error as e:
            print(f"Error al insertar el donante: '{e}'")
            return False
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def actualizar_donante(donante_id, donante):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute('UPDATE DONANTES SET nombre=%s, CORREO=%s, telefono=%s,CEDULA=%s,DIRECCION=%s WHERE id_donante=%s', 
                        (donante['nombre'], donante['email'], donante['telefono'],donante['cedula'],donante['direccion'], donante_id))
            conexion.commit()  
            return True
        except Error as e:
            print(f"Error al actualizar el donante: '{e}'")
            return False
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def eliminar_donante(donante_id):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute('DELETE FROM DONANTES WHERE ID_DONANTE=%s', (donante_id,))
            conexion.commit()
            return True
        except Error as e:
            print(f"Error al eliminar el donante: '{e}'")
            return False
        finally:
            cursor.close()
            conexion.close()

