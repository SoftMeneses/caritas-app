from models.donaciones_model import Donaciones

class DonacionesController:
    def __init__(self):
        self.donaciones = []

    def cargar_donaciones(self):
        self.donaciones = Donaciones.obtener_donaciones()
        return self.donaciones

    def agregar_donacion(self, donacion):
        # donacion: {'donante_id', 'fecha', 'descripcion', 'detalles': [ {...}, {...} ]}
        donacion_id = Donaciones.insertar_donacion_con_detalles(
            {
                'donante_id': donacion['donante_id'],
                'fecha': donacion['fecha'],
                'descripcion': donacion['descripcion']
            },
            [
                {
                    'tipo': detalle.get('TIPO', ''),
                    'descripcion': detalle.get('DESCRIPCION', ''),
                    'cantidad': detalle.get('CANTIDAD', 0),
                    'monto': detalle.get('MONTO', 0),
                    'metodo_pago': detalle.get('METODO_PAGO', ''),
                }
                for detalle in donacion['detalles']
            ]
        )
        return bool(donacion_id)

    def editar_donacion(self, donacion_id, donacion):
        try:
            resultado = Donaciones.actualizar_donacion_con_detalles(
                donacion_id,
                {
                    'donante_id': donacion['donante_id'],
                    'fecha': donacion['fecha'],
                    'descripcion': donacion['descripcion']
                },
                [
                    {
                        'tipo': detalle.get('TIPO', ''),
                        'descripcion': detalle.get('DESCRIPCION', ''),
                        'cantidad': detalle.get('CANTIDAD', 0),
                        'monto': detalle.get('MONTO', 0),
                        'metodo_pago': detalle.get('METODO_PAGO', ''),
                    }
                    for detalle in donacion['detalles']
                ]
            )
            self.cargar_donaciones()
            return resultado
        except Exception as e:
            print(f"Error al editar la donación: {e}")
            return False

    def eliminar_donacion(self, donacion_id):
        if Donaciones.eliminar_donacion(donacion_id):
            self.cargar_donaciones()
            return True
        return False