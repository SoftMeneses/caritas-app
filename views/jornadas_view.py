import flet as ft
from datetime import date, datetime
from controllers.jornadas_controller import JornadasController
from controllers.voluntarios_controller import VoluntariosController
from utils.impresion import (
    crear_pdf_listado_jornadas,
    crear_pdf_detalle_jornada,
    mostrar_confirmacion_impresion,
    mostrar_exito_impresion
)
from views.navbar import NavBar
from utils.dialogos import mostrar_dialogo_exito, mostrar_dialogo_error, mostrar_confirmacion, cerrar_dialogo
import os

def crear_estadisticas_card_jornadas(titulo, valor, icono, color, animar_card_fn):
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
    
def crear_proxima_jornada_card(nombre, fecha, ubicacion, animar_card_fn):
    return ft.Container(
        bgcolor="#e6e6e6",
        border_radius=10,
        padding=ft.padding.symmetric(vertical=18, horizontal=24),
        margin=ft.margin.only(bottom=10, right=16),
        animate=ft.Animation(400, "easeOutQuad"),
        scale=ft.Scale(1.0),
        on_hover=animar_card_fn,
        content=ft.Row([
            ft.Icon(ft.Icons.EVENT, color="#8C1313", size=36),
            ft.Column([
                ft.Text("Próxima Jornada", weight="bold", color="#8C1313", size=18),
                ft.Text(nombre, weight="bold", color="#660924", size=16),
                ft.Text(f"Fecha: {fecha}", color="#145a7b", size=14),
                ft.Text(f"Ubicación: {ubicacion}", color="#348f50", size=14),
            ], spacing=2)
        ], spacing=18, alignment=ft.MainAxisAlignment.START)
    )

