import flet as ft
import threading
import time

def main(page: ft.Page):
    # Configuración de la página
    page.title = "Cáritas San Cristóbal - Inicio de Sesión"
    page.window_width = 1000
    page.window_height = 600
    page.padding = 0
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # Paleta de colores los 3 de abajo no estan siendo utilizados
    cherry = "#660924"          
    wine = "#630D13"            
    nectarine = "#941737"       
    peachy = "#CC3E5E"          
    red_chocolate = "#38050F"

    # Lista de imágenes para el carrusel recuerda cambiar la ruta 
    images = [
        r"C:\Users\Guill\Desktop\caritas-app-main\src\assets\side_1.jpeg",
        r"C:\Users\Guill\Desktop\caritas-app-main\src\assets\side_2.jpeg",
        r"C:\Users\Guill\Desktop\caritas-app-main\src\assets\side_3.jpeg",
        r"C:\Users\Guill\Desktop\caritas-app-main\src\assets\side_4.jpeg",
        r"C:\Users\Guill\Desktop\caritas-app-main\src\assets\side_5.jpeg",
        r"C:\Users\Guill\Desktop\caritas-app-main\src\assets\side_6.jpeg",
        r"C:\Users\Guill\Desktop\caritas-app-main\src\assets\side_7.jpeg",
        r"C:\Users\Guill\Desktop\caritas-app-main\src\assets\side_8.jpeg",
    ]

    # Índice de la imagen actual
    current_index = 0

    # Contenedor para mostrar la imagen actual del carrusel
    carousel_container = ft.Container(
        content=ft.Image(src=images[current_index], width=400, height=300, fit=ft.ImageFit.CONTAIN),
        alignment=ft.alignment.center_left,
        padding=ft.padding.only(left=50),
        bgcolor=ft.colors.TRANSPARENT,
        animate_opacity=ft.Animation(300, "easeInOut"),  # Animación de opacidad
    )

    # Función para cambiar a la siguiente imagen con animación
    def next_image(e=None):
        nonlocal current_index
        current_index = (current_index + 1) % len(images)
        
        # Primero, desvanecer la imagen actual
        carousel_container.opacity = 0
        page.update()

        # Cambiar la imagen y luego hacerla aparecer
        time.sleep(0.3)  
        carousel_container.content.src = images[current_index]
        carousel_container.opacity = 1
        page.update()

    # Función para cambiar automáticamente las imágenes
    def auto_rotate_images():
        while True:
            time.sleep(3)  # Cambiar de imagen cada 3 segundos
            next_image()

    # Iniciar el temporizador para el movimiento automático
    threading.Thread(target=auto_rotate_images, daemon=True).start()

    # Diseño del carrusel 
    carousel = ft.Row(
        controls=[
            carousel_container,  # Contenedor de la imagen actual
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Campos de texto para el formulario de inicio de sesión
    user_field = ft.TextField(
        width=280,
        height=40,
        hint_text="Usuario",
        border="underline",
        color="black",
        prefix_icon=ft.icons.PERSON,
    )

    pass_field = ft.TextField(
        width=280,
        height=40,
        hint_text="Contraseña",
        border="underline",
        color="black",
        prefix_icon=ft.icons.LOCK,
        password=True,
        can_reveal_password=True,
    )

    # Función para manejar el inicio de sesión
    def login(e):
        usuario = user_field.value
        password = pass_field.value
        if usuario and password:
  
            pass  
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, complete los campos"))
            page.snack_bar.open = True
        page.update()

    # Función para confirmar la salida de la aplicación
    def confirm_exit(e):
        def close_dialog(e):
            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("¿Estás seguro?"),
            content=ft.Text("¿Quieres salir de la aplicación?"),
            actions=[
                ft.TextButton("Sí", on_click=lambda _: page.window_close()),
                ft.TextButton("No", on_click=close_dialog),
            ],
        )
        page.dialog.open = True
        page.update()

    # Botón de inicio de sesión 
    login_button = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(ft.icons.LOGIN, color="white"),
                ft.Text("INICIAR SESIÓN", color="white", weight="w500"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        width=280,
        bgcolor="blue",
        on_click=login,
    )

    # Botón para cerrar sesión
    logout_button = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(ft.icons.LOGOUT, color="white"),
                ft.Text("SALIR DEL PROGRAMA", color="white", weight="w500"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        width=280,
        bgcolor="red",
        on_click=confirm_exit,
    )

    # Botón para iniciar sesión como invitado
    guest_login_button = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(ft.icons.PERSON, color="black"),
                ft.Text("INICIAR COMO INVITADO", color="black", weight="w500"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        width=280,
        bgcolor="white",
        on_click=lambda e: page.dialog,
    )

    # Contenedor para el formulario de inicio de sesión
    login_container = ft.Container(
        ft.Column(
            controls=[
                ft.Container(ft.Image(src="https://via.placeholder.com/60", width=60), padding=ft.padding.only(top=20, bottom=20)),
                ft.Text("Iniciar Sesión", size=30, weight="w900", text_align="center", color="white"),
                ft.Container(user_field, padding=ft.padding.only(top=10)),
                ft.Container(pass_field, padding=ft.padding.only(top=10)),
                ft.Container(login_button, padding=ft.padding.only(top=20)),
                ft.Container(logout_button, padding=ft.padding.only(top=10)),
                ft.Container(guest_login_button, padding=ft.padding.only(top=10)),
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
            carousel,
            ft.Container(width=50),
            login_container,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Agregar el diseño principal a la página
    page.add(main_layout)

# Iniciar la aplicación
ft.app(target=main)