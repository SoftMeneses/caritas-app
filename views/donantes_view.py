import flet as ft
import re
from navbar import NavBar  

def main(page: ft.Page):
    # Configuración de la página
    page.title = "Cáritas San Cristóbal - Donantes"
    page.window_width = 900
    page.window_height = 600
    page.window_resizable = False
    page.bgcolor = "white"
    page.padding = 20

    # Paleta de colores
    cherry = "#660924"
    wine = "#630D13"

    # Instancia de NavBar
    navbar = NavBar(cherry=cherry, wine=wine).view

    # Lista de donantes
    donantes = [
        {"nombre": "Juan Pérez", "email": "juan.perez@example.com", "telefono": "0416-1234567"},
        {"nombre": "María Gómez", "email": "maria.gomez@example.com", "telefono": "0426-9876543"},
        {"nombre": "Carlos López", "email": "carlos.lopez@example.com", "telefono": "0414-5551234"},
    ]

    # Campos y errores
    nombre_field = ft.TextField(label="Nombre", hint_text="Escribe el Nombre aquí", filled=True, prefix_icon=ft.Icons.PERSON_ROUNDED, width=410)
    email_field = ft.TextField(label="Email", hint_text="Escribe el Email aquí", filled=True, prefix_icon=ft.Icons.EMAIL_ROUNDED, width=410)
    telefono_field = ft.TextField(label="Teléfono", hint_text="Escribe el Teléfono aquí", filled=True, prefix_icon=ft.Icons.PHONE_ROUNDED, keyboard_type=ft.KeyboardType.NUMBER)
    prefijo_dropdown = ft.Dropdown(options=[ft.dropdown.Option(p) for p in ["0416", "0426", "0414", "0424", "0412"]], value="0416", width=100, filled=True)

    nombre_error = ft.Text("", color="red", size=12)
    email_error = ft.Text("", color="red", size=12)
    telefono_error = ft.Text("", color="red", size=12)

    def validar_campos():
        errores = False
        if not nombre_field.value.strip():
            nombre_error.value = "⚠️ Ingresa un nombre."
            errores = True
        else:
            nombre_error.value = ""

        if not email_field.value.strip():
            email_error.value = "⚠️ Ingresa un email."
            errores = True
        else:
            email_error.value = ""

        if not telefono_field.value.isdigit() or len(telefono_field.value) != 7:
            telefono_error.value = "⚠️ Ingresa un número de 7 dígitos."
            errores = True
        else:
            telefono_error.value = ""

        page.update()
        return not errores

    def cerrar_dialogo(e=None):
        page.dialog.open = False
        page.update()

    def agregar_donante(e):
        if not validar_campos():
            return

        nuevo_donante = {
            "nombre": nombre_field.value,
            "email": email_field.value,
            "telefono": f"{prefijo_dropdown.value}-{telefono_field.value}",
        }
        donantes.append(nuevo_donante)
        lista_donantes.controls = crear_lista_donantes().controls
        limpiar_campos()
        cerrar_dialogo()

    def guardar_edicion(donante):
        def _guardar(e):
            if not validar_campos():
                return
            donante["nombre"] = nombre_field.value
            donante["email"] = email_field.value
            donante["telefono"] = f"{prefijo_dropdown.value}-{telefono_field.value}"
            lista_donantes.controls = crear_lista_donantes().controls
            limpiar_campos()
            cerrar_dialogo()
        return _guardar

    def editar_donante(donante):
        nombre_field.value = donante["nombre"]
        email_field.value = donante["email"]
        telefono_field.value = donante["telefono"].split("-")[1]
        prefijo_dropdown.value = donante["telefono"].split("-")[0]

        page.dialog.title = ft.Text("Editar Donante")
        page.dialog.actions = [
            ft.TextButton("Cancelar", on_click=cerrar_dialogo),
            ft.ElevatedButton("Guardar", on_click=guardar_edicion(donante))
        ]
        page.dialog.open = True
        page.update()

    def eliminar_donante(donante):
        donantes.remove(donante)
        lista_donantes.controls = crear_lista_donantes().controls
        page.update()

    def limpiar_campos():
        nombre_field.value = ""
        email_field.value = ""
        telefono_field.value = ""
        nombre_error.value = ""
        email_error.value = ""
        telefono_error.value = ""
        page.update()

    # Botones de acciones
    def crear_boton_editar(donante):
        return ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda e: editar_donante(donante))

    def crear_boton_eliminar(donante):
        return ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e: eliminar_donante(donante))

    def crear_lista_donantes():
        return ft.Column(
            controls=[
                ft.Row([
                    ft.Text("Seleccionar", weight="bold", color=cherry, width=80),
                    ft.Text("Nombre", weight="bold", color=cherry, width=150),
                    ft.Text("Email", weight="bold", color=cherry, width=200),
                    ft.Text("Teléfono", weight="bold", color=cherry, width=120),
                    ft.Text("Acciones", weight="bold", color=cherry, width=80),
                ], alignment=ft.MainAxisAlignment.CENTER)
            ] + [
                ft.Row([
                    ft.Checkbox(value=False),
                    ft.Container(ft.Text(d["nombre"], color=wine), width=150),
                    ft.Container(ft.Text(d["email"], color=wine), width=200),
                    ft.Container(ft.Text(d["telefono"], color=wine), width=120),
                    ft.Row([
                        crear_boton_editar(d),
                        crear_boton_eliminar(d),
                    ], alignment=ft.MainAxisAlignment.CENTER, width=80),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=5)
                for d in donantes
            ],
            spacing=5,
        )

    lista_donantes = crear_lista_donantes()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Agregar Nuevo Donante"),
        content=ft.Container(
            content=ft.Column([
                ft.Column([nombre_error, nombre_field]),
                ft.Column([email_error, email_field]),
                ft.Column([telefono_error, ft.Row([prefijo_dropdown, telefono_field], spacing=10)]),
            ], spacing=5),
            padding=10,
            width=400
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=cerrar_dialogo),
            ft.ElevatedButton("Agregar", on_click=agregar_donante)
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    fab = ft.FloatingActionButton(icon=ft.Icons.PERSON_ADD, bgcolor=cherry, on_click=lambda e: page.open(dialog))

    main_layout = ft.Column([
        ft.Row([ft.Text("Registro de Donantes", color=cherry, size=24, weight="bold")], alignment=ft.MainAxisAlignment.CENTER),
        lista_donantes,
        ft.Divider(),
    ], spacing=20)

    page.add(
        ft.Row(
            controls=[navbar, ft.Container(content=main_layout, padding=20, expand=True)],
            expand=True
        )
    )
    page.dialog = dialog
    page.add(fab)

ft.app(target=main)
