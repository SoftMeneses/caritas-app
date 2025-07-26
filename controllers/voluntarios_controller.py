from models.voluntarios_model import Voluntario
    
class VoluntariosController:
    def __init__(self):
        self.voluntarios = []

    def cargar_voluntarios(self):
        self.voluntarios = Voluntario.obtener_voluntarios()
        return self.voluntarios
    
    def agregar_voluntario(self, voluntario, disponibilidad):
        if Voluntario.insertar_voluntario(voluntario, disponibilidad):
            self.cargar_voluntarios()  
            return True
        return False   
    
    def editar_voluntario(self, voluntario_id, voluntario, disponibilidad):
        if Voluntario.actualizar_voluntario(voluntario_id, voluntario, disponibilidad):
            self.cargar_voluntarios()  
            return True
        return False   

    def eliminar_voluntario(self, voluntario_id):
        if Voluntario.eliminar_voluntario(voluntario_id):
            self.cargar_voluntarios()  
            return True
        return False