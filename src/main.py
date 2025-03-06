import flet as ft

def main(page: ft.Page):
    page.title = "Cáritas San Cristóbal - Inicio de Sesión"
    page.window_width = 500
    page.window_height = 400
    page.vertical_alignment = ft.MainAxisAlignment.CENTER 
    page.window_icon = "/src/assets/logo_caritas.ico" #TODO revisar la integración del icono en la ventana de windows

    
    def login(e):
        usuario = user_field.value
        password = pass_field.value
        if usuario and password:
            page.dialog = ft.AlertDialog(title=ft.Text("Inicio de sesión exitoso"))
            page.dialog.open = True
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, complete los campos"))
            page.snack_bar.open = True
            page.update()
    
    user_field = ft.TextField(label="Usuario", width=300)
    pass_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    login_button = ft.ElevatedButton("Iniciar", on_click=login, bgcolor=ft.Colors.BLUE)
    exit_button = ft.ElevatedButton("Salir", on_click=lambda e: page.window_destroy(), bgcolor=ft.Colors.RED)
    
    page.add(
        ft.Column(
            [
                ft.Text("Cáritas San Cristóbal", size=24, weight=ft.FontWeight.BOLD),
                user_field,
                pass_field,
                ft.Row([login_button, exit_button], alignment=ft.MainAxisAlignment.CENTER)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)