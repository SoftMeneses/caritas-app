

import flet as ft

'''
def main(page: ft.Page):
    page.title = "AlertDialog examples"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    dlg = ft.AlertDialog(
        title=ft.Text("Hi, this is a non-modal dialog!"),
        on_dismiss=lambda e: page.add(ft.Text("Non-modal dialog dismissed")),
    )

    def handle_close(e):
        page.close(dlg_modal)
        page.add(ft.Text(f"Modal dialog closed with action: {e.control.text}"))

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please confirm"),
        content=ft.Text("Do you really want to delete all those files?"),
        actions=[
            ft.TextButton("Yes", on_click=handle_close),
            ft.TextButton("No", on_click=handle_close),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: page.add(
            ft.Text("Modal dialog dismissed"),
        ),
    )

    page.add(
        ft.ElevatedButton("Open dialog", on_click=lambda e: page.open(dlg)),
        ft.ElevatedButton("Open modal dialog", on_click=lambda e: page.open(dlg_modal)),
    )


ft.app(main)
'''


'''
def main(page: ft.Page):
    page.title = "Pantalla Dividida en Flet"
    page.window_width = 800
    page.window_height = 600
    page.window_resizable = False  # Evita redimensionar la ventana
    

    # Sección izquierda: Imagen de fondo
    left_section = ft.Container(
        content=ft.Image(src="image/Banner_web_1.jpg", fit=ft.ImageFit.CONTAIN),  # Usa una imagen de fondo
        alignment = ft.alignment.center,
        width=800,
        height=600
    )
    

    # Sección derecha: Formulario de inicio de sesión
    right_section = ft.Container(
        content=ft.Column(
            [
                ft.Text("Inicio de Sesión", size=20, weight=ft.FontWeight.BOLD),
                ft.TextField(label="Usuario", width=250),
                ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=250),
                ft.Row(
                    [
                        ft.ElevatedButton("Ingresar", style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE)),
                        ft.ElevatedButton("Salir", on_click=lambda e: page.window.close(), style=ft.ButtonStyle(bgcolor=ft.Colors.RED)),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        padding=20,
        width=300
    )

    
    # Layout principal: Divide en dos columnas
    page.add(
        ft.Row(
            [left_section, right_section],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

ft.app(target=main)
'''





'''
import flet as ft

def main(page: ft.Page):
    page.title = "Pantalla Dividida en Flet"
    page.window_width = 600
    page.window_height = 400
    page.window_resizable = False  # Evita redimensionar la ventana
    
    # Crear el cuadro de diálogo de confirmación
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("¿Seguro que desea salir del programa?"),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: close_dialog()),
            ft.TextButton("Salir", on_click=lambda e: page.window.close()),
        ]
    )

    # Función para cerrar el diálogo
    def close_dialog():
        dialog.open = False
        page.update()

    # Función que abre la ventana de confirmación
    def confirmar_salida(e):
        dialog.open = True
        page.update()

    # Sección derecha: Formulario de inicio de sesión
    right_section = ft.Container(
        content=ft.Column(
            [
                ft.Text("Inicio de Sesión", size=20, weight=ft.FontWeight.BOLD),
                ft.TextField(label="Usuario", width=250),
                ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=250),
                ft.Row(
                    [
                        ft.ElevatedButton("Ingresar", style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE)),
                        ft.ElevatedButton("Salir", on_click=confirmar_salida, style=ft.ButtonStyle(bgcolor=ft.Colors.RED)),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        padding=20,
        width=300
    )

    # Sección izquierda: Imagen de fondo
    left_section = ft.Container(
        content=ft.Image(src="/mnt/data/Banner_web_1.jpg", fit=ft.ImageFit.COVER),  # Ruta corregida
        width=300,
        height=400
    )

    # Agregar el diálogo a la página
    page.dialog = dialog

    # Layout principal: Divide en dos columnas
    page.add(
        ft.Row(
            [left_section, right_section],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

ft.app(target=main)

'''


import flet as ft

def main(page: ft.Page):
    page.title = "Pantalla Dividida en Flet"
    page.window_width = 800
    page.window_height = 600
    page.window_resizable = False  # Evita redimensionar la ventana

    # Función para mostrar el cuadro de diálogo de confirmación
    def mostrar_confirmacion(e):
        def cerrar_dialogo(_):
            page.dialog.open = False
            page.update()

        def salir_programa(_):
            page.window.close()

        page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmación"),
            content=ft.Text("¿Seguro que deseas salir?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_dialogo),
                ft.TextButton("Salir", on_click=salir_programa),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog.open = True
        page.update()

    # Sección izquierda: Imagen de fondo con transparencia y bordes
    left_section = ft.Container(
        content=ft.Image(src="image/Banner_web_1.jpg", fit=ft.ImageFit.COVER),
        width=page.window_width // 2,
        height=page.window_height,
        border_radius=ft.border_radius.all(20),
        opacity=0.8
    )

    # Sección derecha: Formulario de inicio de sesión centrado
    right_section = ft.Container(
        content=ft.Column(
            [
                ft.Text("Inicio de Sesión", size=20, weight=ft.FontWeight.BOLD),
                ft.TextField(label="Usuario", width=250),
                ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=250),
                ft.Row(
                    [
                        ft.ElevatedButton("Ingresar", style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE)),
                        ft.ElevatedButton("Salir", on_click=mostrar_confirmacion(), style=ft.ButtonStyle(bgcolor=ft.Colors.RED)),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        width=page.window_width // 2,
        height=page.window_height,
        alignment=ft.alignment.center,
        padding=20
    )

    # Layout principal: Divide en dos columnas
    page.add(
        ft.Row(
            [left_section, right_section],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

ft.app(target=main)

