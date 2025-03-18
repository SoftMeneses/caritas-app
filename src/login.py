import flet as ft

'''
def main(page: ft.Page):
    page.title = "background img test"
    page.bgcolor = ft.Colors.GREY

    img = ft.Container(
        content=ft.Image(
                src="image/icon.png",
                width=200,
                height=200,
            ),
        alignment=ft.alignment.center,

    )

        
    page.add(img)

'''


def main(page: ft.Page):
    page.title = "Pantalla Dividida en Flet"
    page.window_width = 800
    page.window_height = 600
    page.bgcolor = ft.Colors.SECONDARY_CONTAINER
    page.window_resizable = False  # Evita redimensionar la ventana

    # Función para cerrar la aplicación
    def salir_programa(e):
        page.window.close()

    # Función para cerrar el cuadro de diálogo
    def cerrar_dialogo(e):
        dlg_modal.open = False
        page.update()

    # Crear el cuadro de diálogo modal
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmación"),
        content=ft.Text("¿Seguro que deseas salir?"),
        actions=[
            ft.TextButton("Sí", on_click=salir_programa),
            ft.TextButton("No", on_click=cerrar_dialogo),
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )


    # Sección izquierda: Imagen con bordes y transparencia
    left_section = ft.Container(
        content=ft.Image(src="image/logo-caritas.png", fit=ft.ImageFit.CONTAIN),
        width=page.window_width // 2,
        height=page.window_height,
        border_radius=ft.border_radius.all(20),
        opacity=0.8
    )

    # Sección derecha: Formulario de inicio de sesión centrado
    right_section = ft.Container(
        content = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Inicio de Sesión", size=30, weight=ft.FontWeight.BOLD),
                    ft.TextField(label="Usuario", width=250),
                    ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=250),
                    ft.Row(
                        [
                            ft.ElevatedButton("Ingresar", style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE)),
                            ft.ElevatedButton("Salir", on_click = lambda e: page.open(dlg_modal), style=ft.ButtonStyle(bgcolor=ft.Colors.RED)),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            padding=30,
            border=ft.border.all(2, ft.Colors.WHITE),  # Borde delgado y blanco
            border_radius=ft.border_radius.all(20),  # Bordes redondeados
            bgcolor=ft.Colors.TERTIARY_CONTAINER,  # Fondo blanco semi-transparente
            alignment=ft.alignment.center
        ),
        width=page.window_width // 2,
        height=page.window_height,
        alignment=ft.alignment.center,
        padding=20
    )

    # Agregando ambas secciones a la página
    page.add(
        ft.Row(
            [left_section, right_section],
            alignment=ft.MainAxisAlignment.CENTER
        )
        
    )

ft.app(target=main)


'''
    texto_titulo = ft.Container(
        content = ft.Text(value= "Texto en la pantalla",
                          size= 60,
                          weight=ft.FontWeight.BOLD,
                          color = ft.Colors.BLACK),
        alignment= ft.alignment.center,
    )
'''




