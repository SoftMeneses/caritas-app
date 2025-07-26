from models.db import Database
from mysql.connector import Error
        
class Donaciones:
    @staticmethod
    def obtener_donaciones():
        conexion = Database.crear_conexion()
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute('''
                SELECT d.ID_DONACION, d.DONANTE_ID, dn.NOMBRE, dn.CEDULA, dn.TELEFONO, dn.CORREO, dn.DIRECCION, d.DESCRIPCION AS DESCRI, d.FECHA
                FROM donaciones d
                JOIN donantes dn ON d.DONANTE_ID = dn.ID_DONANTE
            ''')
            donaciones = cursor.fetchall()
            for donacion in donaciones:
                cursor.execute('SELECT * FROM donacion_detalle WHERE DONACION_ID = %s', (donacion['ID_DONACION'],))
                donacion['detalles'] = cursor.fetchall()
            return donaciones
        except Error as e:
            print(f"Error al ejecutar la consulta: '{e}'")
            return None
        finally:
            cursor.close()
            conexion.close()


    @staticmethod
    def insertar_donacion_con_detalles(donacion, detalles):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor()
        try:
            # Obtener el último ID_DONACION y sumarle 1
            cursor.execute('SELECT IFNULL(MAX(ID_DONACION), 0) + 1 as next_id FROM donaciones')
            next_id = cursor.fetchone()[0]
            cursor.execute(
                'INSERT INTO donaciones (ID_DONACION, DONANTE_ID, FECHA, DESCRIPCION) VALUES (%s, %s, %s, %s)',
                (next_id, donacion['donante_id'], donacion['fecha'], donacion['descripcion'])
            )
            conexion.commit()
            donacion_id = next_id

            for detalle in detalles:
                cursor.execute(
                    'INSERT INTO donacion_detalle (DONACION_ID, TIPO, DESCRIPCION, CANTIDAD, MONTO, METODO_PAGO) VALUES (%s, %s, %s, %s, %s, %s)',
                    (
                        donacion_id,
                        detalle.get('tipo', ''),
                        detalle.get('descripcion', ''),
                        detalle.get('cantidad', 0),
                        detalle.get('monto', 0),
                        detalle.get('metodo_pago', '')
                    )
                )
            conexion.commit()
            return donacion_id
        except Error as e:
            print(f"Error al insertar la donacion: '{e}'")
            return None
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def actualizar_donacion_con_detalles(donacion_id, donacion, detalles):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                'UPDATE donaciones SET DONANTE_ID = %s, FECHA = %s, DESCRIPCION = %s WHERE ID_DONACION = %s',
                (donacion['donante_id'], donacion['fecha'], donacion['descripcion'], donacion_id)
            )
            cursor.execute('DELETE FROM donacion_detalle WHERE DONACION_ID = %s', (donacion_id,))
            for detalle in detalles:
                cursor.execute(
                    'INSERT INTO donacion_detalle (DONACION_ID, TIPO, DESCRIPCION, CANTIDAD, MONTO, METODO_PAGO) VALUES (%s, %s, %s, %s, %s, %s)',
                    (
                        donacion_id,
                        detalle.get('tipo', ''),
                        detalle.get('descripcion', ''),
                        detalle.get('cantidad', 0),
                        detalle.get('monto', 0),
                        detalle.get('metodo_pago', '')
                    )
                )
            conexion.commit()
            return True
        except Error as e:
            print(f"Error al actualizar la donacion: '{e}'")
            return False
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def eliminar_detalles_donacion(donacion_id):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute('DELETE FROM donacion_detalle WHERE DONACION_ID = %s', (donacion_id,))
            conexion.commit()
            return True
        except Error as e:
            print(f"Error al eliminar los detalles de la donacion: '{e}'")
            return False
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def eliminar_donacion(donacion_id):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor()
        try:
            
            cursor.execute('DELETE FROM donacion_detalle WHERE DONACION_ID = %s', (donacion_id,))
            cursor.execute('DELETE FROM donaciones WHERE ID_DONACION = %s', (donacion_id,))
            
            conexion.commit()
            return True
        except Error as e:
            print(f"Error al eliminar la donacion: '{e}'")
            return False
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def obtener_detalles_donaciones():
        conexion = Database.crear_conexion()
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute('SELECT * FROM donacion_detalle')
            return cursor.fetchall()
        except Error as e:
            print(f"Error al obtener detalles de donaciones: '{e}'")
            return []
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def sumar_utilizado_detalle(id_detalle, cantidad):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                'UPDATE donacion_detalle SET UTILIZADO = IFNULL(UTILIZADO,0) + %s WHERE DETALLE_ID = %s',
                (cantidad, id_detalle)
            )
            conexion.commit()
            return True
        except Error as e:
            print(f"Error al actualizar UTILIZADO en donacion_detalle: '{e}'")
            return False
        finally:
            cursor.close()
            conexion.close()


    @staticmethod
    def restar_utilizado_detalle(id_detalle, cantidad):
        conexion = Database.crear_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                'UPDATE donacion_detalle SET UTILIZADO = IFNULL(UTILIZADO,0) - %s WHERE DETALLE_ID = %s',
                (cantidad, id_detalle)
            )
            conexion.commit()
            return True
        except Error as e:
            print(f"Error al restar UTILIZADO en donacion_detalle: '{e}'")
            return False
        finally:
            cursor.close()
            conexion.close()