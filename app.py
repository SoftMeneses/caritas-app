import flet as ft
from views.login_view import LoginView

def main(page: ft.Page):
    # Configuración de la página
    page.title = "Cáritas San Cristóbal - Inicio de Sesión"
    page.window_width = 800
    page.window_height = 600
    page.window_resizable = False  
    page.window.icon = "./views/assets/image/logo_caritas_2.ico" # TODO revisar integracion del icono
    page.bgcolor = "#dfdcbd"  
    page.padding = 0
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # Cargar la vista de inicio de sesión
    login_view = LoginView(page)
    page.add(login_view)

# iniciar la aplicación
ft.app(target=main)