# user_controller.py
from models.db import verificar_usuario

class LoginController:
    def __init__(self):
        pass

    def login(self, usuario, password):
     
        if not usuario or not password:
            return None, "Por favor complete los campos"  

        user = verificar_usuario(usuario, password)
        if user:
            return user, "Inicio de sesión exitoso"  
        else:
            return None, "Usuario o contraseña incorrectos" 