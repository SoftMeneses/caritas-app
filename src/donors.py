import flet as ft
import re

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

    # Lista de donantes (inventada)
    donantes = [
        {"nombre": "Juan Pérez", "email": "juan.perez@example.com", "telefono": "123-456-7890"},
        {"nombre": "María Gómez", "email": "maria.gomez@example.com", "telefono": "987-654-3210"},
        {"nombre": "Carlos López", "email": "carlos.lopez@example.com", "telefono": "555-123-4567"},
    ]

    # Contenedor de la lista de donantes con checkboxes y celdas
    lista_donantes = ft.Column(
        controls=[  
            # Encabezados de la tabla
            ft.Row([
                ft.Text("Seleccionar", weight="bold", color=cherry, width=80),
                ft.Text("Nombre", weight="bold", color=cherry, width=150),
                ft.Text("Email", weight="bold", color=cherry, width=200),
                ft.Text("Teléfono", weight="bold", color=cherry, width=120),
            ], alignment=ft.MainAxisAlignment.CENTER)
        ] + [
            # Fila de cada donante con checkbox
            ft.Row([
                ft.Checkbox(value=False),  # checkbox al inicio de cada fila
                ft.Container(ft.Text(d["nombre"], color=wine), width=150),
                ft.Container(ft.Text(d["email"], color=wine), width=200),
                ft.Container(ft.Text(d["telefono"], color=wine), width=120),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=5)
            for d in donantes
        ],
        spacing=5,
    )

    # Opciones de prefijo telefónico
    prefijo_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("0416"),
            ft.dropdown.Option("0426"),
            ft.dropdown.Option("0414"),
            ft.dropdown.Option("0424"),
            ft.dropdown.Option("0412"),
        ],
        value="0416",  # Valor por defecto
        width=100,
        filled=True
    )

    # Campos de entrada con hint_text y validaciones
    nombre_field = ft.TextField(
        label="Nombre", 
        hint_text="Escribe el Nombre aquí", 
        filled=True,
        prefix_icon=ft.Icons.PERSON_ROUNDED,
        width=410
    )    
    email_field = ft.TextField(
        label="Email", 
        hint_text="Escribe el Email aquí", 
        filled=True,
        prefix_icon=ft.Icons.EMAIL_ROUNDED,
        width=410
    )
    telefono_field = ft.TextField(
        label="Teléfono", 
        hint_text="Escribe el Teléfono aquí", 
        filled=True,
        prefix_icon=ft.Icons.PHONE_ROUNDED,
        keyboard_type=ft.KeyboardType.NUMBER
    )

    # Mensajes de error
    nombre_error = ft.Text("", color="red", size=12)
    email_error = ft.Text("", color="red", size=12)
    telefono_error = ft.Text("", color="red", size=12)

    def validar_campos():
        # Verifica si los campos están vacíos y muestra mensajes de error
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

        # Validación del teléfono: solo números y exactamente 7 dígitos
        if not telefono_field.value.isdigit() or len(telefono_field.value) != 7:
            telefono_error.value = "⚠️ Ingresa un número de 7 dígitos."
            errores = True
        else:
            telefono_error.value = ""

        page.update()
        return not errores  # Retorna True si no hay errores

    def agregar_donante(e):
        if not validar_campos():
            return  # Si hay errores, se detiene aquí

        nuevo_donante = {
            "nombre": nombre_field.value,
            "email": email_field.value,
            "telefono": f"{prefijo_dropdown.value}-{telefono_field.value}",  # Prefijo + número
        }
        donantes.append(nuevo_donante)
        lista_donantes.controls.append(
            ft.Row([
                ft.Checkbox(value=False),  # Agregar checkbox al inicio de cada fila
                ft.Container(ft.Text(nuevo_donante["nombre"], color="black"), width=150),
                ft.Container(ft.Text(nuevo_donante["email"], color="black"), width=200),
                ft.Container(ft.Text(nuevo_donante["telefono"], color="black"), width=120),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=5)
        )
        page.update()

        # Limpiar los campos
        nombre_field.value = ""
        email_field.value = ""
        telefono_field.value = ""

        # Limpiar mensajes de error después de enviar correctamente
        nombre_error.value = ""
        email_error.value = ""
        telefono_error.value = ""

        page.update()

    agregar_button = ft.ElevatedButton("Agregar Donante", on_click=agregar_donante)

    # Teléfono con prefijo y campo
    telefono_container = ft.Row([prefijo_dropdown, telefono_field], spacing=10)

    # Contenedor para el formulario con mensajes de error encima de los inputs
    form_container = ft.Container(
        width=500,
        content=ft.Column([  
            ft.Column([nombre_error, nombre_field]),  
            ft.Column([email_error, email_field]),    
            ft.Column([telefono_error, telefono_container]),   
            ft.Container(agregar_button, padding=ft.padding.only(top=10))
        ], spacing=5),
        padding=20,
        border_radius=10,
        bgcolor="#f0f0f0",
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.GREY_400)
    )

    # Diseño principal
    main_layout = ft.Column([
        ft.Row(
            [ft.Text("Registro de Donantes", color=cherry, size=24, weight="bold")],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        lista_donantes,
        ft.Divider(),
        form_container
    ], spacing=20)

    page.add(main_layout)

ft.app(target=main)