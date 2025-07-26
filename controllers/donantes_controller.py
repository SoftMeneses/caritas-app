from models.donantes_model import Donante

class DonantesController:
    def __init__(self):
        self.donantes = []

    def cargar_donantes(self):
        self.donantes = Donante.obtener_donantes()
        return self.donantes
    
    def agregar_donante(self, donante):
        if Donante.insertar_donante(donante):
            self.cargar_donantes()  
            return True
        return False   
    
    def editar_donante(self, donante_id, donante):
        if Donante.actualizar_donante(donante_id, donante):
            self.cargar_donantes()  
            return True
        return False   
    

    def eliminar_donante(self, donante_id):
        if Donante.eliminar_donante(donante_id):
            self.cargar_donantes()  
            return True
        return False

