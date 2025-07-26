import flet as ft
import re
import os
from datetime import date
from controllers.voluntarios_controller import VoluntariosController
from views.navbar import NavBar
from utils.impresion import (
    crear_pdf_listado_voluntarios,
    crear_pdf_detalle_voluntario,
    mostrar_confirmacion_impresion,
    mostrar_exito_impresion
)
from utils.dialogos import mostrar_dialogo_exito, mostrar_dialogo_error, mostrar_confirmacion, cerrar_dialogo


def crear_estadisticas_card_voluntarios(titulo, valor, icono, color, animar_card_fn):
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
    page.title = "Cáritas San Cristóbal - Voluntarios"
    page.window_width = 1000
    page.window_height = 700
    page.bgcolor = "white"
    page.padding = 0

    cherry = "#660924"
    wine = "#630D13"

    navbar = NavBar(page, navegar, cherry=cherry, wine=wine).view
    controller = VoluntariosController()
    voluntarios = controller.cargar_voluntarios() 
    fecha = date.today()
    
    if voluntarios is None:
        voluntarios = [] 
    print(voluntarios)

    # Crear directorio de reportes si no existe
    REPORTES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'reportes')
    if not os.path.exists(REPORTES_DIR):
        os.makedirs(REPORTES_DIR)

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
    
    
    def imprimir_general():
        ruta_pdf = os.path.join(REPORTES_DIR, 'voluntarios_general.pdf')
        crear_pdf_listado_voluntarios(ruta_pdf, voluntarios)
        mostrar_exito_impresion(page, ruta_pdf)

    def mostrar_confirmacion_imprimir_general(e):
        mostrar_confirmacion_impresion(
            page,
            "¿Deseas imprimir el listado general de voluntarios en PDF?",
            imprimir_general
        )

    def imprimir_individual(voluntario):
        nombre = str(voluntario[1]).replace(' ', '_')
        ruta_pdf = os.path.join(REPORTES_DIR, f'voluntario_{nombre}.pdf')
        crear_pdf_detalle_voluntario(ruta_pdf, voluntario)
        mostrar_exito_impresion(page, ruta_pdf)

    def mostrar_confirmacion_imprimir_individual(voluntario):
        mostrar_confirmacion_impresion(
            page,
            f"¿Deseas imprimir el registro de {voluntario[1]} en PDF?",
            lambda: imprimir_individual(voluntario)
        )

    # Campos y errores
    nombre_field = ft.TextField(
        label="Nombre",
        hint_text="Escribe el Nombre del Voluntario aquí",
        prefix_icon=ft.Icons.PERSON_ROUNDED,
        width=410,
        bgcolor="#f9f9f9",
        border_color="#ccc",
        color="black",
        border_radius=8,
        label_style=ft.TextStyle(color="black") 
    )
    
    cedula_field = ft.TextField(
        label="Cédula",
        hint_text="Escribe la Cédula aquí",
        prefix_icon=ft.Icons.CREDIT_CARD,
        width=410,
        bgcolor="#f9f9f9",
        border_color="#ccc",
        color="black",
        border_radius=8,
        label_style=ft.TextStyle(color="black") 
    )
    email_field = ft.TextField(
        label="Email",
        hint_text="Escribe el Email aquí",
        prefix_icon=ft.Icons.EMAIL_ROUNDED,
        width=410,
        bgcolor="#f9f9f9",
        border_color="#ccc",
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
        bgcolor="#f9f9f9",
        border_color="#ccc",
        color="black",
        border_radius=8,
        label_style=ft.TextStyle(color="black") 
    )

    prefijo_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(p) for p in ["0416", "0426", "0414", "0424", "0412"]],
        value="0416",
        width=100,
        bgcolor="#f9f9f9",
        border_color="#ccc",
        color="black",
        border_radius=8,
        label_style=ft.TextStyle(color="black") 
    )

    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    disponibilidad_row = ft.Row([])

    for dia in dias_semana:
        checkbox = ft.Checkbox(value=False)
        columna_dia = ft.Column(
            [
                checkbox,
                ft.Text(dia, size=11, text_align=ft.TextAlign.CENTER, color="black")
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=1,
            width=48
        )
        disponibilidad_row.controls.append(columna_dia)

    # Errores
    nombre_error = ft.Text("", color="red", size=12)
    cedula_error = ft.Text("", color="red", size=12)
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
        if not cedula_field.value.strip() or not cedula_field.value.isdigit() or len(cedula_field.value) < 6:
            cedula_error.value = "⚠️ Ingresa una cédula válida."
            errores = True
        else:
            cedula_error.value = ""

        if not telefono_field.value.isdigit() or len(telefono_field.value) != 7:
            telefono_error.value = "⚠️ Ingresa un número de 7 dígitos."
            errores = True
        else:
            telefono_error.value = ""

        page.update()
        return not errores

    # --- Definición de helpers y componentes visuales ---
    def crear_boton_editar(voluntario):
        return ft.IconButton(icon=ft.Icons.EDIT,icon_color=cherry, on_click=lambda e: abrir_dialogo(voluntario))

    def crear_boton_eliminar(voluntario):
        return ft.IconButton(icon=ft.Icons.DELETE, icon_color=cherry,on_click=lambda e: eliminar_voluntario(voluntario))
    
    def crear_lista_voluntarios(voluntarios):
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        return ft.Column(
            controls=[
                ft.Divider(height=1, color="#e0e0e0"), 
                ft.Container(
                    bgcolor="#e6e6e6",
                    expand=True,
                    content= ft.Row([
                        ft.Text("Codigo", weight="bold", color=cherry, width=100),
                        ft.Text("Nombre", weight="bold", color=cherry, width=180),
                        ft.Text("Disponibilidad", weight="bold", color=cherry, width=200),
                        ft.Text("Ultima Jornada", weight="bold", color=cherry, width=200),
                        ft.Text("Email", weight="bold", color=cherry, width=200),
                        ft.Text("Teléfono", weight="bold", color=cherry, width=200),
                        ft.Text("Acciones", weight="bold", color=cherry, width=80),
                    ], alignment=ft.MainAxisAlignment.START),
                ),
                ft.Divider(height=1, color="#e0e0e0"), 
            ] + [
                ft.Container(
                    content=ft.Row([
                        ft.Container(ft.Text(d[0], color="black"), width=100),
                        ft.Container(ft.Text(d[1], color="black"), width=180),  # Nombre
                        ft.Container(
                            ft.Text(
                                "Todos los días" if set((d[5] or "").replace(" ","").split(",")) == set(dias_semana) else d[5],
                                color="black"
                            ),
                            width=200
                        ),
                        ft.Container(
                            ft.Text(str(d[6]) if d[6] else "-", color="black"),
                            width=200
                        ),
                        ft.Container(ft.Text(d[4], color="black"), width=200),  # Email
                        ft.Container(ft.Text(d[3], color="black"), width=200),  # Teléfono
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
                for d in voluntarios
            ],
            spacing=5,
        )

    # --- ListView global para voluntarios ---
    lista_voluntarios_lv = ft.ListView(
        controls=crear_lista_voluntarios(voluntarios).controls,
        expand=True,
        spacing=0,
        padding=0,
        auto_scroll=False
    )

    def agregar_voluntario(e):
        nonlocal voluntarios
        page.dialog.title = ft.Text(
                "Agregar Nuevo Voluntario",
                size=22,
                weight="bold",
                color=cherry,
                expand=True
         )
        if not validar_campos():
            return
        disponibilidad = obtener_disponibilidad()
        nuevo_voluntario = {
            "nombre": nombre_field.value,
            "cedula": cedula_field.value,
            "email": email_field.value,
            "telefono": f"{prefijo_dropdown.value}-{telefono_field.value}",
        }
        if controller.agregar_voluntario(nuevo_voluntario, disponibilidad):
            voluntarios.clear()
            voluntarios.extend(controller.cargar_voluntarios() or [])
            lista_voluntarios_lv.controls = crear_lista_voluntarios(voluntarios).controls
            limpiar_campos()
            cerrar_dialogo(page)
            mostrar_dialogo_exito(page, "Voluntario agregado con éxito.")
            page.update()
        else:
            mostrar_dialogo_error(page, "No se pudo agregar el voluntario.")

    def imprimir_general():
        ruta_pdf = os.path.join(REPORTES_DIR, 'voluntarios_general.pdf')
        crear_pdf_listado_voluntarios(ruta_pdf, voluntarios)
        mostrar_exito_impresion(page, ruta_pdf)

    def mostrar_confirmacion_imprimir_general(e):
        mostrar_confirmacion_impresion(
            page,
            "¿Deseas imprimir el listado general de voluntarios en PDF?",
            imprimir_general
        )

    def imprimir_individual(voluntario):
        nombre = str(voluntario[1]).replace(' ', '_')
        ruta_pdf = os.path.join(REPORTES_DIR, f'voluntario_{nombre}.pdf')
        crear_pdf_detalle_voluntario(ruta_pdf, voluntario)
        mostrar_exito_impresion(page, ruta_pdf)

    def mostrar_confirmacion_imprimir_individual(voluntario):
        mostrar_confirmacion_impresion(
            page,
            f"¿Deseas imprimir el registro de {voluntario[1]} en PDF?",
            lambda: imprimir_individual(voluntario)
        )

    # Campos y errores
    nombre_field = ft.TextField(
        label="Nombre",
        hint_text="Escribe el Nombre del Voluntario aquí",
        prefix_icon=ft.Icons.PERSON_ROUNDED,
        width=410,
        bgcolor="#f9f9f9",
        border_color="#ccc",
        color="black",
        border_radius=8,
        label_style=ft.TextStyle(color="black") 
    )
    
    cedula_field = ft.TextField(
        label="Cédula",
        hint_text="Escribe la Cédula aquí",
        prefix_icon=ft.Icons.CREDIT_CARD,
        width=410,
        bgcolor="#f9f9f9",
        border_color="#ccc",
        color="black",
        border_radius=8,
        label_style=ft.TextStyle(color="black") 
    )
    email_field = ft.TextField(
        label="Email",
        hint_text="Escribe el Email aquí",
        prefix_icon=ft.Icons.EMAIL_ROUNDED,
        width=410,
        bgcolor="#f9f9f9",
        border_color="#ccc",
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
        bgcolor="#f9f9f9",
        border_color="#ccc",
        color="black",
        border_radius=8,
        label_style=ft.TextStyle(color="black") 
    )

    prefijo_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(p) for p in ["0416", "0426", "0414", "0424", "0412"]],
        value="0416",
        width=100,
        bgcolor="#f9f9f9",
        border_color="#ccc",
        color="black",
        border_radius=8,
        label_style=ft.TextStyle(color="black") 
    )

    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    disponibilidad_row = ft.Row([])

    for dia in dias_semana:
        checkbox = ft.Checkbox(value=False)
        columna_dia = ft.Column(
            [
                checkbox,
                ft.Text(dia, size=11, text_align=ft.TextAlign.CENTER, color="black")
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=1,
            width=48
        )
        disponibilidad_row.controls.append(columna_dia)

    # Errores
    nombre_error = ft.Text("", color="red", size=12)
    cedula_error = ft.Text("", color="red", size=12)
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
        if not cedula_field.value.strip() or not cedula_field.value.isdigit() or len(cedula_field.value) < 6:
            cedula_error.value = "⚠️ Ingresa una cédula válida."
            errores = True
        else:
            cedula_error.value = ""

        if not telefono_field.value.isdigit() or len(telefono_field.value) != 7:
            telefono_error.value = "⚠️ Ingresa un número de 7 dígitos."
            errores = True
        else:
            telefono_error.value = ""

        page.update()
        return not errores

    def agregar_voluntario(e):
        nonlocal voluntarios
        page.dialog.title = ft.Text(
                "Agregar Nuevo Voluntario",
                size=22,
                weight="bold",
                color=cherry,
                expand=True
         )
        if not validar_campos():
            return
        disponibilidad = obtener_disponibilidad()
        
        nuevo_voluntario = {
            "nombre": nombre_field.value,
            "cedula": cedula_field.value,
            "email": email_field.value,
            "telefono": f"{prefijo_dropdown.value}-{telefono_field.value}",
        }
        if controller.agregar_voluntario(nuevo_voluntario, disponibilidad):
            voluntarios.clear()
            voluntarios.extend(controller.cargar_voluntarios() or [])
            lista_voluntarios_lv.controls = crear_lista_voluntarios(voluntarios).controls
            limpiar_campos()
            cerrar_dialogo(page)
            mostrar_dialogo_exito(page, "Voluntario agregado con éxito.")
            page.update()
        else:
            mostrar_dialogo_error(page, "No se pudo agregar el voluntario.")

    def obtener_disponibilidad():
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        disponibilidad = [dia for dia, checkbox in zip(dias, disponibilidad_row.controls) if checkbox.controls[0].value]
        return ','.join(disponibilidad)

    def guardar_edicion(voluntario):
        def _guardar(e):
            nonlocal voluntarios
            if not validar_campos():
                return
            
            disponibilidad = obtener_disponibilidad()
            
            voluntario_actualizado = {
                "nombre": nombre_field.value,
                "cedula": cedula_field.value,
                "email": email_field.value,
                "telefono": f"{prefijo_dropdown.value}-{telefono_field.value}",
            }
            
            voluntario_id = voluntario[0]
            if controller.editar_voluntario(voluntario_id, voluntario_actualizado, disponibilidad):
                voluntarios.clear()
                voluntarios.extend(controller.cargar_voluntarios() or [])
                lista_voluntarios_lv.controls = crear_lista_voluntarios(voluntarios).controls
                limpiar_campos()
                cerrar_dialogo(page)
                mostrar_dialogo_exito(page, "Voluntario actualizado con éxito.")
                page.update()
            else:
                mostrar_dialogo_error(page, "No se pudo actualizar el voluntario.")
        return _guardar

    def confirmar_eliminacion(voluntario):
        def _eliminar(e):
            nonlocal voluntarios
            voluntario_id = voluntario[0]
            if controller.eliminar_voluntario(voluntario_id):
                try:
                    voluntarios.clear()
                    voluntarios.extend(controller.cargar_voluntarios() or [])
                    lista_voluntarios_lv.controls = crear_lista_voluntarios(voluntarios).controls
                    mostrar_dialogo_exito(page, "Voluntario eliminado con éxito.")
                    page.update()
                except ValueError:
                    print("El Voluntario no se encontró en la lista.")
            else:
                mostrar_dialogo_error(page, "No se puede eliminar el Voluntario porque tiene registros asociados.")
        return _eliminar

    def eliminar_voluntario(voluntario):
        usuario = page.session.get("usuario")
        if not usuario or (not usuario.get("eliminar") and not usuario.get("total")):
            page.open(ft.SnackBar(content=ft.Text("No tiene permiso para eliminar voluntarios"), action="OK", bgcolor="red"))
            return
        def on_confirmar():
            confirmar_eliminacion(voluntario)(None)
        mostrar_confirmacion(page, f"¿Estás seguro de que deseas eliminar a {voluntario[1]}?", on_confirmar)

    dialog = ft.AlertDialog(
        modal=False,
        bgcolor="white",
        title=ft.Text("Agregar Nuevo Voluntario"),
        content=ft.Container(
            content=ft.Column([
                ft.Column([nombre_error, nombre_field]),
                ft.Column([cedula_error,cedula_field]),
                ft.Column([email_error, email_field]),
                ft.Column([telefono_error, ft.Row([prefijo_dropdown, telefono_field], spacing=10)]),
                ft.Divider(height=5, color="#e0e0e0"), 
                ft.Text("Disponibilidad:", color="black"),
                disponibilidad_row,
            ], spacing=5),
            padding=10,
            width=400,
            height=450,
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo(page)),
            ft.ElevatedButton("Agregar", on_click=agregar_voluntario, bgcolor="white", color=cherry, style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                side=ft.BorderSide(1, cherry),
                bgcolor={"": "white", "hovered": "#f5f5f5"},
                color={"": cherry, "hovered": wine}
            ))
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )
        
    page.dialog = dialog

    def abrir_dialogo(voluntario=None):
        usuario = page.session.get("usuario")
        if voluntario:
            # Validar permiso antes de abrir el diálogo de editar
            if not usuario or (not usuario.get("modificar") and not usuario.get("total")):
                page.open(ft.SnackBar(content=ft.Text("No tiene permiso para editar voluntarios"), action="OK", bgcolor="red"))
                return
            dialog.title = ft.Text(
                "Editar Voluntario",
                size=22,
                weight="bold",
                color=cherry,
                expand=True
            )
            nombre_field.value = voluntario[1]
            cedula_field.value = voluntario[2]
            email_field.value = voluntario[4]
            telefono_field.value = voluntario[3].split("-")[1]
            prefijo_dropdown.value = voluntario[3].split("-")[0]

            # Cargar disponibilidad
            disponibilidad = voluntario[5].split(',')  # Suponiendo que el índice 5 es la disponibilidad
            for dia, checkbox in zip(dias_semana, disponibilidad_row.controls):
                checkbox.controls[0].value = dia in disponibilidad  # Marca el checkbox si el día está en la disponibilidad

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
                    on_click=guardar_edicion(voluntario),
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
                page.open(ft.SnackBar(content=ft.Text("No tiene permiso para agregar voluntarios"), action="OK", bgcolor="red"))
                return
            dialog.title = ft.Text(
                "Agregar Nuevo Voluntario",
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
                    on_click=agregar_voluntario,
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

    def limpiar_campos():
        cedula_field.value = ""
        nombre_field.value = ""
        email_field.value = ""
        telefono_field.value = ""
        nombre_error.value = ""
        email_error.value = ""
        telefono_error.value = ""
        for checkbox in disponibilidad_row.controls:
            checkbox.controls[0].value = False  # Desmarcar todos los checkboxes
        page.update()

    lista_voluntarios = crear_lista_voluntarios(voluntarios)

    search_field = ft.TextField(
        hint_text='Buscar voluntarios',
        filled=True,
        width=400,
        border_color=ft.Colors.TRANSPARENT, 
        prefix_icon=ft.Icons.SEARCH,
        bgcolor=ft.Colors.WHITE,
        color=cherry,  
        on_change=lambda e: filtrar_voluntarios(e.control.value) 
    )

    def filtrar_voluntarios(query):
        query = query.lower()
        filtrados = [v for v in voluntarios if query in v[1].lower() or query in v[2].lower() or query in v[3].lower() or query in v[4].lower()] 
        lista_voluntarios_lv.controls = crear_lista_voluntarios(filtrados).controls
        page.update()

    voluntarios_activos_card = crear_estadisticas_card_voluntarios(
        "Voluntarios Activos",
        str(len(voluntarios)),  # O el valor que corresponda
        ft.Icons.GROUP,
        "#660924",
        animar_card
    )

    main_layout = ft.Column(
        controls=[
            # Encabezado
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text("Voluntarios", color=cherry, size=24, weight="bold"),
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
            # Lista scrolleable de voluntarios
            ft.Container(
                content=lista_voluntarios_lv,
                expand=True,
                bgcolor="#fff",
                border_radius=8,
                padding=0,
                height=420
            ),
            # Tarjeta Voluntarios Activos al final
            ft.Container(
                content=voluntarios_activos_card,
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
                    padding=ft.padding.only(left=32, right=32, top=24, bottom=24)
                )
            ],
            expand=True
        )
    )

