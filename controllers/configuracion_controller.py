from models.configuracion_model import UsuariosPerfilesModel

class UsuariosPerfilesController:
    # --- PERFILES ---
    def obtener_perfiles(self):
        return UsuariosPerfilesModel.obtener_perfiles()

    def agregar_perfil(self, nombre, permisos):
        return UsuariosPerfilesModel.agregar_perfil(nombre, permisos)

    def eliminar_perfil(self, perfil_id):
        return UsuariosPerfilesModel.eliminar_perfil(perfil_id)
    
    def actualizar_perfil(self, perfil_id, nombre, permisos):
        return UsuariosPerfilesModel.actualizar_perfil(perfil_id, nombre, permisos)

    # --- USUARIOS ---
    def obtener_usuarios(self):
        return UsuariosPerfilesModel.obtener_usuarios()

    def agregar_usuario(self, usuario):
        return UsuariosPerfilesModel.agregar_usuario(usuario)

    def eliminar_usuario(self, usuario_id):
        return UsuariosPerfilesModel.eliminar_usuario(usuario_id)

    def actualizar_usuario(self, usuario_id, datos):
        return UsuariosPerfilesModel.actualizar_usuario(usuario_id, datos)