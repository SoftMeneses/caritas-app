from models.db import Database
from mysql.connector import Error

class Jornadas:
    @staticmethod
    def obtener_jornadas():
        conexion = Database.crear_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute('SELECT ID_JORNADA, FECHA, DESCRIPCION, UBICACION, IF(COMPLETADA = 0,"POR COMPLETAR","COMPLETADA") AS COMPLETADA FROM JORNADAS')
            jornada = cursor.fetchall() 
        except Error as e:
            print(f"Error al ejecutar la consulta: '{e}'")
            jornada = None
        finally:
            cursor.close()
            conexion.close()
        return jornada

    @staticmethod
    def insertar_jornada(jornada):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute('SELECT IFNULL(MAX(ID_JORNADA), 0) + 1 as next_id FROM JORNADAS')
            next_id = cursor.fetchone()[0]
            cursor.execute('INSERT INTO JORNADAS (ID_JORNADA, FECHA, DESCRIPCION, UBICACION) VALUES (%s, %s, %s, %s)',
                        (next_id, jornada['fecha'], jornada['descripcion'], jornada['ubicacion']))
            conexion.commit() 
            return True
        except Error as e:
            print(f"Error al insertar la jornada: '{e}'")
            return False
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def actualizar_jornada(jornada_id, jornada):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute('UPDATE JORNADAS SET FECHA=%s, DESCRIPCION=%s, UBICACION=%s WHERE ID_JORNADA=%s',
                        (jornada['fecha'], jornada['descripcion'], jornada['ubicacion'], jornada_id))
            conexion.commit()  
            return True
        except Error as e:
            print(f"Error al actualizar la jornada: '{e}'")
            return False
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def eliminar_jornada(jornada_id):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute('DELETE FROM JORNADAS WHERE ID_JORNADA=%s', (jornada_id,))
            conexion.commit()
            return True
        except Error as e:
            print(f"Error al eliminar la jornada: '{e}'")
            return False
        finally:
            cursor.close()
            conexion.close()
 
    @staticmethod
    def guardar_voluntarios(voluntario_id, jornada_id):     
        conexion = Database.crear_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute('INSERT INTO JORNADAS_VOLUNTARIOS (ID_JORNADA, ID_VOLUNTARIO) VALUES (%s, %s)',
                        (jornada_id, voluntario_id))
            conexion.commit() 
            return True
        except Error as e:
            print(f"Error al guardar el voluntario en la jornada: '{e}'")
            return False
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def limpiar_voluntarios_jornada(jornada_id):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute('DELETE FROM JORNADAS_VOLUNTARIOS WHERE ID_JORNADA=%s', (jornada_id,))
            conexion.commit()
            return True
        except Error as e:
            print(f"Error al limpiar voluntarios de jornada: '{e}'")
            return False
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def obtener_voluntarios_por_jornada(jornada_id):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute('''
                SELECT v.ID_VOLUNTARIO, v.NOMBRE, jv.PARTICIPACION, jv.HORAS_VOLUNTARIO
                FROM VOLUNTARIOS v
                JOIN JORNADAS_VOLUNTARIOS jv ON v.ID_VOLUNTARIO = jv.ID_VOLUNTARIO
                WHERE jv.ID_JORNADA = %s
            ''', (jornada_id,))
            return cursor.fetchall()
        except Error as e:
            print(f"Error al obtener voluntarios por jornada: '{e}'")
            return []
        finally:
            cursor.close()
            conexion.close()



    @staticmethod
    def marcar_jornada_completada(jornada_id, observacion):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                'UPDATE JORNADAS SET COMPLETADA=1, OBSERVACION=%s WHERE ID_JORNADA=%s',
                (observacion, jornada_id)
            )
            conexion.commit()
            return True
        except Error as e:
            print(f"Error al marcar la jornada como completada: '{e}'")
            return False
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def marcar_jornada_no_completada(jornada_id):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                'UPDATE JORNADAS SET COMPLETADA=0 WHERE ID_JORNADA=%s',
                (jornada_id,)
            )
            conexion.commit()
            return True
        except Error as e:
            print(f"Error al marcar la jornada como no completada: '{e}'")
            return False
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def actualizar_participacion_voluntario(jornada_id, voluntarios_participacion, voluntarios_horas):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor()
        try:
            # Primero, poner PARTICIPACION=0 y HORAS_VOLUNTARIO=NULL para todos los voluntarios de la jornada
            cursor.execute(
                'UPDATE JORNADAS_VOLUNTARIOS SET PARTICIPACION=0, HORAS_VOLUNTARIO="" WHERE ID_JORNADA=%s',
                (jornada_id,)
            )
            # Luego, actualizar los que participaron y sus horas
            for voluntario_id in voluntarios_participacion:
                horas = voluntarios_horas.get(voluntario_id, 0)
                cursor.execute(
                    'UPDATE JORNADAS_VOLUNTARIOS SET PARTICIPACION=1, HORAS_VOLUNTARIO=%s WHERE ID_JORNADA=%s AND ID_VOLUNTARIO=%s',
                    (horas, jornada_id, voluntario_id)
                )
            conexion.commit()
            return True
        except Error as e:
            print(f"Error al actualizar la participación del voluntario: '{e}'")
            return False
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def insertar_jornada_detalle(jornada_id, recurso_utilizado, cantidad_utilizada, id_detalle_donacion=None):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                'INSERT INTO jornada_detalle (JORNADA_ID, RECURSO_UTILIZADO, CANTIDAD_UTILIZADA, ID_DETALLE_DONACION) VALUES (%s, %s, %s, %s)',
                (jornada_id, recurso_utilizado, cantidad_utilizada, id_detalle_donacion)
            )
            conexion.commit()
            return True
        except Error as e:
            print(f"Error al insertar detalle de jornada: '{e}'")
            return False
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def obtener_detalles_jornada(jornada_id):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute('''
                SELECT 
                    jd.DETALLE_JORNADA_ID, 
                    jd.JORNADA_ID, 
                    J.OBSERVACION,
                    jd.RECURSO_UTILIZADO, 
                    jd.CANTIDAD_UTILIZADA, 
                    jd.ID_DETALLE_DONACION,
                    dd.TIPO,
                    dd.DESCRIPCION,
                    dd.CANTIDAD
                    - IFNULL((
                        SELECT SUM(jd2.CANTIDAD_UTILIZADA)
                        FROM jornada_detalle jd2
                        WHERE jd2.ID_DETALLE_DONACION = dd.DETALLE_ID
                    ), 0) AS CANTIDAD_DISPONIBLE
                    
                    FROM JORNADAS j
                    
                LEFT JOIN jornada_detalle jd ON jd.jornada_id = j.id_jornada
                LEFT JOIN donacion_detalle dd ON jd.ID_DETALLE_DONACION = dd.DETALLE_ID
		
                WHERE j.ID_JORNADA = %s
            ''', (jornada_id,))
            return cursor.fetchall()
        except Error as e:
            print(f"Error al obtener detalles de jornada: '{e}'")
            return []
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def eliminar_detalles_jornada(jornada_id):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute('DELETE FROM jornada_detalle WHERE JORNADA_ID=%s', (jornada_id,))
            conexion.commit()
            return True
        except Error as e:
            print(f"Error al eliminar detalles de jornada: '{e}'")
            return False
        finally:
            cursor.close()
            conexion.close()