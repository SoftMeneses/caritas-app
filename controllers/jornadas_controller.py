from models.jornadas_model import Jornadas
from models.donaciones_model import Donaciones

class JornadasController:
    def __init__(self):
        self.jornadas = []

    def cargar_jornadas(self):
        self.jornadas = Jornadas.obtener_jornadas()
        return self.jornadas

    def agregar_jornada(self, jornada):
        if Jornadas.insertar_jornada(jornada):
            self.cargar_jornadas()
            return True
        return False

    def editar_jornada(self, jornada_id, jornada):
        if Jornadas.actualizar_jornada(jornada_id, jornada):
            self.cargar_jornadas()
            return True
        return False

    def eliminar_jornada(self, jornada_id):
        # 1. Obtener detalles de la jornada antes de eliminar
        detalles = self.obtener_detalles_jornada(jornada_id)
        for detalle in detalles:
            id_detalle = detalle.get("ID_DETALLE_DONACION") or detalle.get("id_detalle")
            cantidad_utilizada = float(detalle.get("CANTIDAD_UTILIZADA") or 0)
            Donaciones.restar_utilizado_detalle(id_detalle, cantidad_utilizada)

        # 2. Eliminar detalles de la jornada
        self.eliminar_detalles_jornada(jornada_id)

        # 3. Eliminar voluntarios asociados a la jornada
        Jornadas.limpiar_voluntarios_jornada(jornada_id)

        # 4. Eliminar la jornada principal
        return Jornadas.eliminar_jornada(jornada_id)

    def guardar_voluntarios(self, voluntario_id, jornada_id):
        if Jornadas.guardar_voluntarios(voluntario_id, jornada_id):
            self.cargar_jornadas()
            return True
        return False

    def limpiar_voluntarios_jornada(self, jornada_id):
        if Jornadas.limpiar_voluntarios_jornada(jornada_id):
            self.cargar_jornadas()
            return True
        return False

    def obtener_voluntarios_por_jornada(self, jornada_id):
        return Jornadas.obtener_voluntarios_por_jornada(jornada_id)

    def obtener_recursos_disponibles(self):
        detalles = Donaciones.obtener_detalles_donaciones()
        recursos = []
        for d in detalles:
            cantidad = float(d.get("CANTIDAD", 0) or d.get("MONTO", 0) or 0)
            utilizado = float(d.get("UTILIZADO", 0) or 0)
            disponible = cantidad - utilizado
            if disponible > 0:
                recursos.append({
                    "tipo": d.get("TIPO", ""),
                    "descripcion": d.get("DESCRIPCION", ""),
                    "cantidad_disponible": disponible,
                    "id_detalle": d.get("ID_DETALLE", d.get("DETALLE_ID", None))
                })
        return recursos

    def insertar_jornada_detalle(self, jornada_id, recurso_utilizado, cantidad_utilizada, id_detalle=None):
        return Jornadas.insertar_jornada_detalle(jornada_id, recurso_utilizado, cantidad_utilizada, id_detalle)

    def actualizar_utilizado_donacion_detalle(self, id_detalle, cantidad_utilizada):
        return Donaciones.sumar_utilizado_detalle(id_detalle, cantidad_utilizada)

    def obtener_detalles_jornada(self, jornada_id):
        return Jornadas.obtener_detalles_jornada(jornada_id)

    def eliminar_detalles_jornada(self, jornada_id):
        return Jornadas.eliminar_detalles_jornada(jornada_id)

    def completar_jornada(self, jornada_id, recursos_utilizados, comentarios, voluntarios_participacion, voluntarios_horas):
        # 1. Obtener detalles actuales antes de eliminar
        detalles_anteriores = self.obtener_detalles_jornada(jornada_id)
        for detalle in detalles_anteriores:
            id_detalle = detalle.get("ID_DETALLE_DONACION") or detalle.get("id_detalle")
            cantidad_utilizada = float(detalle.get("CANTIDAD_UTILIZADA") or 0)
            Donaciones.restar_utilizado_detalle(id_detalle, cantidad_utilizada)
        # 2. Elimina detalles previos
        self.eliminar_detalles_jornada(jornada_id)

        # 3. Inserta nuevos detalles y suma lo utilizado
        for recurso in recursos_utilizados:
            self.insertar_jornada_detalle(
                jornada_id,
                recurso["descripcion"],
                recurso["cantidad_utilizada"],
                recurso.get("id_detalle")
            )
            self.actualizar_utilizado_donacion_detalle(recurso.get("id_detalle"), recurso["cantidad_utilizada"])

        # 4. Actualiza la participación y horas de los voluntarios
        Jornadas.actualizar_participacion_voluntario(jornada_id, voluntarios_participacion, voluntarios_horas)
        # 5. Marca la jornada como completada
    
    def marcar_jornada_completada(self, jornada_id, comentarios):
        return Jornadas.marcar_jornada_completada(jornada_id, comentarios)
        #Jornadas.marcar_jornada_completada(jornada_id, comentarios)
        #return True

    def marcar_jornada_no_completada(self, jornada_id):
        return Jornadas.marcar_jornada_no_completada(jornada_id)