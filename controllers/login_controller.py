from models.login_model import Usuario

class LoginController:
    def __init__(self):
        pass

    def login(self, usuario, password):
     
        if not usuario or not password:
            return None, "Por favor complete los campos"  

        user = Usuario.verificar_usuario(usuario, password)
        if user:
            return user, "Inicio de sesión exitoso"  
        else:
            return None, "Usuario o contraseña incorrectos" 

    def autenticar(self, usuario, password):
        return Usuario.autenticar(usuario, password)