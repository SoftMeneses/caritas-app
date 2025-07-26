import flet as ft
from datetime import date
import datetime 
from controllers.donaciones_controller import DonacionesController
from controllers.donantes_controller import DonantesController
from views.navbar import NavBar
from utils.impresion import (
    crear_pdf_blanco,
    mostrar_confirmacion_impresion,
    mostrar_exito_impresion,
    crear_pdf_listado_donaciones,
    crear_pdf_detalle_donacion
)
from utils.dialogos import mostrar_dialogo_exito, mostrar_dialogo_error, mostrar_confirmacion, cerrar_dialogo
import os


def crear_estadisticas_card_donaciones(titulo, valor, icono, color, animar_card_fn):
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
    page.title = "Cáritas San Cristóbal - Donaciones"
    page.window_width = 900
    page.window_height = 600
    page.window_resizable = True
    page.bgcolor = "white"
    page.padding = 0

    cherry = "#660924"
    wine = "#630D13"
    donaciones = []

    navbar = NavBar(page, navegar, cherry=cherry, wine=wine).view
    fecha = date.today()
    controller = DonantesController()
    controllerDonaciones = DonacionesController()

    donantes = controller.cargar_donantes() 
    if donantes is None:
        donantes = [] 

    donaciones = controllerDonaciones.cargar_donaciones() 
    if donaciones is None:
        donaciones = []
         

    def animar_card(e):
        if e.data == "true":
            e.control.scale = ft.Scale(1.05)
            e.control.bgcolor = ft.Colors.with_opacity(0.9, e.control.bgcolor)
        else:
            e.control.scale = ft.Scale(1.0)
            e.control.bgcolor = ft.Colors.with_opacity(1.0, e.control.bgcolor)
        e.control.update()


    def animar_fila(e):
        if e.data == "true":
            e.control.scale = ft.Scale(1.02)
            e.control.bgcolor = "#fbe9ee"  # <-- Color vino claro para hover
        else:
            e.control.scale = ft.Scale(1.0)
            e.control.bgcolor = "#fff"
        e.control.update()

    def filtrar_donaciones(query):
        query = query.lower()
        filtradas = [
            d for d in donaciones
            if query in str(d['NOMBRE']).lower()
            or query in str(d['DESCRI']).lower()
            or query in str(d['FECHA']).lower()
        ]
        lista_donaciones_lv.controls = crear_lista_donaciones(filtradas).controls
        page.update()

    busqueda_input = ft.TextField(
        label="Buscar donación",
        filled=True,
        width=400,
        border_color=ft.Colors.TRANSPARENT, 
        prefix_icon=ft.Icons.SEARCH,
        bgcolor=ft.Colors.WHITE,
        color=cherry,
        on_change=lambda e: filtrar_donaciones(e.control.value)
    )

    # ...dentro de main()...
    # Carpeta de reportes en la raíz del proyecto
    REPORTES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'reportes')
    
    if not os.path.exists(REPORTES_DIR):
        os.makedirs(REPORTES_DIR)

    def imprimir_general():
        ruta_pdf = os.path.join(REPORTES_DIR, 'donaciones_general.pdf')
        crear_pdf_listado_donaciones(ruta_pdf, donaciones)
        mostrar_exito_impresion(page, ruta_pdf)

    def imprimir_individual(donacion):
        nombre = str(donacion['NOMBRE']).replace(' ', '_')
        fecha = str(donacion['FECHA'])
        ruta_pdf = os.path.join(REPORTES_DIR, f'donacion_{nombre}_{fecha}.pdf')
        crear_pdf_detalle_donacion(ruta_pdf, donacion)
        mostrar_exito_impresion(page, ruta_pdf)

    def mostrar_confirmacion_imprimir_general(e):
        mostrar_confirmacion_impresion(
            page,
            "¿Deseas imprimir el listado general de donaciones en PDF?",
            imprimir_general
        )

    def mostrar_confirmacion_imprimir_individual(donacion):
        mostrar_confirmacion_impresion(
            page,
            f"¿Deseas imprimir la donación de {donacion['NOMBRE']} en PDF?",
            lambda: imprimir_individual(donacion)
        )

    def on_donante_change(e):
        seleccionado = e.control.value
        for donante in donantes:
            if donante[1] == seleccionado:
                id_donante.value = donante[0]
                cedula_field.value = donante[4]
                telefono_field.value = donante[2]
                correo_field.value = donante[3]
                direccion_field.value = donante[5]

        # Actualiza la vista
        page.update()

    selected_date_field = ft.TextField(label="Fecha de la Donación", 
                            width=250, 
                            read_only=True, 
                            prefix_icon=ft.Icons.CALENDAR_TODAY,
                            bgcolor="#f9f9f9",  # Fondo más claro
                            border_color="#ccc",  # Borde más suave
                            color="black",
                            border_radius=8, 
                            label_style=ft.TextStyle(color="black"))

    def handle_date_change(e):
        if e.data:  # Asegúrate de que e.data no sea None
            try:
                # Convertir la cadena a un objeto datetime
                date_object = datetime.datetime.strptime(e.data, "%Y-%m-%dT%H:%M:%S.%f")
                # Formatear la fecha al formato deseado
                selected_date_field.value = date_object.strftime("%Y-%m-%d")
            except ValueError:
                print("Formato de fecha no válido. Por favor, usa YYYY-MM-DD.")
            page.update()

    def open_date_picker(e):
        # Abre el DatePicker
        page.open(
            ft.DatePicker(
                first_date=datetime.datetime(year=2023, month=10, day=1),
                last_date=datetime.datetime(year=2025, month=12, day=1),
                on_change=handle_date_change,  # Asegúrate de que esta función esté correctamente referenciada
            )
        )

    # Inicializa el campo de fecha con la fecha actual
    selected_date_field.value = datetime.datetime.now().strftime("%Y-%m-%d")

    campos_dinamicos = ft.Column()
    list_view = ft.ListView(
        controls=campos_dinamicos.controls,
        height=350,
        auto_scroll=True
    )

    def crear_detalle(tipo=None, valores=None):
        tipo_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(p) for p in ["Monetaria", "Alimentos", "Medicamentos"]],
            label="Tipo de Donación",
            width=200,
            bgcolor="white",
            border_color=ft.Colors.TRANSPARENT,
            color="black",
            on_change=lambda e: actualizar_campos_detalle(e.control.value, campos_row, valores),
        )

        campos_row = ft.Row(
            spacing=15,
            wrap=True,
        )

        if tipo:
            actualizar_campos_detalle(tipo, campos_row, valores)

        detalle_row = ft.Container(  # Cambiamos a Container para mejor control del padding
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            tipo_dropdown,
                            ft.IconButton(
                                icon=ft.Icons.REMOVE,
                                on_click=lambda e: eliminar_detalle(detalle_row),
                                icon_color=wine
                            )
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    campos_row
                ],
                spacing=10,
            ),
            padding=ft.padding.only(bottom=20, top=10),  # Espaciado inferior de 20px
            border=ft.border.all(1, "#e0e0e0"),  # Borde sutil para diferenciar
            border_radius=8,
            bgcolor="#f9f9f9",  # Fondo ligeramente diferenciado
            margin=ft.margin.only(bottom=15),  # Margen inferior entre detalles
        )
        return detalle_row

    def actualizar_campos_detalle(tipo, campos_row, valores=None):
        campos_row.controls.clear()  # Limpiamos la fila de campos
        
        if tipo == "Monetaria":
            campos_row.controls.append(
                ft.TextField(label="Monto", width=120, prefix_icon=ft.Icons.ATTACH_MONEY, 
                            value=(valores or {}).get("Monto", ""),
                            bgcolor="white", border_color=ft.Colors.TRANSPARENT, color="black")
            )
            campos_row.controls.append(
                ft.TextField(label="Método de Pago", width=150, prefix_icon=ft.Icons.PAYMENT_ROUNDED, 
                            value=(valores or {}).get("Método de Pago", ""),
                            bgcolor="white", border_color=ft.Colors.TRANSPARENT, color="black")
            )
        elif tipo == "Alimentos":
            campos_row.controls.append(
                ft.TextField(label="Tipo de Alimento", width=150, prefix_icon=ft.Icons.FOOD_BANK, 
                            value=(valores or {}).get("Tipo de Alimento", ""),
                            bgcolor="white", border_color=ft.Colors.TRANSPARENT, color="black")
            )
            campos_row.controls.append(
                ft.TextField(label="Cantidad", width=150, prefix_icon=ft.Icons.ADD_CIRCLE_OUTLINE, 
                            value=(valores or {}).get("Cantidad", ""),
                            bgcolor="white", border_color=ft.Colors.TRANSPARENT, color="black")
            )
        elif tipo == "Medicamentos":
            campos_row.controls.append(
                ft.TextField(label="Nombre del Medicamento", width=180, prefix_icon=ft.Icons.MEDICATION, 
                            value=(valores or {}).get("Nombre del Medicamento", ""),
                            bgcolor="white", border_color=ft.Colors.TRANSPARENT, color="black")
            )
            campos_row.controls.append(
                ft.TextField(label="Cantidad", width=150, prefix_icon=ft.Icons.ADD_CIRCLE_OUTLINE, 
                            value=(valores or {}).get("Cantidad", ""),
                            bgcolor="white", border_color=ft.Colors.TRANSPARENT, color="black")
            )
        page.update()

    def agregar_detalle(e=None):
        detalle_row = crear_detalle()
        campos_dinamicos.controls.append(detalle_row)
        list_view.controls = campos_dinamicos.controls
        page.update()
    
    def guardar_edicion(donacion):
        def _guardar(e):
            if not validar_campos():
                return

            detalles_actualizados = []
            for row in campos_dinamicos.controls:
                tipo = row.content.controls[0].controls[0].value
                campos = row.content.controls[1].controls
                detalle = {"TIPO": tipo}
                for field in campos:
                    if tipo == "Monetaria" and field.label == "Monto":
                        detalle["MONTO"] = float(field.value)
                    elif tipo == "Monetaria" and field.label == "Método de Pago":
                        detalle["METODO_PAGO"] = field.value
                    elif tipo == "Alimentos" and field.label == "Tipo de Alimento":
                        detalle["DESCRIPCION"] = field.value
                    elif tipo == "Alimentos" and field.label == "Cantidad":
                        detalle["CANTIDAD"] = float(field.value)
                    elif tipo == "Medicamentos" and field.label == "Nombre del Medicamento":
                        detalle["DESCRIPCION"] = field.value
                    elif tipo == "Medicamentos" and field.label == "Cantidad":
                        detalle["CANTIDAD"] = float(field.value)
                detalles_actualizados.append(detalle)

            donacion_actualizada = {
                "donante_id": id_donante.value,
                "descripcion": descripcion.value,
                "fecha": selected_date_field.value,
                "detalles": detalles_actualizados,
            }


            donacion_id = donacion['ID_DONACION'] if isinstance(donacion, dict) else donacion[0]
            if controllerDonaciones.editar_donacion(donacion_id, donacion_actualizada):
                donaciones.clear()
                donaciones.extend(controllerDonaciones.cargar_donaciones() or [])
                lista_donaciones_lv.controls = crear_lista_donaciones(donaciones).controls
                limpiar_campos()
                cerrar_dialogo(page)
                mostrar_dialogo_exito(page, "Donación actualizada con éxito.")
                page.update()
            else:
                mostrar_dialogo_error(page, "No se pudo actualizar la Donación.")
        return _guardar




    def eliminar_detalle(detalle_row):
        campos_dinamicos.controls.remove(detalle_row)
        list_view.controls = campos_dinamicos.controls
        page.update()

    def confirmar_eliminacion(donacion):
        def _eliminar(e):
            donacion_id = donacion['ID_DONACION'] if isinstance(donacion, dict) else donacion[0]
            if controllerDonaciones.eliminar_donacion(donacion_id):
                try:
                    donaciones.clear()
                    donaciones.extend(controllerDonaciones.cargar_donaciones() or [])
                    lista_donaciones_lv.controls = crear_lista_donaciones(donaciones).controls
                    mostrar_dialogo_exito(page, "Donación eliminada con éxito.")
                    page.update()
                except ValueError:
                    print("La Donación no se encontró en la lista.")
            else:
                mostrar_dialogo_error(page, "No se puede eliminar la Donación.")
        return _eliminar

    def eliminar_donacion(donacion):
        usuario = page.session.get("usuario")
        if not usuario or (not usuario.get("eliminar") and not usuario.get("total")):
            page.open(ft.SnackBar(content=ft.Text("No tiene permiso para eliminar donaciones"), action="OK", bgcolor="red"))
            return
        def on_confirmar():
            confirmar_eliminacion(donacion)(None)
        mostrar_confirmacion(page, f"¿Estás seguro de que deseas eliminar la donación?", on_confirmar)

    # Agregar al inicio (con los otros campos):
    error_donante = ft.Text("", color="red", size=12)
    error_descripcion = ft.Text("", color="red", size=12)
    error_fecha = ft.Text("", color="red", size=12)
    error_detalles = ft.Text("", color="red", size=12)
    error_campos = ft.Text("", color="red", size=12)

    def validar_campos():
        errores = False
        
        # Limpiar errores anteriores
        error_donante.value = ""
        error_descripcion.value = ""
        error_fecha.value = ""
        error_detalles.value = ""
        error_campos.value = ""
        
        # Validación del donante
        if not str(id_donante.value):
            error_donante.value = "⚠️ Debes seleccionar un donante"
            errores = True

        # Validación de la descripción
        if not descripcion.value.strip():
            error_descripcion.value = "⚠️ Debes ingresar una descripción"
            errores = True

        # Validación de la fecha
        if not selected_date_field.value.strip():
            error_fecha.value = "⚠️ Debes seleccionar una fecha"
            errores = True

        # Validación de los detalles
        if not campos_dinamicos.controls:
            error_detalles.value = "⚠️ Debes agregar al menos un detalle"
            errores = True
        
        # Validación de campos dinámicos
        for row in campos_dinamicos.controls:
            tipo = row.content.controls[0].controls[0].value
            campos = row.content.controls[1].controls
            
            for field in campos:
                # Manejar campos numéricos y de texto de forma diferente
                if field.label in ["Monto", "Cantidad"]:
                    try:
                        # Solo verificar si es convertible a número
                        float(field.value)
                    except (ValueError, TypeError):
                        error_campos.value = f"⚠️ {field.label} debe ser numérico"
                        errores = True
                        break
                else:
                    # Para campos de texto
                    if not str(field.value).strip():
                        error_campos.value = f"⚠️ Completa el campo {field.label}"
                        errores = True
                        break
                
            if errores:
                break

        page.update()
        return not errores

    def limpiar_campos():
        # Limpiar campos del formulario
        fields_to_clear = [
            donante,id_donante, correo_field, cedula_field,
            direccion_field, telefono_field, descripcion,
            error_donante, error_descripcion, error_fecha,
            error_detalles, error_campos
        ]
        
        for field in fields_to_clear:
            field.value = "" if isinstance(field, ft.TextField) or isinstance(field, ft.Text) else None
        
        # Restablecer fecha actual
        selected_date_field.value = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Limpiar detalles dinámicos
        campos_dinamicos.controls.clear()
        list_view.controls = campos_dinamicos.controls
        
        # Limpiar selección del dropdown de donante
        if hasattr(page.dialog, "content") and hasattr(page.dialog.content, "content"):
            dialog_content = page.dialog.content.content
            if hasattr(dialog_content, "controls"):
                for container in dialog_content.controls:
                    if hasattr(container, "content") and hasattr(container.content, "controls"):
                        for control in container.content.controls:
                            if isinstance(control, ft.Dropdown):
                                control.value = None
                                break
        
        page.update()

    def crear_boton_editar(donacion):
        return ft.IconButton(icon=ft.Icons.EDIT,icon_color=cherry, on_click=lambda e: abrir_dialogo(donacion))

    def crear_boton_eliminar(donacion):
        return ft.IconButton(icon=ft.Icons.DELETE,icon_color=cherry, on_click=lambda e: eliminar_donacion(donacion))    

    def crear_lista_donaciones(donaciones):
        return ft.Column(
            controls=[
                ft.Divider(height=1, color="#e0e0e0"), 
                ft.Container(
                    bgcolor="#e6e6e6",
                    expand=True,
                    content=ft.Row([
                        ft.Text("Numero", weight="bold", color=cherry, width=100),
                        ft.Text("Fecha", weight="bold", color=cherry, width=150),
                        ft.Text("Donante", weight="bold", color=cherry, width=140),
                        ft.Text("Tipo de Donacion", weight="bold", color=cherry, width=200),
                        ft.Text("Descripcion", weight="bold", color=cherry, width=180),
                        ft.Text("Monto Total", weight="bold", color=cherry, width=100),
                        ft.Text("Cantidad Total de Ítems", weight="bold", color=cherry, width=200),
                        ft.Text("Acciones", weight="bold", color=cherry, width=80),
                    ], alignment=ft.MainAxisAlignment.START, spacing=5)
                ),
                ft.Divider(height=1, color="#e0e0e0"), 
            ] + [
                ft.Container(
                    content=ft.Row([
                        ft.Container(ft.Text(str(d['ID_DONACION']), color='black'), width=100),
                        ft.Container(ft.Text(str(d['FECHA']), color='black'), width=150), 
                        ft.Container(ft.Text(str(d['NOMBRE']), color='black'), width=140),  
                        ft.Container(
                            ft.Text(", ".join([detalle.get("TIPO", "") for detalle in d.get("detalles", [])]), color='black'),
                            width=200
                        ),
                        ft.Container(ft.Text(str(d['DESCRI']), color='black'), width=200),
                        # Monto Total
                        ft.Container(
                            ft.Text(str(sum(det.get("MONTO", 0) for det in d.get("detalles", []) if det.get("TIPO") == "Monetaria")), color='black'),
                            width=140
                        ),
                        # Cantidad Total de Ítems
                        ft.Container(
                            ft.Text(str(sum(det.get("CANTIDAD", 0) for det in d.get("detalles", []) if det.get("TIPO") in ["Alimentos", "Medicamentos"])), color='black'),
                            width=120
                        ),
                        ft.Row([
                            crear_boton_editar(d),  
                            crear_boton_eliminar(d),  
                            ft.IconButton(
                                icon=ft.Icons.PICTURE_AS_PDF,
                                tooltip="Imprimir donación",
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
                for d in donaciones
            ],
            spacing=5,
        )

    lista_donaciones = crear_lista_donaciones(donaciones)    

    def agregar_donacion(e):
        nonlocal donaciones
        if not validar_campos():
            return
            
        detalles = []
        for row in campos_dinamicos.controls:
            tipo = row.content.controls[0].controls[0].value
            campos = row.content.controls[1].controls
            detalle = {"TIPO": tipo}
            for field in campos:
                if tipo == "Monetaria" and field.label == "Monto":
                    detalle["MONTO"] = float(field.value)
                elif tipo == "Monetaria" and field.label == "Método de Pago":
                    detalle["METODO_PAGO"] = field.value
                elif tipo == "Alimentos" and field.label == "Tipo de Alimento":
                    detalle["DESCRIPCION"] = field.value
                elif tipo == "Alimentos" and field.label == "Cantidad":
                    detalle["CANTIDAD"] = float(field.value)
                elif tipo == "Medicamentos" and field.label == "Nombre del Medicamento":
                    detalle["DESCRIPCION"] = field.value
                elif tipo == "Medicamentos" and field.label == "Cantidad":
                    detalle["CANTIDAD"] = float(field.value)
            detalles.append(detalle)

        nueva_donacion = {
            "donante_id": id_donante.value,
            "descripcion": descripcion.value,
            "fecha": selected_date_field.value,
            "detalles": detalles,
        }

        # Si estamos editando, donacion_id estará definido en el contexto de editar
        if hasattr(agregar_donacion, 'donacion_id') and agregar_donacion.donacion_id is not None:
            donacion_id = agregar_donacion.donacion_id
            if controllerDonaciones.editar_donacion(donacion_id, nueva_donacion):
                donaciones = controllerDonaciones.cargar_donaciones()
                lista_donaciones.controls = crear_lista_donaciones(donaciones).controls
                limpiar_campos()
                cerrar_dialogo(page)
                mostrar_dialogo_exito(page, "Donación actualizada con éxito.")
                page.update()
            else:
                mostrar_dialogo_error(page, "No se pudo actualizar la Donación.")
        else:
            if controllerDonaciones.agregar_donacion(nueva_donacion):
                donaciones.clear()
                donaciones.extend(controllerDonaciones.cargar_donaciones() or [])
                lista_donaciones_lv.controls = crear_lista_donaciones(donaciones).controls
                limpiar_campos()
                cerrar_dialogo(page)
                mostrar_dialogo_exito(page, "Donación agregada con éxito.")
                page.update()
            else:
                mostrar_dialogo_error(page, "No se pudo agregar la Donación.")

    dialog = ft.AlertDialog(
        modal=False,
        bgcolor="white",
        title=ft.Text("Registro de Donación", size=20, weight="bold", text_align=ft.TextAlign.CENTER),
        content=ft.Container(
            content=ft.Row(
                controls=[
                    # Contenedor 1: Datos del Donante
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    "Datos del Donante",
                                    size=22,
                                    weight="bold",
                                    color=cherry
                                ),
                                ft.Column([error_donante, donante := ft.Dropdown(
                                    label="Donante",
                                    options=[ft.dropdown.Option(d[1]) for d in donantes],
                                    on_change=on_donante_change,
                                    width=300,
                                    prefix_icon=ft.Icons.PERSON_ROUNDED,
                                    bgcolor="#f9f9f9",  # Fondo más claro
                                    border_color="#ccc",  # Borde más suave
                                    color="black",
                                    border_radius=8, 
                                    label_style=ft.TextStyle(color="black" )
                                ),]),
                                (id_donante := ft.TextField(visible=False)),
                                (cedula_field := ft.TextField(
                                        label="Cédula",
                                        hint_text="Escribe la Cédula aquí",
                                        prefix_icon=ft.Icons.CREDIT_CARD,
                                        width=300,
                                        bgcolor="#f9f9f9",  # Fondo más claro
                                        border_color="#ccc",  # Borde más suave
                                        color="black",
                                        border_radius=8, 
                                        label_style=ft.TextStyle(color="black" )
                                    )
                                ),
                                (telefono_field := ft.TextField(
                                        label="Teléfono",
                                        hint_text="Escribe el Teléfono aquí",
                                        prefix_icon=ft.Icons.PHONE_ROUNDED,
                                        width=300,
                                        keyboard_type=ft.KeyboardType.NUMBER,
                                        bgcolor="#f9f9f9",  # Fondo más claro
                                        border_color="#ccc",  # Borde más suave
                                        color="black",
                                        border_radius=8, 
                                        label_style=ft.TextStyle(color="black" ) 
                                    )
                                ),
                                (correo_field := ft.TextField(
                                        label="Email",
                                        hint_text="Escribe el Email aquí",
                                        prefix_icon=ft.Icons.EMAIL_ROUNDED,
                                        width=300,
                                        bgcolor="#f9f9f9",  # Fondo más claro
                                        border_color="#ccc",  # Borde más suave
                                        color="black",
                                        border_radius=8, 
                                        label_style=ft.TextStyle(color="black" ) 
                                    )
                                ),
                                (direccion_field := ft.TextField(
                                        label="Dirección",
                                        hint_text="Escribe la Dirección aquí",
                                        prefix_icon=ft.Icons.MAPS_HOME_WORK,
                                        width=300,
                                        bgcolor="#f9f9f9",  # Fondo más claro
                                        border_color="#ccc",  # Borde más suave
                                        color="black",
                                        border_radius=8, 
                                        label_style=ft.TextStyle(color="black" ) 
                                    )
                                ),
                            ],
                            spacing=15,
                        ),
                        width=350,
                        padding=10,
                    ),
                    # Contenedor 2: Datos de la Donación
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    "Datos de la Donación",
                                    size=22,
                                    weight="bold",
                                    color=cherry
                                ),
                                ft.Row(
                                    controls=[ 
                                        ft.Column([error_fecha, selected_date_field]),
                                        ft.ElevatedButton(
                                            " ",
                                            icon=ft.Icons.CALENDAR_TODAY,
                                            on_click=open_date_picker
                                        )
                                    ] 
                                ),
                                error_descripcion,
                                descripcion := ft.TextField(label="Descripción", 
                                                            width=300, 
                                                            multiline=True, 
                                                            prefix_icon=ft.Icons.DESCRIPTION_ROUNDED,
                                                            bgcolor="#f9f9f9",  # Fondo más claro
                                                            border_color="#ccc",  # Borde más suave
                                                            color="black",
                                                            border_radius=8, 
                                                            label_style=ft.TextStyle(color="black" )),
                                ft.Row(
                                    controls=[
                                        ft.Text("Detalles de la Donación", weight="bold", color=cherry),
                                        error_campos,
                                        ft.IconButton(icon=ft.Icons.ADD, on_click=agregar_detalle, icon_color=wine)
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                list_view,
                            ],
                            spacing=10,
                        ),
                        width=450,
                        padding=10,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=10,
            width=800,
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo(page)),
            ft.ElevatedButton("Agregar", on_click=agregar_donacion)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = dialog
    
    def abrir_dialogo(donacion=None):
        usuario = page.session.get("usuario")
        limpiar_campos()
        if donacion:
            # Validar permiso antes de abrir el diálogo de editar
            if not usuario or (not usuario.get("modificar") and not usuario.get("total")):
                page.open(ft.SnackBar(content=ft.Text("No tiene permiso para editar donaciones"), action="OK", bgcolor="red"))
                return
            dialog.title = ft.Text(
                "Editar Donación",
                size=22,
                weight="bold",
                color=cherry,
                expand=True
            )
            id_donante.value = donacion['DONANTE_ID']
            cedula_field.value = donacion['CEDULA']    
            telefono_field.value = donacion['TELEFONO']
            correo_field.value = donacion['CORREO']       
            direccion_field.value = donacion['DIRECCION']       
            donante.value = donacion['NOMBRE']
            descripcion.value = donacion['DESCRI']
            selected_date_field.value = donacion['FECHA'].strftime("%Y-%m-%d")  # Asegúrate de que la fecha esté en el formato correcto
            campos_dinamicos.controls.clear()

            for detalle in donacion['detalles']:
                tipo = detalle.get("TIPO", "")
                valores = {}
                if tipo == "Monetaria":
                    valores = {
                        "Monto": detalle.get("MONTO", ""),
                        "Método de Pago": detalle.get("METODO_PAGO", "")
                    }
                elif tipo == "Alimentos":
                    valores = {
                        "Tipo de Alimento": detalle.get("DESCRIPCION", ""),
                        "Cantidad": detalle.get("CANTIDAD", "")
                    }
                elif tipo == "Medicamentos":
                    valores = {
                        "Nombre del Medicamento": detalle.get("DESCRIPCION", ""),
                        "Cantidad": detalle.get("CANTIDAD", "")
                    }
                nuevo_row = crear_detalle(tipo=tipo, valores=valores)
                nuevo_row.content.controls[0].controls[0].value = tipo
                campos_dinamicos.controls.append(nuevo_row)

            list_view.controls = campos_dinamicos.controls
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
                    on_click=guardar_edicion(donacion),
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
                page.open(ft.SnackBar(content=ft.Text("No tiene permiso para agregar donaciones"), action="OK", bgcolor="red"))
                return
            dialog.title = ft.Text(
                "Agregar Nueva Donación",
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
                    on_click=agregar_donacion,
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

    donaciones_mes_card = crear_estadisticas_card_donaciones(
        "Donaciones Mes",
        str(len(donaciones)),  # O el valor que corresponda
        ft.Icons.ATTACH_MONEY,
        "#660924",
        animar_card
    )

    lista_donaciones_lv = ft.ListView(
        controls=crear_lista_donaciones(donaciones).controls,
        expand=True,
        spacing=0,
        padding=0,
        auto_scroll=False
    )

    main_layout = ft.Container(
        ft.Column([
            # Encabezado
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text("Donaciones", color=cherry, size=24, weight="bold"),
                        ft.FloatingActionButton(icon=ft.Icons.ADD, bgcolor=wine, on_click=lambda e: abrir_dialogo()),
                        ft.Container(content=busqueda_input, expand=True),
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
            # Lista scrolleable de donaciones
            lista_donaciones_lv,
            # Tarjeta Donaciones Mes al final
            ft.Container(
                content=donaciones_mes_card,
                alignment=ft.alignment.bottom_right,
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
