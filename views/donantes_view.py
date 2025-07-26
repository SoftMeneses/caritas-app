import flet as ft
import re
from datetime import date
from controllers.donantes_controller import DonantesController
from views.navbar import NavBar
from utils.impresion import (
    crear_pdf_blanco,
    mostrar_confirmacion_impresion,
    mostrar_exito_impresion,
    crear_pdf_listado_donantes,
    crear_pdf_detalle_donante
)
from utils.dialogos import mostrar_dialogo_exito, mostrar_dialogo_error, mostrar_confirmacion, cerrar_dialogo
import os

# Tarjeta animada de Donantes Activos
def crear_estadisticas_card_donantes(titulo, valor, icono, color, animar_card_fn):
    return ft.Container(
        width=200,
        height=130,
        bgcolor=color,
        border_radius=10,
        padding=16,
        animate=ft.Animation(400, "easeOutQuad"),
        scale=ft.Scale(1.0),
        content=ft.Column(
            controls=[
                ft.Icon(icono, size=32, color="white"),
                ft.Text(titulo, size=15, color="white70"),
                ft.Text(valor, size=28, weight="bold", color="white"),
            ],
            spacing=4,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        on_hover=animar_card_fn
    )


def main(page: ft.Page, navegar):
    page.title = "Cáritas San Cristóbal - Donantes"
    page.window_width = 1000
    page.window_height = 700
    page.bgcolor = "white"
    page.padding = 0

    cherry = "#660924"
    wine = "#630D13"

    navbar = NavBar(page, navegar, cherry=cherry, wine=wine).view


    
    fecha = date.today()
    controller = DonantesController()
    donantes = controller.cargar_donantes() 
    
    if donantes is None:
        donantes = [] 
    print(donantes)

    def crear_boton_editar(donante):
        return ft.IconButton(icon=ft.Icons.EDIT, icon_color=cherry, on_click=lambda e: abrir_dialogo(donante))

    def crear_boton_eliminar(donante):
        return ft.IconButton(icon=ft.Icons.DELETE,icon_color=cherry, on_click=lambda e: eliminar_donante(donante))

    def crear_lista_donantes(donantes):
        return ft.Column(
            controls=[
                ft.Divider(height=1, color="#e0e0e0"),
                ft.Container(
                    bgcolor="#e6e6e6",
                    expand=True,
                    content=ft.Row([
                        ft.Text("Codigo", weight="bold", color=cherry, width=150),
                        ft.Text("Nombre", weight="bold", color=cherry, width=200),
                        ft.Text("Ultima Donacion", weight="bold", color=cherry, width=250),
                        ft.Text("Email", weight="bold", color=cherry, width=250),
                        ft.Text("Teléfono", weight="bold", color=cherry, width=200),
                        ft.Text("Acciones", weight="bold", color=cherry, width=80),
                    ], alignment=ft.MainAxisAlignment.START)
                ),
                ft.Divider(height=1, color="#e0e0e0")
            ] + [
                ft.Container(
                    content=ft.Row([
                        ft.Container(ft.Text(d[0], color="black"), width=150, height=50),  # Nombre
                        ft.Container(ft.Text(d[1], color="black"), width=200, height=50),
                        ft.Container(ft.Text(d[6], color="black"), width=250, height=50),
                        ft.Container(ft.Text(d[3], color="black"), width=250, height=50),  # Email
                        ft.Container(ft.Text(d[2], color="black"), width=200, height=50),  # Teléfono
                        ft.Row([
                            crear_boton_editar(d),
                            crear_boton_eliminar(d),
                            ft.IconButton(
                                icon=ft.Icons.PICTURE_AS_PDF,
                                tooltip="Imprimir registro",
                                on_click=lambda e, d=d: mostrar_confirmacion_imprimir_individual(d),
                                icon_color=cherry
                            ),
                        ], alignment=ft.MainAxisAlignment.START, spacing=5)
                    ], alignment=ft.MainAxisAlignment.START, spacing=5),
                    bgcolor="#fff",
                    border_radius=8,
                    animate=ft.Animation(400, "easeOutQuad"),
                    scale=ft.Scale(1.0),
                    on_hover=lambda e: animar_fila(e),
                    padding=ft.padding.symmetric(vertical=2, horizontal=0),
                    margin=ft.margin.only(bottom=4)
                )
                for d in donantes
            ],
            spacing=5,
        )

    # Referencia global a la lista de donantes para actualizarla dinámicamente
    lista_donantes_lv = ft.ListView(
        controls=crear_lista_donantes(donantes).controls,
        expand=True,
        spacing=0,
        padding=0,
        auto_scroll=False
    )

    def animar_fila(e):
        if e.data == "true":
            e.control.scale = ft.Scale(1.02)
            e.control.bgcolor = "#fbe9ee"  # <-- Color vino claro para hover
        else:
            e.control.scale = ft.Scale(1.0)
            e.control.bgcolor = "#fff"
        e.control.update()
    
    def animar_card(e):
        if e.data == "true":
            e.control.scale = ft.Scale(1.05)
            e.control.bgcolor = ft.Colors.with_opacity(0.9, e.control.bgcolor)
        else:
            e.control.scale = ft.Scale(1.0)
            e.control.bgcolor = ft.Colors.with_opacity(1.0, e.control.bgcolor)
        e.control.update()
    
    # Campos y errores
    nombre_field = ft.TextField(
        label="Nombre",
        hint_text="Escribe el Nombre aquí",
        prefix_icon=ft.Icons.PERSON_ROUNDED,
        width=410,
        bgcolor="#f9f9f9",  # Fondo más claro
        border_color="#ccc",  # Borde más suave
        color="black",
        border_radius=8,  # Bordes redondeados
        label_style=ft.TextStyle(color="black") 
    )
    email_field = ft.TextField(
        label="Email",
        hint_text="Escribe el Email aquí",
        prefix_icon=ft.Icons.EMAIL_ROUNDED,
        width=410,
        bgcolor="#f9f9f9",  # Fondo más claro
        border_color="#ccc",  # Borde más suave
        color="black",
        border_radius=8, 
        label_style=ft.TextStyle(color="black") 
    )

    cedula_field = ft.TextField(
        label="Cédula",
        hint_text="Escribe la Cédula aquí",
        prefix_icon=ft.Icons.CREDIT_CARD,
        width=410,
        bgcolor="#f9f9f9",  # Fondo más claro
        border_color="#ccc",  # Borde más suave
        color="black",
        border_radius=8, 
        label_style=ft.TextStyle(color="black") 
    )

    direccion_field = ft.TextField(
        label="Dirección",
        hint_text="Escribe la Dirección aquí",
        prefix_icon=ft.Icons.MAPS_HOME_WORK,
        width=410,
        bgcolor="#f9f9f9",  # Fondo más claro
        border_color="#ccc",  # Borde más suave
        color="black",
        border_radius=8, 
        label_style=ft.TextStyle(color="black") 
    )

    telefono_field = ft.TextField(
        label="Teléfono",
        hint_text="Escribe el Teléfono aquí",
        prefix_icon=ft.Icons.PHONE_ROUNDED,
        width=270,
        keyboard_type=ft.KeyboardType.NUMBER,
        bgcolor="#f9f9f9",  # Fondo más claro
        border_color="#ccc",  # Borde más suave
        color="black",
        border_radius=8, 
        label_style=ft.TextStyle(color="black") 
    )

    prefijo_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(p) for p in ["0416", "0426", "0414", "0424", "0412"]],
        value="0416",
        width=100,
        bgcolor="#f9f9f9",  # Fondo más claro
        border_color="#ccc",  # Borde más suave
        color="black",
        border_radius=8, 
        label_style=ft.TextStyle(color="black") 
    )

    # Errores
    nombre_error = ft.Text("", color="red", size=12)
    cedula_error = ft.Text("", color="red", size=12)
    direccion_error = ft.Text("", color="red", size=12)
    email_error = ft.Text("", color="red", size=12)
    telefono_error = ft.Text("", color="red", size=12)

    def validar_campos():
        errores = False
        if not nombre_field.value.strip():
            nombre_error.value = "⚠️ Ingresa un nombre."
            errores = True
        else:
            nombre_error.value = ""

        if not email_field.value.strip() or not re.match(r"[^@]+@[^@]+\.[^@]+", email_field.value):
            email_error.value = "⚠️ Ingresa un email válido."
            errores = True
        else:
            email_error.value = ""

        if not telefono_field.value.isdigit() or len(telefono_field.value) != 7:
            telefono_error.value = "⚠️ Ingresa un número de 7 dígitos."
            errores = True
        else:
            telefono_error.value = ""

        if not cedula_field.value.strip() or not cedula_field.value.isdigit() or len(cedula_field.value) < 6:
            cedula_error.value = "⚠️ Ingresa una cédula válida."
            errores = True
        else:
            cedula_error.value = ""

        if not direccion_field.value.strip():
            direccion_error.value = "⚠️ Ingresa una dirección."
            errores = True
        else:
            direccion_error.value = ""

        page.update()
        return not errores



    def agregar_donante(e):
        
        page.dialog.title = ft.Text(
                "Agregar Nuevo Donante",
                size=22,
                weight="bold",
                color=cherry,
                expand=True
         )
        if not validar_campos():
            return

        nuevo_donante = {
            "nombre": nombre_field.value,
            "email": email_field.value,
            "cedula": cedula_field.value,
            "direccion": direccion_field.value,
            "telefono": f"{prefijo_dropdown.value}-{telefono_field.value}",
        }
        
        if controller.agregar_donante(nuevo_donante):
            donantes.clear()
            donantes.extend(controller.cargar_donantes() or [])
            lista_donantes_lv.controls = crear_lista_donantes(donantes).controls
            limpiar_campos()
            cerrar_dialogo(page)
            mostrar_dialogo_exito(page, "Donante agregado con éxito.")
            page.update()
        else:
            mostrar_dialogo_error(page, "No se pudo agregar el donante.")


    def guardar_edicion(donante):
        def _guardar(e):
            if not validar_campos():
                return
            
            donante_actualizado = {
                "nombre": nombre_field.value,
                "email": email_field.value,
                "cedula": cedula_field.value,
                "direccion": direccion_field.value,
                "telefono": f"{prefijo_dropdown.value}-{telefono_field.value}",
            }
            
            donante_id = donante[0]  # Asegúrate de que esto sea correcto
            if controller.editar_donante(donante_id, donante_actualizado):
                donantes.clear()
                donantes.extend(controller.cargar_donantes() or [])
                lista_donantes_lv.controls = crear_lista_donantes(donantes).controls  
                limpiar_campos()
                cerrar_dialogo(page)
                mostrar_dialogo_exito(page, "Donante actualizado con éxito.")
                page.update()
            else:
                mostrar_dialogo_error(page, "No se pudo actualizar el donante.")
        return _guardar

            
    def confirmar_eliminacion(donante):
        def _eliminar(e):
            donante_id = donante[0]  
            if controller.eliminar_donante(donante_id):  
                try:
                    donantes.clear()
                    donantes.extend(controller.cargar_donantes() or [])
                    lista_donantes_lv.controls = crear_lista_donantes(donantes).controls
                    mostrar_dialogo_exito(page, "Donante eliminado con éxito.")
                    page.update()  
                except ValueError:
                    print("El donante no se encontró en la lista.")  
            else:
                mostrar_dialogo_error(page, "No se puede eliminar el donante porque tiene donaciones registradas.") 
        return _eliminar


    def eliminar_donante(donante):
        usuario = page.session.get("usuario")
        if not usuario or (not usuario.get("eliminar") and not usuario.get("total")):
            page.open(ft.SnackBar(content=ft.Text("No tiene permiso para eliminar donantes"), action="OK", bgcolor="red"))
            return
        def on_confirmar():
            confirmar_eliminacion(donante)(None)
        mostrar_confirmacion(page, f"¿Estás seguro de que deseas eliminar a {donante[1]}?", on_confirmar)


    def limpiar_campos():
        nombre_field.value = ""
        email_field.value = ""
        cedula_field.value = ""
        direccion_field.value = ""
        telefono_field.value = ""
        nombre_error.value = ""
        email_error.value = ""
        telefono_error.value = ""
        cedula_error.value = ""
        direccion_error.value = ""
        page.update()

    def crear_boton_editar(donante):
        return ft.IconButton(icon=ft.Icons.EDIT, icon_color=cherry, on_click=lambda e: abrir_dialogo(donante))

    def crear_boton_eliminar(donante):
        return ft.IconButton(icon=ft.Icons.DELETE,icon_color=cherry, on_click=lambda e: eliminar_donante(donante))
    
    # Crear carpeta 'reportes' si no existe
    REPORTES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'reportes')
    if not os.path.exists(REPORTES_DIR):
        os.makedirs(REPORTES_DIR)

    def imprimir_general():
        ruta_pdf = os.path.join(REPORTES_DIR, 'donantes_general.pdf')
        crear_pdf_listado_donantes(ruta_pdf, donantes)
        mostrar_exito_impresion(page, ruta_pdf)

    def imprimir_individual(donante):
        nombre = str(donante[1]).replace(' ', '_')
        ruta_pdf = os.path.join(REPORTES_DIR, f'donante_{nombre}.pdf')
        crear_pdf_detalle_donante(ruta_pdf, donante)
        mostrar_exito_impresion(page, ruta_pdf)

    def mostrar_confirmacion_imprimir_general(e):
        mostrar_confirmacion_impresion(
            page,
            "¿Deseas imprimir el listado general de donaciones en PDF?",
            imprimir_general
        )

    def mostrar_confirmacion_imprimir_individual(donante):
        mostrar_confirmacion_impresion(
            page,
            f"¿Deseas imprimir el registro de {donante[1]} en PDF?",
            lambda: imprimir_individual(donante)
        )    
    
    dialog = ft.AlertDialog(
        modal=False,
        bgcolor="white",
        title=ft.Text("Agregar Nuevo Donante"),
        content=ft.Container(
            content=ft.Column([
                ft.Column([nombre_error, nombre_field]),
                ft.Column([cedula_error, cedula_field]),
                ft.Column([telefono_error, ft.Row([prefijo_dropdown, telefono_field], spacing=10)]),
                ft.Column([email_error, email_field]),
                ft.Column([direccion_error, direccion_field]),
            ], spacing=5),
            padding=10,
            width=400,
            height=500,
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo(page)),
            ft.ElevatedButton(
                "Agregar",
                on_click=agregar_donante,
                bgcolor="white",
                color=cherry,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                    side=ft.BorderSide(1, cherry),
                    bgcolor={"": "white", "hovered": "#f5f5f5"},
                    color={"": cherry, "hovered": wine}
                )
            )
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )
    page.dialog = dialog

    def abrir_dialogo(donante=None):
        usuario = page.session.get("usuario")
        if donante:
            # Validar permiso antes de abrir el diálogo de editar
            if not usuario or (not usuario.get("modificar") and not usuario.get("total")):
                page.open(ft.SnackBar(content=ft.Text("No tiene permiso para editar donantes"), action="OK", bgcolor="red"))
                return
            dialog.title = ft.Text(
                "Editar Donante",
                size=22,
                weight="bold",
                color=cherry,
                expand=True
            )
            nombre_field.value = donante[1]  
            cedula_field.value = donante[4]  
            email_field.value = donante[3]  
            telefono_field.value = donante[2].split("-")[1]  
            prefijo_dropdown.value = donante[2].split("-")[0]
            direccion_field.value = donante[5] 
            dialog.actions = [
                ft.ElevatedButton(
                    "Cancelar",
                    on_click=lambda e: cerrar_dialogo(page),
                    bgcolor="white",
                    color=cherry,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        side=ft.BorderSide(1, cherry),
                        bgcolor={"": "white", "hovered": "#f5f5f5"},
                        color={"": cherry, "hovered": wine}
                    )
                ),
                ft.ElevatedButton(
                    "Guardar",
                    on_click=guardar_edicion(donante),
                    bgcolor="white",
                    color=cherry,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        side=ft.BorderSide(1, cherry),
                        bgcolor={"": "white", "hovered": "#f5f5f5"},
                        color={"": cherry, "hovered": wine}
                    )
                )
            ]
        else:
            # Validar permiso antes de abrir el diálogo de agregar
            if not usuario or (not usuario.get("insertar") and not usuario.get("total")):
                page.open(ft.SnackBar(content=ft.Text("No tiene permiso para agregar donantes"), action="OK", bgcolor="red"))
                return
            dialog.title = ft.Text(
                "Agregar Nuevo Donante",
                size=22,
                weight="bold",
                color=cherry,
                expand=True
            )
            limpiar_campos()
            dialog.actions = [
                ft.ElevatedButton(
                    "Cancelar",
                    on_click=lambda e: cerrar_dialogo(page),
                    bgcolor="white",
                    color=cherry,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        side=ft.BorderSide(1, cherry),
                        bgcolor={"": "white", "hovered": "#f5f5f5"},
                        color={"": cherry, "hovered": wine}
                    )
                ),
                ft.ElevatedButton(
                    "Agregar",
                    on_click=agregar_donante,
                    bgcolor="white",
                    color=cherry,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        side=ft.BorderSide(1, cherry),
                        bgcolor={"": "white", "hovered": "#f5f5f5"},
                        color={"": cherry, "hovered": wine}
                    )
                )
            ]

        page.open(dialog)
        page.update()

    def filtrar_donantes(query):
        query = query.lower()
        filtrados = [v for v in donantes if query in v[1].lower() or query in v[2].lower() or query in v[3].lower()] 
        lista_donantes_lv.controls = crear_lista_donantes(filtrados).controls
        page.update()

    search_field = ft.TextField(
        hint_text='Buscar Donantes',
        filled=True,
        width=400,
        border_color=ft.Colors.TRANSPARENT, 
        prefix_icon=ft.Icons.SEARCH,
        bgcolor=ft.Colors.WHITE,
        color=cherry,  
        on_change=lambda e: filtrar_donantes(e.control.value)
    )

    donantes_activos_card = crear_estadisticas_card_donantes(
        "Donantes Activos",
        str(len(donantes)),  # O el valor que corresponda
        ft.Icons.PEOPLE,
        "#660924",
        animar_card
    )

    main_layout = ft.Column(
        controls=[
            # Encabezado
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text("Donantes", color=cherry, size=24, weight="bold"),
                        ft.FloatingActionButton(icon=ft.Icons.ADD, bgcolor=wine, on_click=lambda e: abrir_dialogo()),
                        ft.Container(content=search_field, expand=True),
                        ft.IconButton(
                            icon=ft.Icons.PICTURE_AS_PDF,
                            tooltip="Imprimir listado general",
                            on_click=mostrar_confirmacion_imprimir_general,
                            icon_color=cherry
                        ),
                        ft.Text(str(fecha), weight="bold", color=cherry),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                padding=ft.padding.only(top=40, left=0, right=0, bottom=10),
            ),
            # Lista scrolleable de donantes
            ft.Container(
                content=lista_donantes_lv,
                expand=True,
                bgcolor="#fff",
                border_radius=8,
                padding=0,
                height=420  # Ajusta la altura máxima visible de la lista
            ),
            # Tarjeta Donantes Activos al final
            ft.Container(
                content=donantes_activos_card,
                alignment=ft.alignment.bottom_right,
                margin=ft.margin.only(left=0, bottom=30, top=20, right=0)
            )
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.START,
    )

    page.add(
        ft.Row(
            controls=[
                navbar,
                ft.Container(
                    content=main_layout,
                    expand=True,
                    padding=ft.padding.only(left=32, right=32, top=24, bottom=24)  # <-- Margen general
                )
            ],
            expand=True
        )
    )
