import flet as ft
import threading
import time
import os
from controllers.user_controller import LoginController

class LoginView(ft.Row):
    def __init__(self, page: ft.Page):
        super().__init__(alignment=ft.MainAxisAlignment.CENTER)
        self.page = page
        self.controller = LoginController()
        self.cherry = "#660924"
        self.wine = "#630D13"
                # Cargar imágenes desde la carpeta
        self.images = self.load_images_from_folder("./views/assets/side_images")
        self.current_index = 0
        
        self.image_display = ft.Image(
            src=self.images[self.current_index],
            fit=ft.ImageFit.COVER,
            width=self.page.window_width,
            height=self.page.window_height,
        )
        self.image_container = self.create_image_container()
        self.user_field, self.pass_field = self.create_login_fields()
        self.login_button, self.logout_button = self.create_buttons()
        self.dlg_modal = self.create_dialog()
        self.setup_auto_rotate_images()

        # Agregar los controles a la columna
        self.controls.append(self.image_container)
        self.controls.append(self.create_login_container())

    def load_images_from_folder(self, folder):
        images = []
        folder = os.path.abspath(folder)
        for filename in os.listdir(folder):
            if filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):  # Filtrar por extensiones de imagen
                img_path = os.path.join(folder, filename)
                images.append(img_path)  # Agregar la ruta de la imagen
        return images

    def create_image_container(self):
        return ft.Container(
            content=self.image_display,
            width=self.page.window_width,
            height=self.page.window_height,
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

    def create_login_fields(self):
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

        return user_field, pass_field

    def create_buttons(self):
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
            on_click=self.login,
        )

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
            on_click=lambda e: self.page.open(self.dlg_modal),
        )

        return login_button, logout_button

    def create_dialog(self):
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("¿Estás Seguro?"),
            content=ft.Text("¿Deseas Salir de la Aplicación?"),
            actions=[
                ft.TextButton("Sí", on_click=self.salir_programa),
                ft.TextButton("No", on_click=self.cerrar_dialogo),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        return dlg_modal

    def setup_auto_rotate_images(self):
        def next_image():
            self.current_index = (self.current_index + 1) % len(self.images)
            self.image_display.src = self.images[self.current_index]
            self.page.update()

        def auto_rotate_images():
            while True:
                time.sleep(3)
                next_image()

        threading.Thread(target=auto_rotate_images, daemon=True).start()

    def login(self, e):
        usuario = self.user_field.value
        password = self.pass_field.value

        user, message = self.controller.login(usuario, password)  # Captura el usuario y el mensaje

        # Mostrar el mensaje en un SnackBar
        self.page.open(ft.SnackBar(
            content=ft.Text(message),  # Mostrar el mensaje del controlador
            action="OK",
            bgcolor="white"
        ))

        if user:
            print("Inicio de sesión exitoso")
        else:
            self.page.open(ft.SnackBar(
                content=ft.Text("Por favor, complete los campos"),
                action="OK",
                bgcolor="white"
            ))

    def salir_programa(self, e):
        self.page.window.close()

    def cerrar_dialogo(self, e):
        self.dlg_modal.open = False
        self.page.update()

    def create_login_container(self):
        return ft.Container(
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
                    ft.Container(self.user_field, padding=ft.padding.only(top=10)),
                    ft.Container(self.pass_field, padding=ft.padding.only(top=10)),
                    ft.Container(self.login_button, padding=ft.padding.only(top=20)),
                    ft.Container(self.logout_button, padding=ft.padding.only(top=10)),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            gradient=ft.LinearGradient(
                colors=[self.cherry, self.wine],
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
            ),
            width=380,
            height=460,
            border_radius=20,
            padding=ft.padding.all(20),
        )