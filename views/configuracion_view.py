import flet as ft
from datetime import date
from views.navbar import NavBar
from utils.dialogos import mostrar_dialogo_exito, mostrar_dialogo_error, mostrar_confirmacion, cerrar_dialogo
from controllers.configuracion_controller import UsuariosPerfilesController

def main(page: ft.Page, navegar):
    
    page.title = "Cáritas San Cristóbal - Control de Usuarios"
    page.window_width = 1000
    page.window_height = 700
    page.bgcolor = "white"
    page.padding = 0

    cherry = "#660924"
    wine = "#630D13"

    fecha = date.today()

    navbar = NavBar(page, navegar, cherry=cherry, wine=wine).view

    controlador = UsuariosPerfilesController()

    # Campos de entrada para usuarios
    nombre_field = ft.TextField(
        label="Nombre",
        hint_text="Escribe el Nombre aquí",
        prefix_icon=ft.Icons.PERSON_ROUNDED,
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

    perfil_dropdown = ft.Dropdown(
        options=[],  # Se llenará dinámicamente
        width=410,
        bgcolor="#f9f9f9",
        border_color="#ccc",
        color="black",
        border_radius=8,
        label_style=ft.TextStyle(color="black")
    )
    password_field = ft.TextField(
        label="Contraseña",
        hint_text="Escribe la contraseña aquí",
        prefix_icon=ft.Icons.LOCK,
        width=410,
        bgcolor="#f9f9f9",
        border_color="#ccc",
        color="black",
        border_radius=8,
        label_style=ft.TextStyle(color="black"),
        password=True,
        can_reveal_password=True
    )

    # Errores
    nombre_error = ft.Text("", color="red", size=12)
    email_error = ft.Text("", color="red", size=12)
    password_error = ft.Text("", color="red", size=12)

    def limpiar_campos():
        nombre_field.value = ""
        email_field.value = ""
        nombre_error.value = ""
        email_error.value = ""
        perfil_dropdown.value = None
        password_field.value = ""
        password_error.value = ""
        page.update()

    def cargar_perfiles():
        perfiles = controlador.obtener_perfiles()
        perfil_dropdown.options = [ft.dropdown.Option(str(p['ID']), p['NOMBRE']) for p in perfiles]
        if perfiles:
            perfil_dropdown.value = str(perfiles[0]['ID'])
        page.update()

    def abrir_dialogo_usuario(e=None):
        cargar_perfiles()
        dialog_usuario.title = ft.Text("Agregar Nuevo Usuario", size=22, weight="bold", color=cherry)
        limpiar_campos()
        page.dialog = dialog_usuario
        page.open(dialog_usuario)
        page.update()

    def agregar_usuario(e):
        errores = False
        if not nombre_field.value.strip():
            nombre_error.value = "El nombre es obligatorio."
            errores = True
        else:
            nombre_error.value = ""
        if not email_field.value.strip():
            email_error.value = "El email es obligatorio."
            errores = True
        else:
            email_error.value = ""
        if not password_field.value.strip():
            password_error.value = "La contraseña es obligatoria."
            errores = True
        else:
            password_error.value = ""
        if not perfil_dropdown.value:
            mostrar_dialogo_error(page, "Debes seleccionar un perfil.")
            errores = True

        page.update()
        if errores:
            return

        nuevo_usuario = {
            "nombre": nombre_field.value,
            "email": email_field.value,
            "perfil_id": int(perfil_dropdown.value),
            "password": password_field.value
        }
        if controlador.agregar_usuario(nuevo_usuario):
            mostrar_dialogo_exito(page, "Usuario agregado con éxito.")
            actualizar_lista_usuarios()
            cerrar_dialogo(page)
        else:
            mostrar_dialogo_error(page, "No se pudo agregar el usuario.")

    dialog_usuario = ft.AlertDialog(
        modal=False,
        bgcolor="white",
        title=ft.Text("Agregar Nuevo Usuario"),
        content=ft.Container(
        content=ft.Column([
            ft.Column([nombre_error, nombre_field]),
            ft.Column([email_error, email_field]),
            ft.Column([password_error, password_field]),
            ft.Column([ft.Text("Perfil"), perfil_dropdown]),
        ], spacing=5),
        padding=10,
        width=400,
        height=450,
    ),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo(page)),
            ft.ElevatedButton(
                "Agregar",
                on_click=agregar_usuario,
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

    def abrir_dialogo_editar_usuario(usuario):
        cargar_perfiles()
        dialog_usuario.title = ft.Text("Editar Usuario", size=22, weight="bold", color=cherry)
        nombre_field.value = usuario["nombre"]
        email_field.value = usuario["email"]
        perfil_dropdown.value = str(usuario["perfil_id"])
        password_field.value = ""  # Por seguridad, pide nueva contraseña si se desea cambiar
        page.dialog = dialog_usuario
        page.open(dialog_usuario)
        page.update()

        def guardar_edicion(e):
            errores = False
            if not nombre_field.value.strip():
                nombre_error.value = "El nombre es obligatorio."
                errores = True
            else:
                nombre_error.value = ""
            if not email_field.value.strip():
                email_error.value = "El email es obligatorio."
                errores = True
            else:
                email_error.value = ""
            if not perfil_dropdown.value:
                mostrar_dialogo_error(page, "Debes seleccionar un perfil.")
                errores = True
            page.update()
            if errores:
                return

            datos = {
                "nombre": nombre_field.value,
                "email": email_field.value,
                "perfil_id": int(perfil_dropdown.value),
                "password": password_field.value if password_field.value else usuario["password"]
            }
            if controlador.actualizar_usuario(usuario["ID"], datos):
                mostrar_dialogo_exito(page, "Usuario actualizado con éxito.")
                actualizar_lista_usuarios()
                cerrar_dialogo(page)
            else:
                mostrar_dialogo_error(page, "No se pudo actualizar el usuario.")

        # Cambia el botón de acción a "Guardar"
        dialog_usuario.actions[-1].text = "Guardar"
        dialog_usuario.actions[-1].on_click = guardar_edicion

    def eliminar_usuario(usuario):
        def on_confirmar():
            if usuario["nombre"].lower() == "admin":
                mostrar_dialogo_error(page, "No se puede eliminar el usuario admin.")
                return
            if controlador.eliminar_usuario(usuario["ID"]):
                mostrar_dialogo_exito(page, "Usuario eliminado con éxito.")
                actualizar_lista_usuarios()
            else:
                mostrar_dialogo_error(page, "No se pudo eliminar el usuario.")
        mostrar_confirmacion(page, f"¿Estás seguro de que deseas eliminar a {usuario['nombre']}?", on_confirmar)


    # Diálogo para crear perfiles
    perfil_nombre_field = ft.TextField(
        label="Perfil Nuevo",
        hint_text="Escribe el nombre del perfil aquí",
        width=400,
        bgcolor="#f9f9f9",
        border_color="#ccc",
        color="black",
        border_radius=8,
        label_style=ft.TextStyle(color="black")
    )

    permiso_consulta = ft.Checkbox(label="Consulta", label_style=ft.TextStyle(color="black"))
    permiso_modificar = ft.Checkbox(label="Modificar", label_style=ft.TextStyle(color="black"))
    permiso_insertar = ft.Checkbox(label="Insertar", label_style=ft.TextStyle(color="black"))
    permiso_eliminar = ft.Checkbox(label="Eliminar", label_style=ft.TextStyle(color="black"))
    permiso_total = ft.Checkbox(label="Total", label_style=ft.TextStyle(color="black"))

    # Dropdown para seleccionar perfil existente al crear/editar
    perfil_existente_dropdown = ft.Dropdown(
        options=[],
        width=400,
        bgcolor="#f9f9f9",
        border_color="#ccc",
        color="black",
        border_radius=8,
        label="Perfil Existente",
        label_style=ft.TextStyle(color="black"),
        on_change=None  # Se asigna después
    )

    def cargar_perfiles_en_dropdown():
        perfiles = controlador.obtener_perfiles()
        perfil_existente_dropdown.options = [ft.dropdown.Option(str(p['ID']), p['NOMBRE']) for p in perfiles]
        page.update()

    def eliminar_perfil(e=None):
        id_sel = perfil_existente_dropdown.value
        if not id_sel:
            mostrar_dialogo_error(page, "Selecciona un perfil para eliminar.")
            return
        if not puede_eliminar_perfil(int(id_sel)):
            mostrar_dialogo_error(page, "No se puede eliminar el perfil porque tiene usuarios asociados.")
            return
        def on_confirmar():
            if controlador.eliminar_perfil(int(id_sel)):
                mostrar_dialogo_exito(page, "Perfil eliminado con éxito.")
                cargar_perfiles_en_dropdown()
                cargar_perfiles()
                limpiar_campos_perfil()
                perfil_existente_dropdown.value = None
                page.update()
            else:
                mostrar_dialogo_error(page, "No se pudo eliminar el perfil.")
        mostrar_confirmacion(page, "¿Estás seguro de que deseas eliminar este perfil?", on_confirmar)

    def puede_eliminar_perfil(perfil_id):
        # Devuelve True si no hay usuarios asociados a ese perfil
        usuarios = controlador.obtener_usuarios()
        return not any(u["perfil_id"] == perfil_id for u in usuarios)

    def on_perfil_existente_change(e):
        id_sel = perfil_existente_dropdown.value
        if not id_sel:
            limpiar_campos_perfil()
            dialog_perfil.actions = [
                ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo(page)),
                ft.ElevatedButton(
                    "Guardar",
                    on_click=agregar_o_actualizar_perfil,
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
            page.update()
            return
        perfiles = controlador.obtener_perfiles()
        perfil = next((p for p in perfiles if str(p['ID']) == id_sel), None)
        if perfil:
            perfil_nombre_field.value = perfil['NOMBRE']
            permiso_consulta.value = bool(perfil['CONSULTA'])
            permiso_modificar.value = bool(perfil['MODIFICAR'])
            permiso_insertar.value = bool(perfil['INSERTAR'])
            permiso_eliminar.value = bool(perfil['ELIMINAR'])
            permiso_total.value = bool(perfil['TOTAL'])
            # Si el perfil puede eliminarse, muestra el botón Eliminar
            if puede_eliminar_perfil(int(id_sel)):
                dialog_perfil.actions = [
                    ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo(page)),
                    ft.ElevatedButton(
                        "Eliminar",
                        on_click=eliminar_perfil,
                        bgcolor=wine,
                        color="white",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            side=ft.BorderSide(1, wine),
                            bgcolor={"": wine, "hovered": cherry},
                            color={"": "white", "hovered": "#fff0f0"}
                        )
                    ),
                    ft.ElevatedButton(
                        "Guardar",
                        on_click=agregar_o_actualizar_perfil,
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
                dialog_perfil.actions = [
                    ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo(page)),
                    ft.ElevatedButton(
                        "Guardar",
                        on_click=agregar_o_actualizar_perfil,
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
            page.update()

    perfil_existente_dropdown.on_change = on_perfil_existente_change

    def limpiar_campos_perfil():
        perfil_nombre_field.value = ""
        permiso_consulta.value = False
        permiso_modificar.value = False
        permiso_insertar.value = False
        permiso_eliminar.value = False
        permiso_total.value = False
        page.update()

    def abrir_dialogo_perfil(e=None):
        cargar_perfiles_en_dropdown()
        limpiar_campos_perfil()
        perfil_existente_dropdown.value = None
        dialog_perfil.title = ft.Text("Crear o Editar Perfil", size=22, weight="bold", color=cherry)
        page.dialog = dialog_perfil
        page.open(dialog_perfil)
        page.update()

    def agregar_o_actualizar_perfil(e):
        if not perfil_nombre_field.value.strip():
            mostrar_dialogo_error(page, "El nombre del perfil es obligatorio.")
            return
        permisos = {
            "consulta": permiso_consulta.value,
            "modificar": permiso_modificar.value,
            "insertar": permiso_insertar.value,
            "eliminar": permiso_eliminar.value,
            "total": permiso_total.value
        }
        id_sel = perfil_existente_dropdown.value
        if id_sel:
            # Actualizar perfil existente
            if controlador.actualizar_perfil(int(id_sel), perfil_nombre_field.value, permisos):
                mostrar_dialogo_exito(page, "Perfil actualizado con éxito.")
                cargar_perfiles()
                cerrar_dialogo(page)
            else:
                mostrar_dialogo_error(page, "No se pudo actualizar el perfil.")
        else:
            # Crear perfil nuevo
            if controlador.agregar_perfil(perfil_nombre_field.value, permisos):
                mostrar_dialogo_exito(page, "Perfil creado con éxito.")
                cargar_perfiles()
                cerrar_dialogo(page)
            else:
                mostrar_dialogo_error(page, "No se pudo crear el perfil.")

    dialog_perfil = ft.AlertDialog(
        modal=False,
        bgcolor="white",
        title=ft.Text("Crear o Editar Perfil"),
        content=ft.Container(
            content=ft.Column([
                perfil_existente_dropdown,
                perfil_nombre_field,
                permiso_consulta,
                permiso_modificar,
                permiso_insertar,
                permiso_eliminar,
                permiso_total,
            ], spacing=10),
            padding=10,
            width=400,
            height=350,
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo(page)),
            ft.ElevatedButton(
                "Guardar",
                on_click=agregar_o_actualizar_perfil,
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

    # Lista de usuarios (de la base de datos)
    def actualizar_lista_usuarios():
        usuarios = controlador.obtener_usuarios()  # Debe traer nombre, email, perfil, permisos
        lista_usuarios.controls = crear_lista_usuarios(usuarios).controls
        page.update()

    def crear_lista_usuarios(usuarios):
        return ft.Column(
            controls=[
                ft.Divider(height=1, color="#e0e0e0"),
                ft.Container(
                    bgcolor="#e6e6e6",
                    expand=True,
                    content=ft.Row([
                        ft.Text("Nombre", weight="bold", color=cherry, width=250),
                        ft.Text("Email", weight="bold", color=cherry, width=250),
                        ft.Text("Perfil", weight="bold", color=cherry, width=200),
                        ft.Text("Permisos", weight="bold", color=cherry, width=200),
                        ft.Text("Eliminar", weight="bold", color=cherry, width=150),
                        ft.Text("Editar", weight="bold", color=cherry, width=150),
                    ], alignment=ft.MainAxisAlignment.START)
                ),
                ft.Divider(height=1, color="#e0e0e0")
            ] + [
                ft.Row([
                    ft.Container(ft.Text(u["nombre"], color="black"), width=250),
                    ft.Container(ft.Text(u["email"], color="black"), width=250),
                    ft.Container(ft.Text(u["perfil"], color="black"), width=200),
                    ft.Container(ft.Text(u["permisos"], color="black"), width=200),
                    ft.Container(
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color=cherry,
                            on_click=lambda e, u=u: eliminar_usuario(u)
                        ),
                        width=150
                    ),
                    ft.Container(
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            icon_color=cherry,
                            on_click=lambda e, u=u: abrir_dialogo_editar_usuario(u)
                        ),
                        width=150
                    )
                ], alignment=ft.MainAxisAlignment.START, spacing=5)
                for u in usuarios
            ],
            spacing=5,
        )

    usuarios = controlador.obtener_usuarios()
    lista_usuarios = crear_lista_usuarios(usuarios)

    search_field = ft.TextField(
        hint_text='Buscar Usuarios',
        filled=True,
        width=400,
        border_color=ft.Colors.TRANSPARENT,
        prefix_icon=ft.Icons.SEARCH,
        bgcolor=ft.Colors.WHITE,
        color=cherry,
        on_change=lambda e: filtrar_usuarios(e.control.value)
    )

    def filtrar_usuarios(query):
        query = query.lower()
        usuarios = controlador.obtener_usuarios()
        filtrados = [u for u in usuarios if query in u["nombre"].lower() or query in u["email"].lower()]
        lista_usuarios.controls = crear_lista_usuarios(filtrados).controls
        page.update()

    main_layout = ft.Container(
        ft.Column([
            ft.Row(
                controls=[
                    ft.Text("Control de Usuarios", color=cherry, size=24, weight="bold"),
                    ft.FloatingActionButton(icon=ft.Icons.ADD, bgcolor=wine, on_click=lambda e: abrir_dialogo_usuario()),
                    ft.FloatingActionButton(icon=ft.Icons.PERSON_ADD, bgcolor=wine, on_click=lambda e: abrir_dialogo_perfil()),
                    ft.Container(content=search_field, expand=True),
                    ft.Text(str(fecha), weight="bold", color=cherry),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            lista_usuarios,
        ], spacing=20),
        padding=ft.Padding(left=50, top=50, right=20, bottom=0)
    )

    page.add(
        ft.Row(
            controls=[navbar, ft.Container(content=main_layout, expand=True)],
            expand=True
        )
    )