def main(page: ft.Page, navegar):
    page.title = "Cáritas San Cristóbal - Jornadas"
    page.window_width = 1000
    page.window_height = 700
    page.bgcolor = "white"
    page.padding = 0

    cherry = "#660924"
    wine = "#630D13"

    navbar = NavBar(page, navegar, cherry=cherry, wine=wine).view
    jornadas_controller = JornadasController()
    voluntarios_controller = VoluntariosController()
    jornadas = jornadas_controller.cargar_jornadas() or []

    # Crear carpeta 'reportes' si no existe
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
        ruta_pdf = os.path.join(REPORTES_DIR, 'jornadas_general.pdf')
        crear_pdf_listado_jornadas(ruta_pdf, jornadas)
        mostrar_exito_impresion(page, ruta_pdf)

    def mostrar_confirmacion_imprimir_general(e):
        mostrar_confirmacion_impresion(
            page,
            "¿Deseas imprimir el listado general de jornadas en PDF?",
            imprimir_general
        )

    def imprimir_individual(jornada):
        ruta_pdf = os.path.join(REPORTES_DIR, f'jornada_{jornada[0]}.pdf')
        voluntarios = jornadas_controller.obtener_voluntarios_por_jornada(jornada[0])
        recursos = jornadas_controller.obtener_detalles_jornada(jornada[0])
        observacion = recursos[0]["OBSERVACION"] if recursos and "OBSERVACION" in recursos[0] else ""
        crear_pdf_detalle_jornada(ruta_pdf, jornada, voluntarios, recursos, observacion)
        mostrar_exito_impresion(page, ruta_pdf)

    def mostrar_confirmacion_imprimir_individual(jornada):
        mostrar_confirmacion_impresion(
            page,
            f"¿Deseas imprimir el registro de la jornada '{jornada[2]}' en PDF?",
            lambda: imprimir_individual(jornada)
        )

    # Función para manejar la selección de fecha
    def seleccionar_fecha(e):
        if e.control.value:
            fecha_field.value = e.control.value.strftime("%d/%m/%Y")
            page.update()
            date_picker.open = False
            page.update()

    # Crear DatePicker
    date_picker = ft.DatePicker(
        first_date=datetime(year=2000, month=10, day=1),
        last_date=datetime(year=2025, month=10, day=1),
        on_change=seleccionar_fecha,
        on_dismiss=lambda e: page.update()
    )

    # Campo de fecha
    fecha_field = ft.TextField(
        label="Fecha",
        read_only=True,
        filled=True,
        prefix_icon=ft.Icons.CALENDAR_TODAY,
        bgcolor="#f9f9f9",
        border_color="#ccc",
        color="black",
        border_radius=8,
        label_style=ft.TextStyle(color="black"),
        width=410,
        hint_text="Haz click para seleccionar fecha",
        on_click=lambda e: page.open(date_picker)
    )

    descripcion_field = ft.TextField(
        label="Descripción", 
        hint_text="Descripción de la jornada",
        width=410, 
        multiline=True, 
        prefix_icon=ft.Icons.DESCRIPTION_ROUNDED,
        bgcolor="#f9f9f9",
        border_color="#ccc",
        color="black",
        border_radius=8,
        label_style=ft.TextStyle(color="black"),
    )
    
    ubicacion_field = ft.TextField(
        label="Ubicación",
        hint_text="Ejemplo: Calle 123, Ciudad",
        width=410, 
        multiline=True, 
        prefix_icon=ft.Icons.LOCATION_ON,
        bgcolor="#f9f9f9",
        border_color="#ccc",
        color="black",
        border_radius=8,
        label_style=ft.TextStyle(color="black"),
    )

    fecha_error = ft.Text("", color="red", size=12)
    descripcion_error = ft.Text("", color="red", size=12)
    ubicacion_error = ft.Text("", color="red", size=12)

    def validar_campos():
        errores = False

        if not fecha_field.value:
            fecha_error.value = "⚠️ Selecciona una fecha."
            errores = True
        else:
            fecha_error.value = ""

        if not descripcion_field.value.strip():
            descripcion_error.value = "⚠️ Ingresa una descripción."
            errores = True
        else:
            descripcion_error.value = ""

        if not ubicacion_field.value.strip():
            ubicacion_error.value = "⚠️ Ingresa una ubicación."
            errores = True
        else:
            ubicacion_error.value = ""

        page.update()
        return not errores

    def agregar_jornada(e):
        if not validar_campos():
            return

        try:
            fecha_obj = datetime.strptime(fecha_field.value, "%d/%m/%Y").date()
        except Exception as e:
            fecha_error.value = "⚠️ Formato de fecha inválido"
            page.update()
            return

        nueva_jornada = {
            "fecha": fecha_obj.strftime("%Y-%m-%d"),
            "descripcion": descripcion_field.value,
            "ubicacion": ubicacion_field.value,
        }
        if jornadas_controller.agregar_jornada(nueva_jornada):
            actualizar_lista_jornadas()  # <-- Esto refresca la lista
            limpiar_campos()
            cerrar_dialogo(page)
            page.update()
            mostrar_dialogo_exito(page, "Jornada agregada con éxito.")
   
        else:
            mostrar_dialogo_error(page, "No se pudo agregar la jornada.")
        page.update()


    def guardar_edicion(jornada):
        def _guardar(e):
            if not validar_campos():
                return

            try:
                fecha_obj = datetime.strptime(fecha_field.value, "%d/%m/%Y").date()
                fecha_mysql = fecha_obj.strftime("%Y-%m-%d")
            except Exception as e:
                fecha_error.value = "⚠️ Formato de fecha inválido"
                page.update()
                return
            
            jornada_actualizada = {
                "fecha": fecha_mysql,
                "descripcion": descripcion_field.value,
                "ubicacion": ubicacion_field.value,
            }

            jornada_id = jornada[0]
            if jornadas_controller.editar_jornada(jornada_id, jornada_actualizada):
                actualizar_lista_jornadas()
                limpiar_campos()
                cerrar_dialogo(page)
                mostrar_dialogo_exito(page, "Jornada actualizada con éxito.")
       
            else:
                mostrar_dialogo_error(page, "No se pudo actualizar la jornada.")
        return _guardar
        
    def eliminar_jornada(jornada):
        usuario = page.session.get("usuario")
        if not usuario or (not usuario.get("eliminar") and not usuario.get("total")):
            page.open(ft.SnackBar(content=ft.Text("No tiene permiso para eliminar jornadas"), action="OK", bgcolor="red"))
            return
        def on_confirmar():
            jornada_id = jornada[0]
            if jornadas_controller.eliminar_jornada(jornada_id):
                actualizar_lista_jornadas()
                mostrar_dialogo_exito(page, "Jornada eliminada con éxito.")
            else:
                mostrar_dialogo_error(page, "No se pudo eliminar la jornada.")
        mostrar_confirmacion(page, f"¿Estás seguro de que deseas eliminar la jornada '{jornada[2]}'?", on_confirmar)


    def limpiar_campos():
        fecha_field.value = ""
        descripcion_field.value = ""
        ubicacion_field.value = ""
        fecha_error.value = ""
        descripcion_error.value = ""
        ubicacion_error.value = ""
        page.update()

    def crear_boton_editar(jornada):
        return ft.IconButton(icon=ft.Icons.EDIT,icon_color=cherry, on_click=lambda e: abrir_dialogo(jornada))

    def crear_boton_eliminar(jornada):
        return ft.IconButton(icon=ft.Icons.DELETE,icon_color=cherry, on_click=lambda e: eliminar_jornada(jornada))

    def crear_boton_voluntarios(jornada):
        return ft.IconButton(icon=ft.Icons.PEOPLE,icon_color=cherry, on_click=lambda e: abrir_dialogo_voluntarios(jornada))

    def crear_boton_completar(jornada):
        color = "green" if jornada[4] == "COMPLETADA" else cherry
        return ft.IconButton(
            icon=ft.Icons.CHECK,
            icon_color=color,
            on_click=lambda e: abrir_dialogo_completar(jornada)
        )

    def crear_lista_jornadas(jornadas):
        return ft.Column(
            controls=[
                ft.Divider(height=1, color="#e0e0e0"), 
                ft.Container(
                    bgcolor="#e6e6e6",
                    expand=True,
                    content=ft.Row([
                        ft.Text("Descripcion de Jornada", weight="bold", color=cherry, width=300),
                        ft.Text("Fecha", weight="bold", color=cherry, width=200),
                        ft.Text("Ubicacion", weight="bold", color=cherry, width=200),
                        ft.Text("Estatus", weight="bold", color=cherry, width=150),
                        ft.Text("Voluntarios", weight="bold", color=cherry, width=200),
                        ft.Text("Acciones", weight="bold", color=cherry, width=100),
                    ], alignment=ft.MainAxisAlignment.START, spacing=5),
                ),
                ft.Divider(height=1, color="#e0e0e0"), 
            ] + [
                ft.Container(
                    content=ft.Row([
                        ft.Container(ft.Text(j[2], color="black"), width=300),  
                        ft.Container(ft.Text(j[1], color="black"), width=200),  
                        ft.Container(ft.Text(j[3], color="black"), width=200), 
                        ft.Container(ft.Text(j[4], color="black"), width=150),  
                        ft.Container(ft.Text("3", color="black"), width=120),  
                        ft.Row([
                            crear_boton_editar(j),  
                            crear_boton_eliminar(j),  
                            crear_boton_voluntarios(j),
                            crear_boton_completar(j),
                            ft.IconButton(
                                icon=ft.Icons.PICTURE_AS_PDF,
                                tooltip="Imprimir registro",
                                on_click=lambda e, j=j: mostrar_confirmacion_imprimir_individual(j),
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
                for j in jornadas
            ],
            spacing=5,
        )

    lista_jornadas = ft.ListView(
        controls=crear_lista_jornadas(jornadas).controls,
        expand=True,
        spacing=0,
        padding=0,
        auto_scroll=False
    )

    def actualizar_lista_jornadas():
        global jornadas
        jornadas = jornadas_controller.cargar_jornadas()
        lista_jornadas.controls = crear_lista_jornadas(jornadas).controls
        lista_jornadas.update()

    

    search_field = ft.TextField(
        hint_text='Buscar Jornada',
        filled=True,
        width=400,
        border_color=ft.Colors.TRANSPARENT, 
        prefix_icon=ft.Icons.SEARCH,
        bgcolor=ft.Colors.WHITE,
        color=cherry,  
        on_change=lambda e: filtrar_jornadas(e.control.value)
    )

    def filtrar_jornadas(query):
        query = query.lower()
        filtrados = [v for v in jornadas if query in v[4].lower() or query in v[2].lower() or query in v[3].lower()] 
        lista_jornadas.controls = crear_lista_jornadas(filtrados).controls
        page.update()

    dialog = ft.AlertDialog(
        modal=False,
        bgcolor="white",
        title=ft.Text("Agregar Nueva Jornada"),
        content=ft.Container(
            content=ft.Column([
                ft.Column([fecha_error, fecha_field]),
                ft.Column([descripcion_error, descripcion_field]),
                ft.Column([ubicacion_error, ubicacion_field]),
            ], spacing=5),
            padding=10,
            width=400,
            height=300
        ),
        actions=[
            ft.TextButton("Cancelar",on_click=lambda e: cerrar_dialogo(page)),
            ft.ElevatedButton("Agregar", on_click=agregar_jornada, bgcolor="white", color=cherry, style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                side=ft.BorderSide(1, cherry),
                bgcolor={"": "white", "hovered": "#f5f5f5"},
                color={"": cherry, "hovered": wine}
            ))
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )
    page.dialog = dialog

    def abrir_dialogo(jornada=None):
        usuario = page.session.get("usuario")
        if jornada:
            # Validar permiso antes de abrir el diálogo de editar
            if not usuario or (not usuario.get("modificar") and not usuario.get("total")):
                page.open(ft.SnackBar(content=ft.Text("No tiene permiso para editar jornadas"), action="OK", bgcolor="red"))
                return
            dialog.title = ft.Text(
                "Editar Jornada",
                size=22,
                weight="bold",
                color=cherry,
                expand=True
            )
            try:
                fecha_mysql = jornada[1]
                fecha_obj = datetime.strptime(fecha_mysql, "%Y-%m-%d").date() if isinstance(fecha_mysql, str) else fecha_mysql
                fecha_field.value = fecha_obj.strftime("%d/%m/%Y")
            except Exception as e:
                print(f"Error al formatear fecha: {e}")
                fecha_field.value = ""
                
            descripcion_field.value = jornada[2]  
            ubicacion_field.value = jornada[3]  
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
                    on_click=guardar_edicion(jornada),
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
                page.open(ft.SnackBar(content=ft.Text("No tiene permiso para agregar jornadas"), action="OK", bgcolor="red"))
                return
            dialog.title = ft.Text(
                "Nueva Jornada",
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
                    on_click=agregar_jornada,
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

    # Diálogo para seleccionar voluntarios
    dialog_voluntarios = ft.AlertDialog(
        modal=False,
        bgcolor="white",
        title=ft.Text(
            "Seleccionar Voluntarios",
            size=22,
            weight="bold",
            color=cherry,
            expand=True
        ),
        content=ft.ListView(
            controls=[],
            spacing=10,
            padding=10,
            width=400,
            height=300,
            auto_scroll=True
        ),
        actions=[
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
                on_click=lambda e: guardar_voluntarios(jornada),
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

    selected_voluntarios = []

    def abrir_dialogo_voluntarios(jornada):
        voluntarios = voluntarios_controller.cargar_voluntarios()
        voluntarios_asociados = jornadas_controller.obtener_voluntarios_por_jornada(jornada[0])
        
        selected_voluntarios.clear()
        selected_voluntarios.extend([v[0] for v in voluntarios_asociados])
        
        dialog_voluntarios.content = crear_lista_voluntarios(voluntarios, jornada)
        
        dialog_voluntarios.actions = [
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
                on_click=lambda e: guardar_voluntarios(jornada),
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
        
        page.dialog = dialog_voluntarios
        page.open(dialog_voluntarios)
        page.update()

    def crear_lista_voluntarios(voluntarios, jornada):
        controles = [
            ft.Row([
                ft.Text("Nombre", weight="bold", color=cherry, width=150),
                ft.Text("Disponibilidad", weight="bold", color=cherry, width=200),
                ft.Text("Seleccionar", weight="bold", color=cherry, width=100),
            ], alignment=ft.MainAxisAlignment.START)
        ]
        
        controles.extend([
            ft.Row([
                ft.Container(ft.Text(v[1], color="black"), width=150),
                ft.Container(ft.Text(v[5], color="black"), width=200),
                ft.Container(
                    content=ft.Checkbox(
                        value=v[0] in selected_voluntarios,
                        on_change=lambda e, id=v[0]: seleccionar_voluntario(id)
                    ),
                    width=100
                )
            ], alignment=ft.MainAxisAlignment.START, spacing=5)
            for v in voluntarios
        ])
        
        return ft.ListView(
            controls=controles,
            spacing=5,
            padding=10,
            height=400,
            width=500,
            auto_scroll=True
        )

    def seleccionar_voluntario(voluntario_id):
        if voluntario_id in selected_voluntarios:
            selected_voluntarios.remove(voluntario_id)
        else:
            selected_voluntarios.append(voluntario_id)
        page.update()

    def guardar_voluntarios(jornada):
        exito = True
        jornadas_controller.limpiar_voluntarios_jornada(jornada[0])
        for voluntario_id in selected_voluntarios:
            if not jornadas_controller.guardar_voluntarios(voluntario_id, jornada[0]):
                exito = False
        selected_voluntarios.clear()
        cerrar_dialogo(page)
        page.update()
        if exito:
            mostrar_dialogo_exito(page, "Voluntarios agregados con éxito.")
        else:
            mostrar_dialogo_error(page, "No se pudieron agregar todos los voluntarios.")


    # ...dentro de la función abrir_dialogo_completar(jornada):
    error_msg = ft.Text("", color="red", size=12)
    def abrir_dialogo_completar(jornada):
        # 1. Obtener recursos disponibles agrupados por tipo
        recursos = jornadas_controller.obtener_recursos_disponibles()  # Debe retornar una lista de dicts con: tipo, descripcion, cantidad_disponible, id_detalle

        # Agrupar recursos por tipo
        recursos_por_tipo = {"Monetaria": [], "Alimentos": [], "Medicamentos": []}
        for r in recursos:
            recursos_por_tipo.get(r["tipo"], []).append(r)

        # Estado para los controles dinámicos
        recursos_rows = ft.Column([], spacing=5)

        def recursos_disponibles_para_tipo(tipo, exclude_row=None):
            seleccionados = set()
            for row in recursos_rows.controls:
                if row is exclude_row:
                    continue
                recurso_id = row.controls[1].value  # recurso_dropdown
                if row.controls[0].value == tipo and recurso_id:
                    seleccionados.add(int(recurso_id))
            return [r for r in recursos_por_tipo.get(tipo, []) if r["id_detalle"] not in seleccionados]

        comentarios_field = ft.TextField(
            label="Observación",
            multiline=True,
            width=700,
            bgcolor="#f9f9f9",
            border_color="#ccc",
            color="black",
            border_radius=8,
            label_style=ft.TextStyle(color="black"),
        )

        detalles_guardados = []
        if (jornada[4] == 'COMPLETADA'):
            detalles_guardados = jornadas_controller.obtener_detalles_jornada(jornada[0])
            print("DETALLES GUARDADOS:", detalles_guardados)
            # Precarga la observación general (toma la del primer detalle, o ajústalo según tu modelo)
            if detalles_guardados and "OBSERVACION" in detalles_guardados[0]:
                comentarios_field.value = detalles_guardados[0]["OBSERVACION"]
            else:
                comentarios_field.value = ""
        else:
            comentarios_field.value = ""
        
        recursos_header = ft.Row([
            ft.Text("Tipo", weight="bold", width=150, color=cherry),
            ft.Text("Recurso", weight="bold", width=140,color=cherry),
            ft.Text("Utilizado", weight="bold", width=80,color=cherry),
            ft.Container(width=40)  # espacio para el botón eliminar
        ], spacing=10)

        # 
        def crear_row_recurso(tipo=None, recurso_id=None, disponible=None, utilizado=None, descripcion=None):
            def on_tipo_change(e, recurso_dropdown, cantidad_field, row_ref=None):
                tipo_actual = e.control.value
                disponibles = recursos_disponibles_para_tipo(tipo_actual, exclude_row=row_ref)
                options = [ft.dropdown.Option(str(r["id_detalle"]), r["descripcion"]) for r in disponibles]

                # Si estamos editando y el recurso_id no está en disponibles, lo agregamos
                if recurso_id and tipo_actual == tipo:
                    if not any(str(r["id_detalle"]) == str(recurso_id) for r in disponibles):
                        desc = descripcion or ""
                        if not desc and detalles_guardados:
                            desc = next(
                                (d.get("DESCRIPCION", "") for d in detalles_guardados if str(d.get("ID_DETALLE_DONACION")) == str(recurso_id)),
                                ""
                            )
                        if not desc:
                            desc = next(
                                (r["descripcion"] for r in recursos_por_tipo.get(tipo_actual, []) if str(r["id_detalle"]) == str(recurso_id)),
                                str(recurso_id)
                            )
                        options.append(ft.dropdown.Option(str(recurso_id), desc))
                recurso_dropdown.options = options

                # Selecciona el recurso si corresponde
                if recurso_id and tipo_actual == tipo:
                    recurso_dropdown.value = str(recurso_id)
                else:
                    recurso_dropdown.value = None

                # Actualiza hint de cantidad_field con el disponible SOLO si ya está en la página
                disponible_val = ""
                if recurso_dropdown.value:
                    recurso = next((r for r in recursos_por_tipo.get(tipo_actual, []) if str(r["id_detalle"]) == recurso_dropdown.value), None)
                    if recurso:
                        disponible_val = str(recurso["cantidad_disponible"])
                    elif disponible is not None:
                        disponible_val = str(disponible)
                elif disponible is not None:
                    disponible_val = str(disponible)
                cantidad_field.hint_text = f"Disponible: {disponible_val}" if disponible_val else ""

                # Solo actualiza si ya está en la página (evento real)
                if hasattr(recurso_dropdown, "update") and hasattr(cantidad_field, "update"):
                    recurso_dropdown.hint_text = "" if options else "No hay más insumos disponibles"
                    recurso_dropdown.disabled = not bool(options)
                    recurso_dropdown.update()
                    cantidad_field.update()

            def on_recurso_change(e, selected_tipo, cantidad_field):
                tipo_actual = selected_tipo.value
                try:
                    recurso_id_val = int(e.control.value)
                except Exception:
                    return
                recurso = next((r for r in recursos_por_tipo.get(tipo_actual, []) if r["id_detalle"] == recurso_id_val), None)
                disponible_val = ""
                if recurso:
                    disponible_val = str(recurso["cantidad_disponible"])
                cantidad_field.hint_text = f"Disponible: {disponible_val}" if disponible_val else ""
                if hasattr(cantidad_field, "update"):
                    cantidad_field.update()

            def eliminar_row(e):
                recursos_rows.controls.remove(row)
                recursos_rows.update()
                # Refresca los dropdowns de las otras filas para que el recurso vuelva a estar disponible
                for other_row in recursos_rows.controls:
                    tipo_val = other_row.controls[0].value
                    on_tipo_change(
                        type("e", (), {"control": type("c", (), {"value": tipo_val})()})(),
                        other_row.controls[1],
                        other_row.controls[2],
                        other_row
                    )

            selected_tipo = ft.Dropdown(
                label=None,
                options=[
                    ft.dropdown.Option("Monetaria", "Monetaria"),
                    ft.dropdown.Option("Alimentos", "Alimentos"),
                    ft.dropdown.Option("Medicamentos", "Medicamentos"),
                ],
                width=150,
                color="black",
                text_size=12,
                bgcolor="white",
                border_color="#cccccc",
                border_radius=4,
                on_change=None  # Se asigna después de crear row
            )
            recurso_dropdown = ft.Dropdown(
                label=None,
                options=[],
                width=140,
                color="black",
                text_size=12,
                bgcolor="white",
                border_color="#cccccc",
                border_radius=4,
                on_change=None  # Se asigna después de crear row
            )
            cantidad_field = ft.TextField(
                label=None,
                value=str(utilizado) if utilizado is not None else "",
                width=120,
                color="black",
                text_size=12 ,
                border_color="#cccccc",
                bgcolor="white"
            )

            eliminar_btn = ft.IconButton(
                icon=ft.Icons.DELETE,
                icon_color="red",
                tooltip="Eliminar este recurso",
                on_click=eliminar_row
            )

            row = ft.Row([
                selected_tipo,
                recurso_dropdown,
                cantidad_field,
                eliminar_btn
            ], spacing=10)

            # Asigna handlers después de crear row para pasar la referencia correcta
            selected_tipo.on_change = lambda e: on_tipo_change(e, recurso_dropdown, cantidad_field, row)
            recurso_dropdown.on_change = lambda e: on_recurso_change(e, selected_tipo, cantidad_field)

            # Precarga valores si existen (NO LLAMIES update aquí)
            if tipo:
                selected_tipo.value = tipo
            if recurso_id:
                recurso_dropdown.value = str(recurso_id)

            # POBLA LAS OPCIONES Y HINTS SIN LLAMAR .update()
            tipo_actual = tipo or ""
            disponibles = recursos_disponibles_para_tipo(tipo_actual)
            options = [ft.dropdown.Option(str(r["id_detalle"]), r["descripcion"]) for r in disponibles]

            if recurso_id and tipo_actual:
                if not any(str(r["id_detalle"]) == str(recurso_id) for r in disponibles):
                    desc = descripcion or ""
                    if not desc and detalles_guardados:
                        desc = next(
                            (d.get("DESCRIPCION", "") for d in detalles_guardados if str(d.get("ID_DETALLE_DONACION")) == str(recurso_id)),
                            ""
                        )
                    if not desc:
                        desc = next(
                            (r["descripcion"] for r in recursos_por_tipo.get(tipo_actual, []) if str(r["id_detalle"]) == str(recurso_id)),
                            str(recurso_id)
                        )
                    options.append(ft.dropdown.Option(str(recurso_id), desc))
            recurso_dropdown.options = options

            # Selecciona el recurso si corresponde
            if recurso_id and tipo_actual:
                recurso_dropdown.value = str(recurso_id)
            else:
                recurso_dropdown.value = None

            # Actualiza hint de cantidad_field con el disponible (sin update)
            disponible_val = ""
            if recurso_dropdown.value:
                recurso = next((r for r in recursos_por_tipo.get(tipo_actual, []) if str(r["id_detalle"]) == recurso_dropdown.value), None)
                if recurso:
                    disponible_val = str(recurso["cantidad_disponible"])
                elif disponible is not None:
                    disponible_val = str(disponible)
            elif disponible is not None:
                disponible_val = str(disponible)
            cantidad_field.hint_text = f"Disponible: {disponible_val}" if disponible_val else ""

            return row
        # --- Precarga filas de recursos ---
        recursos_rows.controls = []
        if detalles_guardados:
            for det in detalles_guardados:
                recursos_rows.controls.append(
                    crear_row_recurso(
                        tipo=det.get("TIPO"),
                        recurso_id=det.get("ID_DETALLE_DONACION"),
                        disponible=det.get("CANTIDAD_DISPONIBLE"),
                        utilizado=det.get("CANTIDAD_UTILIZADA"),
                        descripcion=det.get("DESCRIPCION")
                    )
                )
        else:
            recursos_rows.controls = [crear_row_recurso()]
        # Precarga filas de recursos si hay detalles guardados
        recursos_rows.controls = []
        if detalles_guardados:
            for det in detalles_guardados:
                recursos_rows.controls.append(
                    crear_row_recurso(
                        tipo=det.get("TIPO"),
                        recurso_id=det.get("ID_DETALLE_DONACION"),
                        disponible=det.get("CANTIDAD_DISPONIBLE"),
                        utilizado=det.get("CANTIDAD_UTILIZADA"),
                        descripcion=det.get("DESCRIPCION")
                    )
                )
        else:
            recursos_rows.controls = [crear_row_recurso()]

        def agregar_row_recurso(e):
            recursos_rows.controls.append(crear_row_recurso())
            recursos_rows.update()

        btn_agregar_recurso = ft.IconButton(icon=ft.Icons.ADD, on_click=agregar_row_recurso)



        # Obtener voluntarios asociados a la jornada
                # Obtener voluntarios asociados a la jornada
        voluntarios_asociados = jornadas_controller.obtener_voluntarios_por_jornada(jornada[0])
        voluntarios_participacion = []


        voluntarios_header = ft.Row([
            ft.Text("Voluntario", weight="bold", width=200, color=cherry),
            ft.Text("Horas", weight="bold", width=80, color=cherry),
            ft.Text("Participó", weight="bold", width=90, color=cherry),
        ], spacing=10)

        voluntarios_column_controls = []
        for voluntario in voluntarios_asociados:
            nombre = ft.Text(voluntario[1], width=200, color="black")
            horas_field = ft.TextField(
                label=None,
                width=80,
                color="black",
                border_color="#cccccc",
                bgcolor="white",
                border_radius=4,
                value=str(voluntario[3]) if voluntario[3] else "",
                disabled=not bool(voluntario[2]),
                keyboard_type="number"
            )
            cb = ft.Checkbox(value=bool(voluntario[2]))  # <-- sin width aquí

            def on_cb_change(e, horas_field=horas_field):
                horas_field.disabled = not e.control.value
                if not e.control.value:
                    horas_field.value = ""
                horas_field.update()

            cb.on_change = on_cb_change
            voluntarios_participacion.append((voluntario[0], cb, horas_field))
            voluntarios_column_controls.append(
                ft.Row([nombre, horas_field, cb], spacing=10)
            )

        voluntarios_column = ft.Column(
            [voluntarios_header] + voluntarios_column_controls,
            spacing=5
        )
        # Contenido del diálogo
        recursos_section = ft.Container(
            content=ft.Column([
                ft.Text("Recursos Utilizados:", weight="bold", color=cherry),
                error_msg,
                recursos_header,
                recursos_rows,
                btn_agregar_recurso,
                
            ], spacing=6, scroll=ft.ScrollMode.AUTO),
            height=230,
            bgcolor="#f7f7f7",
            border_radius=8,
            padding=10,
            expand=False
        )

        voluntarios_section = ft.Container(
            content=ft.Column([
                ft.Text("Participación Voluntarios:", weight="bold", color=cherry),
                voluntarios_column
            ], scroll=ft.ScrollMode.AUTO),
            height=180,
            bgcolor="#f7f7f7",
            border_radius=8,
            padding=10,
            expand=False
        )

        # Checkbox para marcar como completada
        completada_checkbox = ft.Checkbox(
            label="Jornada completada",
            value=(jornada[4] == 'COMPLETADA'),
            on_change=None  # Se asigna después
        )

        contenido = ft.Container(
            content=ft.Column([
                voluntarios_section,
                recursos_section,
                completada_checkbox,
                comentarios_field,
            ], spacing=10),
            width=520,
            height=500,
            padding=10
        )

        # Acción al completar jornada
        def completar_jornada_action(e):
            recursos_a_guardar = []
            error_msg.value = ""  # Limpia el mensaje de error

            # Guardar recursos de alimentos/medicamentos
            for row in recursos_rows.controls:
                tipo = row.controls[0].value
                recurso_id = row.controls[1].value
                cantidad_utilizada = row.controls[2].value  # Solo una casilla ahora

                # Buscar la descripción de forma segura
                descripcion = ""
                if recurso_id:
                    opciones_keys = [opt.key for opt in row.controls[1].options]
                    if recurso_id in opciones_keys:
                        descripcion = row.controls[1].options[opciones_keys.index(recurso_id)].text
                    else:
                        descripcion = next(
                            (r["descripcion"] for r in recursos_por_tipo.get(tipo, []) if str(r["id_detalle"]) == str(recurso_id)),
                            ""
                        )
                        if not descripcion and detalles_guardados:
                            descripcion = next(
                                (d.get("DESCRIPCION", "") for d in detalles_guardados if str(d.get("ID_DETALLE_DONACION")) == str(recurso_id)),
                                ""
                            )

                # Buscar el disponible real
                disponible = None
                recurso = next((r for r in recursos_por_tipo.get(tipo, []) if str(r["id_detalle"]) == str(recurso_id)), None)
                if recurso:
                    disponible = float(recurso["cantidad_disponible"])
                elif detalles_guardados:
                    disponible = float(next(
                        (d.get("CANTIDAD_DISPONIBLE", 0) for d in detalles_guardados if str(d.get("ID_DETALLE_DONACION")) == str(recurso_id)),
                        0
                    ))

                if tipo and recurso_id and cantidad_utilizada:
                    try:
                        cantidad_utilizada = float(cantidad_utilizada)
                        if disponible is not None and cantidad_utilizada > 0 and cantidad_utilizada <= disponible:
                            recursos_a_guardar.append({
                                "tipo": tipo,
                                "descripcion": descripcion,
                                "cantidad_utilizada": cantidad_utilizada,
                                "id_detalle": int(recurso_id)
                            })
                        else:
                            error_msg.value = f"Cantidad utilizada ({cantidad_utilizada}) no puede ser mayor que disponible ({disponible})"
                            page.update()
                            return
                    except ValueError:
                        error_msg.value = "La cantidad utilizada debe ser un número válido."
                        page.update()
                        return

            # Elimina detalles previos
            jornadas_controller.eliminar_detalles_jornada(jornada[0])

            # Inserta los nuevos detalles
            for recurso in recursos_a_guardar:
                jornadas_controller.insertar_jornada_detalle(
                    jornada_id=jornada[0],
                    recurso_utilizado=recurso["descripcion"],
                    cantidad_utilizada=recurso["cantidad_utilizada"],
                    id_detalle=recurso["id_detalle"]
                )

            # Guardar voluntarios participantes
            voluntarios_participantes = []
            voluntarios_horas = {}
            for voluntario_id, cb, horas_field in voluntarios_participacion:
                if cb.value:
                    voluntarios_participantes.append(voluntario_id)
                    try:
                        horas = float(horas_field.value)
                    except Exception:
                        horas = 0
                    voluntarios_horas[voluntario_id] = horas

            # Actualiza la participación y horas
            resultado = jornadas_controller.completar_jornada(
                    jornada[0],
                    recursos_a_guardar,
                    comentarios_field.value,
                    voluntarios_participantes,
                    voluntarios_horas
                )
            # Actualiza el estado de completada en la base de datos
            if completada_checkbox.value:
                jornadas_controller.marcar_jornada_completada(jornada[0], comentarios_field.value)
            else:
                jornadas_controller.marcar_jornada_no_completada(jornada[0])
            actualizar_lista_jornadas()
            cerrar_dialogo(page)
            if resultado:
                mostrar_dialogo_exito(page, "Jornada completada con éxito.")
            else:
                mostrar_dialogo_error(page, "No se pudo completar la jornada.")

        # Crear el diálogo
        dialog_completar = ft.AlertDialog(
            modal=False,
            bgcolor="white",
            title=ft.Text("Completar Jornada", size=22, weight="bold", color="#660924"),
            content=contenido,
            actions=[
                ft.ElevatedButton(
                    "Cancelar",
                    on_click=lambda e: cerrar_dialogo(page),
                    bgcolor="white",
                    color="#660924",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        side=ft.BorderSide(1, "#660924"),
                        bgcolor={"": "white", "hovered": "#f5f5f5"},
                        color={"": "#660924", "hovered": "#630D13"}
                    )
                ),
                ft.ElevatedButton(
                    "Completar",
                    on_click=completar_jornada_action,
                    bgcolor="#630D13",
                    color="white",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                    )
                )
            ]
        )

        page.dialog = dialog_completar
        page.open(dialog_completar)
        page.update()

    jornadas_realizadas_card = crear_estadisticas_card_jornadas(
        "Jornadas Realizadas",
        str(len(jornadas)),  # O el valor que corresponda
        ft.Icons.EVENT,
        "#660924",
        animar_card
    )

    hoy = date.today()
    proxima = None
    for j in jornadas:
        try:
            fecha_jornada = j[1]
            if isinstance(fecha_jornada, str):
                fecha_jornada = datetime.strptime(fecha_jornada, "%Y-%m-%d").date()
            if fecha_jornada >= hoy:
                if not proxima or fecha_jornada < proxima["fecha"]:
                    proxima = {
                        "nombre": j[2],           # Descripción o nombre
                        "fecha": fecha_jornada,
                        "ubicacion": j[3]         # Ubicación
                    }
        except Exception:
            continue

    if proxima:
        proxima_jornada_card = crear_proxima_jornada_card(
            proxima["nombre"],
            proxima["fecha"].strftime("%d/%m/%Y"),
            proxima["ubicacion"],
            animar_card_fn=animar_card
        )
    else:
        proxima_jornada_card = crear_proxima_jornada_card(
            "No hay próximas jornadas",
            "",
            "",
            animar_card_fn=animar_card
        )

    jornadas_realizadas_card = crear_estadisticas_card_jornadas(
        "Jornadas Realizadas",
        str(len(jornadas)),
        ft.Icons.EVENT,
        "#660924",
        animar_card
    )

    def abrir_calendario_personalizado(page, jornadas, mes=None, anio=None):
        from calendar import monthrange
        hoy = datetime.now().date()
        if mes is None:
            mes = hoy.month
        if anio is None:
            anio = hoy.year

        jornadas_por_fecha = {}
        for j in jornadas:
            try:
                fecha_jornada = j[1]
                if isinstance(fecha_jornada, str):
                    fecha_jornada = datetime.strptime(fecha_jornada, "%Y-%m-%d").date()
                if fecha_jornada >= hoy:
                    jornadas_por_fecha[fecha_jornada] = j
            except Exception:
                continue

        primer_dia_semana, dias_mes = monthrange(anio, mes)
        dias_grid = []
        for _ in range(primer_dia_semana):
            dias_grid.append(ft.Container(width=36, height=36))
        for dia in range(1, dias_mes + 1):
            fecha = date(anio, mes, dia)
            jornada = jornadas_por_fecha.get(fecha)
            if jornada:
                dias_grid.append(
                    ft.Container(
                        width=36,
                        height=36,
                        bgcolor="#ffe0e0",
                        border_radius=18,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text(str(dia), weight="bold", color="#8C1313"),
                            ft.Icon(ft.Icons.FIBER_MANUAL_RECORD, color="#8C1313", size=12)
                        ], spacing=0, alignment=ft.MainAxisAlignment.CENTER),
                        on_click=lambda e, j=jornada: mostrar_detalle_jornada(page, j)
                    )
                )
            else:
                dias_grid.append(
                    ft.Container(
                        width=36,
                        height=36,
                        bgcolor="white",
                        border_radius=18,
                        alignment=ft.alignment.center,
                        content=ft.Text(str(dia), color="black")
                    )
                )

        def cambiar_mes(delta):
            nuevo_mes = mes + delta
            nuevo_anio = anio
            if nuevo_mes < 1:
                nuevo_mes = 12
                nuevo_anio -= 1
            elif nuevo_mes > 12:
                nuevo_mes = 1
                nuevo_anio += 1
            abrir_calendario_personalizado(page, jornadas, nuevo_mes, nuevo_anio)

        calendario = ft.Container(
            bgcolor="white",
            border_radius=12,
            padding=20,
            height=280,
            content=ft.Column([
                ft.Row([
                    ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: cambiar_mes(-1)),
                    ft.Text(f"{date(anio, mes, 1).strftime('%B %Y')}", size=18, weight="bold", color="#660924"),
                    ft.IconButton(ft.Icons.ARROW_FORWARD, on_click=lambda e: cambiar_mes(1)),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(
                    [ft.Text(d, weight="bold", color="#8C1313", width=36, text_align="center") for d in ["L", "M", "M", "J", "V", "S", "D"]],
                    spacing=0
                ),
                ft.GridView(
                    controls=dias_grid,
                    runs_count=7,
                    max_extent=36,
                    child_aspect_ratio=1.0,
                    spacing=0,
                    run_spacing=0,
                    expand=False,
                    width=7*36
                ),
                ft.Divider(height=10, color="transparent"),
                ft.Text("Haz clic en un día con punto para ver detalles de la jornada.", size=12, color="#888")
            ], spacing=8)
        )

        dialogo_calendario = ft.AlertDialog(
            modal=True,
            bgcolor="white",
            content=calendario,
            actions=[ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo(page))],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.dialog = dialogo_calendario
        page.open(dialogo_calendario)
        page.update()

    def mostrar_detalle_jornada(page, jornada):
        detalle = ft.AlertDialog(
            modal=True,
            bgcolor="white",
            title=ft.Text("Detalle de Jornada", weight="bold", color="#660924"),
            content=ft.Column([
                ft.Text(f"Nombre: {jornada[2]}", color="#8C1313"),
                ft.Text(f"Fecha: {jornada[1]}", color="#145a7b"),
                ft.Text(f"Ubicación: {jornada[3]}", color="#348f50"),
                ft.Text(f"Estatus: {jornada[4]}", color="#888"),
            ], spacing=4, height=160),
            actions=[ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo(page))],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.dialog = detalle
        page.open(detalle)
        page.update()

    main_layout = ft.Container(
        ft.Column([
            # Encabezado
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text("Jornadas", color=cherry, size=24, weight="bold"),
                        ft.FloatingActionButton(icon=ft.Icons.ADD, bgcolor=wine, on_click=lambda e: abrir_dialogo()),
                        ft.Container(content=search_field, expand=True),
                        ft.IconButton(
                            icon=ft.Icons.PICTURE_AS_PDF,
                            tooltip="Imprimir listado general",
                            on_click=mostrar_confirmacion_imprimir_general,
                            icon_color=cherry
                        ),
                        ft.Text(str(date.today()), weight="bold", color=cherry),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                padding=ft.padding.only(top=40, left=0, right=0, bottom=10),
            ),
            # Lista scrolleable de jornadas
            ft.Container(
                content=lista_jornadas,
                expand=True,
                bgcolor="#fff",
                border_radius=8,
                padding=0,
                height=420
            ),
            # Tarjeta Jornadas Realizadas al final
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.Icons.CALENDAR_TODAY, color="white"),
                                ft.Text("Ver Calendario", color="white", weight="bold")
                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                            bgcolor="#660924",
                            border_radius=10,
                            padding=ft.padding.symmetric(vertical=12, horizontal=24),
                            on_click=lambda e: abrir_calendario_personalizado(page, jornadas),
                            ink=True,
                            animate=ft.Animation(400, "easeOutQuad"),
                            width=200,
                            height=50,
                            alignment=ft.alignment.center,
                            scale=ft.Scale(1.0),
                            on_hover=animar_card
                        ),
                        proxima_jornada_card,
                        jornadas_realizadas_card
                    ],
                    alignment=ft.MainAxisAlignment.END,  # <-- Cambia START por END aquí
                    spacing=20
                ),
                alignment=ft.alignment.bottom_right,  # <-- Esto ya está bien
                margin=ft.margin.only(left=0, bottom=30, top=20, right=0)
            )
        ], spacing=20),
        padding=ft.Padding(left=32, right=32, top=24, bottom=24)
    )

    page.add(
        ft.Row(
            controls=[navbar, ft.Container(content=main_layout, expand=True)],
            expand=True
        )
    )