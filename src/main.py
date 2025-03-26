import flet as ft
import threading
import time

def main(page: ft.Page):
    # Configuración de la página
    page.title = "Cáritas San Cristóbal - Inicio de Sesión"
    page.window_width = 800
    page.window_height = 600
    page.window_resizable = False  
    page.window.icon = "image/logo_caritas_2.ico" # TODO revisar integracion del icono
    page.bgcolor = "#dfdcbd"  
    page.padding = 0
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # Paleta de colores
    cherry = "#660924"          
    wine = "#630D13"            

    # Lista de imágenes para el carrusel
    images = [
        r"src\assets\side_1_rebuild.jpeg",
        r"src\assets\side_2_rebuild.jpeg",
        r"src\assets\side_3_rebuild.jpeg",
        r"src\assets\side_4_rebuild.jpeg",
        r"src\assets\side_5_rebuild.jpeg",
        r"src\assets\side_6_rebuild.jpeg",
        r"src\assets\side_7_rebuild.jpeg",
        r"src\assets\side_8_rebuild.jpeg",
    ]

    current_index = 0

    # Imagen de fondo dinámica
    image_display = ft.Image(
        src=images[current_index],
        fit=ft.ImageFit.COVER,
        width=page.window_width,
        height=page.window_height,
    )

    image_container = ft.Container(
        content=image_display,
        width=page.window_width,
        height=page.window_height,
        border_radius=20,
        shadow=ft.BoxShadow(
            spread_radius=15,
            blur_radius=35,
            color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
            offset=ft.Offset(0, 5),
        ),
        opacity=1.0,  
        animate_opacity=ft.Animation(500, "easeInOut"),  
    )

    def next_image():
        nonlocal current_index
        current_index = (current_index + 1) % len(images)

        image_container.opacity = 0
        page.update()

        time.sleep(0.5)  # pausa para la animación de fade

        image_display.src = images[current_index]
        image_container.opacity = 1
        page.update()

    def auto_rotate_images():
        while True:
            time.sleep(3)
            next_image()

    threading.Thread(target=auto_rotate_images, daemon=True).start()

    # Campos de texto para el formulario de inicio de sesión
    user_field = ft.TextField(
        width=280,
        height=40,
        hint_text="Usuario",
        border="underline",
        color="white",
        prefix_icon=ft.Icons.PERSON,
    )

    pass_field = ft.TextField(
        width=280,
        height=40,
        hint_text="Contraseña",
        border="underline",
        color="white",
        prefix_icon=ft.Icons.LOCK,
        password=True,
        can_reveal_password=True,
    )

    # Función para manejar el inicio de sesión
    def login(e):
        usuario = user_field.value
        password = pass_field.value

        if usuario and password:
            print("Inicio de sesión exitoso")  
        else:
            page.open(ft.SnackBar(
                content=ft.Text("Por favor, complete los campos"),
                action="OK",
                bgcolor="white"
            ))

    # Función para cerrar la aplicación
    def salir_programa(e):
        page.window.close()

    # Función para cerrar el cuadro de diálogo
    def cerrar_dialogo(e):
        dlg_modal.open = False
        page.update()

    # cuadro de diálogo modal
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("¿Estás Seguro?"),
        content=ft.Text("¿Deseas Salir de la Aplicación?"),
        actions=[
            ft.TextButton("Sí", on_click=salir_programa),
            ft.TextButton("No", on_click=cerrar_dialogo),
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    # Botón de inicio de sesión 
    login_button = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.LOGIN, color="white"),
                ft.Text("INICIAR SESIÓN", color="white", weight="w500"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        width=280,
        bgcolor="blue",
        on_click=login,
    )

    # Botón para salir de la aplicación
    logout_button = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.LOGOUT, color="white"),
                ft.Text("SALIR DEL PROGRAMA", color="white", weight="w500"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        width=280,
        bgcolor="red",
        on_click=lambda e: page.open(dlg_modal),
    )

    # Contenedor para el formulario de inicio de sesión
    login_container = ft.Container(
        ft.Column(
            controls=[
                ft.Container(ft.Image(src="https://via.placeholder.com/60", width=60), padding=ft.padding.only(top=-20, bottom=20)),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Image(src=r"src\assets\white_logo.png", width=180, height=60),  
                            ft.Text("¡Bienvenido!", size=30, weight="w900", text_align="center", color="white"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=ft.padding.only(bottom=20),  
                ),
                ft.Container(user_field, padding=ft.padding.only(top=10)),
                ft.Container(pass_field, padding=ft.padding.only(top=10)),
                ft.Container(login_button, padding=ft.padding.only(top=20)),
                ft.Container(logout_button, padding=ft.padding.only(top=10)),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        gradient=ft.LinearGradient(
            colors=[cherry, wine],
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
        ),
        width=380,
        height=460,
        border_radius=20,
        padding=ft.padding.all(20),
    )

    # Diseño principal 
    main_layout = ft.Row(
        [
            image_container,  
            ft.Container(width=50),
            login_container,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    page.add(main_layout)

# Iniciar la aplicación
ft.app(target=main)
