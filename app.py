import flet as ft
from views.login_view import LoginView
from views.donantes_view import main as donantes_view
from views.jornadas_view import main as jornadas_view
from views.voluntarios_view import main as voluntarios_view
from views.donaciones_view import main as donaciones_view
from views.configuracion_view import main as configuracion_view
from views.home_view import main as home_view 

def main(page: ft.Page):
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            on_surface="black",  # Color de texto en menús y listas
            surface="white"
        )
    )
    page.title = "Cáritas San Cristóbal - Inicio de Sesión"
    page.window_width = 800
    page.window_height = 600
    page.window_resizable = False  
    page.window.icon = "./views/assets/image/logo_caritas_2.ico" 
    page.bgcolor = "#dfdcbd"  
    page.padding = 0
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    def navegar(selected_index):
        page.controls.clear() 

        from views.navbar import NavBar
        navbar = NavBar(page, navegar)
        page.controls.append(navbar.view)

        if selected_index == 0:
            page.clean() 
            home_view(page, navegar)

        elif selected_index == 1:
            page.clean() 
            donantes_view(page, navegar)
            
        elif selected_index == 2:
            page.clean() 
            donaciones_view(page, navegar)

        elif selected_index == 3:
            page.clean() 
            voluntarios_view(page, navegar)

        elif selected_index == 4:
            page.clean() 
            jornadas_view(page, navegar)

        elif selected_index == 5:
            page.clean() 
            configuracion_view(page, navegar) 
            
        
        page.update() 


    login_view = LoginView(page, navegar)
    page.add(login_view)

ft.app(target=main)