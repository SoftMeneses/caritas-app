import flet as ft
from datetime import date, datetime
from views.navbar import NavBar
import os

from utils.excel_export import (
    exportar_donantes_excel,
    exportar_donaciones_excel,
    exportar_voluntarios_excel,
    exportar_jornadas_excel
)

from utils.impresion import (
    crear_pdf_listado_donantes,
    crear_pdf_listado_donaciones,
    crear_pdf_listado_voluntarios,
    crear_pdf_listado_jornadas,
    mostrar_confirmacion_impresion,
    mostrar_exito_impresion
)
from controllers.donantes_controller import DonantesController
from controllers.donaciones_controller import DonacionesController
from controllers.voluntarios_controller import VoluntariosController
from controllers.jornadas_controller import JornadasController

class Inicio:
    def __init__(self, page: ft.Page, navegar):
        self.page = page
        self.navegar = navegar
        self._configurar_entorno()
        self._crear_interfaz()

    def _configurar_entorno(self):
        self.page.title = "Cáritas San Cristóbal - Panel Principal"
        self.page.bgcolor = "#f5f5f5"
        self.page.padding = 0
        self.page.font_family = "Segoe UI"
        self.page.theme = ft.Theme(
            text_theme=ft.TextTheme(
                body_large=ft.TextStyle(color="black")
            )
        )

    def _imprimir_listado(self, tipo):
        REPORTES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'reportes')
        if not os.path.exists(REPORTES_DIR):
            os.makedirs(REPORTES_DIR)
        rutas = {
            "donantes": os.path.join(REPORTES_DIR, 'donantes_general.pdf'),
            "donaciones": os.path.join(REPORTES_DIR, 'donaciones_general.pdf'),
            "voluntarios": os.path.join(REPORTES_DIR, 'voluntarios_general.pdf'),
            "jornadas": os.path.join(REPORTES_DIR, 'jornadas_general.pdf'),
        }
        ruta = rutas[tipo]

        if tipo == "donantes":
            datos = DonantesController().cargar_donantes() or []
            crear_pdf_listado_donantes(ruta, datos)
        elif tipo == "donaciones":
            datos = DonacionesController().cargar_donaciones() or []
            crear_pdf_listado_donaciones(ruta, datos)
        elif tipo == "voluntarios":
            datos = VoluntariosController().cargar_voluntarios() or []
            crear_pdf_listado_voluntarios(ruta, datos)
        elif tipo == "jornadas":
            datos = JornadasController().cargar_jornadas() or []
            crear_pdf_listado_jornadas(ruta, datos)

        mostrar_exito_impresion(self.page, ruta)

    def _exportar_listado_excel(self, tipo):
        REPORTES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'reportes')
        if not os.path.exists(REPORTES_DIR):
            os.makedirs(REPORTES_DIR)
        rutas = {
            "donantes": os.path.join(REPORTES_DIR, 'donantes_general.xlsx'),
            "donaciones": os.path.join(REPORTES_DIR, 'donaciones_general.xlsx'),
            "voluntarios": os.path.join(REPORTES_DIR, 'voluntarios_general.xlsx'),
            "jornadas": os.path.join(REPORTES_DIR, 'jornadas_general.xlsx'),
        }
        ruta = rutas[tipo]

        if tipo == "donantes":
            datos = DonantesController().cargar_donantes() or []
            exportar_donantes_excel(ruta, datos)
        elif tipo == "donaciones":
            datos = DonacionesController().cargar_donaciones() or []
            exportar_donaciones_excel(ruta, datos)
        elif tipo == "voluntarios":
            datos = VoluntariosController().cargar_voluntarios() or []
            exportar_voluntarios_excel(ruta, datos)
        elif tipo == "jornadas":
            datos = JornadasController().cargar_jornadas() or []
            exportar_jornadas_excel(ruta, datos)

        mostrar_exito_impresion(self.page, ruta)

    def _mostrar_dialogo_exportar(self, e=None, modo="pdf"):
        iconos = {
            "donantes": ft.Icons.PEOPLE,
            "donaciones": ft.Icons.ATTACH_MONEY,
            "voluntarios": ft.Icons.GROUP,
            "jornadas": ft.Icons.EVENT,
        }
        opciones = [
            ("Listado de Donantes", "donantes"),
            ("Listado de Donaciones", "donaciones"),
            ("Listado de Voluntarios", "voluntarios"),
            ("Listado de Jornadas", "jornadas"),
        ]
        content = ft.Container(
            content=ft.Column([
                ft.Text("¿Qué listado deseas exportar?", weight="bold", size=18, color="#660924"),
                ft.Divider(height=10, color="transparent"),
            ] + [
                ft.TextButton(
                    content=ft.Row([
                        ft.Icon(iconos[tipo], color="#8C1313"),
                        ft.Text(text, color="#8C1313", weight="bold")
                    ], spacing=10),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        bgcolor={"": "#f8f8f8", "hovered": "#f2e6e6"},
                        side=ft.BorderSide(1, "#e0e0e0"),
                        padding=ft.padding.symmetric(vertical=12, horizontal=8),
                    ),
                    on_click=(lambda ev, t=tipo: self._confirmar_exportar(t, modo))
                )
                for text, tipo in opciones
            ], spacing=8),
            height=210,
            width=340
        )

        self.dialogo_exportar = ft.AlertDialog(
            modal=False,
            bgcolor="white",
            content=content,
            actions=[ft.TextButton("Cancelar", on_click=lambda e: self._cerrar_dialogo_exportar())],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = self.dialogo_exportar
        self.page.open(self.dialogo_exportar)
        self.page.update()
    
    def _cerrar_dialogo_exportar(self, e=None):
        if hasattr(self, "dialogo_exportar"):
            self.dialogo_exportar.open = False
            self.page.update()

    def _confirmar_exportar(self, tipo, modo="pdf"):
        self._cerrar_dialogo_exportar()
        tipo_texto = {
            "donantes": "¿Deseas exportar el listado de donantes?",
            "donaciones": "¿Deseas exportar el listado de donaciones?",
            "voluntarios": "¿Deseas exportar el listado de voluntarios?",
            "jornadas": "¿Deseas exportar el listado de jornadas?",
        }
        if modo == "pdf":
            mostrar_confirmacion_impresion(
                self.page,
                tipo_texto[tipo],
                lambda: self._imprimir_listado(tipo)
            )
        elif modo == "excel":
            mostrar_confirmacion_impresion(
                self.page,
                tipo_texto[tipo],
                lambda: self._exportar_listado_excel(tipo)
            )

    def _animar_card(self, e):
        """Animación al hacer hover sobre las tarjetas de estadísticas"""
        if e.data == "true":
            # Animación cuando el mouse entra
            e.control.scale = ft.Scale(1.05)
            e.control.bgcolor = ft.Colors.with_opacity(0.9, e.control.bgcolor)
        else:
            # Animación cuando el mouse sale
            e.control.scale = ft.Scale(1.0)
            e.control.bgcolor = ft.Colors.with_opacity(1.0, e.control.bgcolor)
        e.control.update()

    def _crear_estadisticas_card(self, titulo, valor, icono, color):
        """Crea una tarjeta de estadísticas con animación al hacer hover"""
        card = ft.Container(
            width=200,
            height=130,
            bgcolor=color,
            border_radius=10,
            padding=16,
            animate=ft.Animation(400, "easeOutQuad"),
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
            on_hover=lambda e: self._animar_card(e)
        )
        return card

    def _crear_item_evento(self, nombre, fecha, color):
        return ft.Container(
            bgcolor="#2e2e2e",
            border_radius=6,
            padding=6,
            content=ft.Row(
                controls=[
                    ft.Container(
                        width=4,
                        height=22,
                        bgcolor=color,
                        border_radius=4
                    ),
                    ft.VerticalDivider(width=6, color="transparent"),
                    ft.Column(
                        controls=[
                            ft.Text(nombre, weight="bold", color="white", size=12),
                            ft.Text(fecha, color="white70", size=10)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=1
                    )
                ]
            )
        )

    def _crear_proxima_jornada_card(self, nombre, fecha, ubicacion):
        return ft.Container(
            bgcolor="#e6e6e6",
            border_radius=10,
            padding=ft.padding.symmetric(vertical=18, horizontal=24),
            margin=ft.margin.only(bottom=10),
            animate=ft.Animation(400, "easeOutQuad"),      # <-- animación
            scale=ft.Scale(1.0),                           # <-- escala inicial
            on_hover=lambda e: self._animar_card(e),       # <-- animación al hover
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

    def _abrir_calendario_personalizado(self, jornadas, mes=None, anio=None):
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
                # Día con jornada: fondo de color y punto
                dias_grid.append(
                    ft.Container(
                        width=36,
                        height=36,
                        bgcolor="#ffe0e0",  # Fondo especial para jornadas
                        border_radius=18,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Text(str(dia), weight="bold", color="#8C1313"),
                            ft.Icon(ft.Icons.FIBER_MANUAL_RECORD, color="#8C1313", size=12)
                        ], spacing=0, alignment=ft.MainAxisAlignment.CENTER),
                        on_click=lambda e, j=jornada: self._mostrar_detalle_jornada(j)
                    )
                )
            else:
                # Día normal: fondo blanco, número negro
                dias_grid.append(
                    ft.Container(
                        width=36,
                        height=36,
                        bgcolor="white",  # Fondo blanco para días normales
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
            self._abrir_calendario_personalizado(jornadas, nuevo_mes, nuevo_anio)

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

        self.dialogo_calendario = ft.AlertDialog(
            modal=False,
            bgcolor="white",
            content=calendario,
            actions=[ft.TextButton("Cerrar", on_click=lambda e: self._cerrar_calendario_personalizado())],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = self.dialogo_calendario
        self.page.open(self.dialogo_calendario)
        self.page.update()

    def _cerrar_calendario_personalizado(self):
        if hasattr(self, "dialogo_calendario"):
            self.dialogo_calendario.open = False
            self.page.update()

    def _mostrar_detalle_jornada(self, jornada):
        detalle = ft.AlertDialog(
            modal=False,
            bgcolor="white",
            title=ft.Text("Detalle de Jornada", weight="bold", color="#660924"),
            content=ft.Column([
                ft.Text(f"Nombre: {jornada[2]}", color="#8C1313"),
                ft.Text(f"Fecha: {jornada[1]}", color="#145a7b"),
                ft.Text(f"Ubicación: {jornada[3]}", color="#348f50"),
                ft.Text(f"Estatus: {jornada[4]}", color="#888"),
            ], spacing=4,height=160),
            actions=[ft.TextButton("Cerrar", on_click=lambda e: self._cerrar_detalle_jornada())],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = detalle
        self.page.open(detalle)
        self.page.update()

    def _cerrar_detalle_jornada(self):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()


    def _crear_interfaz(self):
        Colors = {
            "primary": "#660924",
            "secondary": "#145a7b",
            "accent": "#348f50",
            "background": "#f5f5f5"
        }

        navbar = NavBar(self.page, self.navegar, cherry="#660924", wine="#630D13").view

         # --- OBTENER DATOS REALES ---
        donantes = DonantesController().cargar_donantes() or []
        donaciones = DonacionesController().cargar_donaciones() or []
        voluntarios = VoluntariosController().cargar_voluntarios() or []
        jornadas = JornadasController().cargar_jornadas() or []

        header = ft.Container(
            padding=ft.padding.only(top=80, bottom=10),
            content=ft.Row(
                controls=[
                    ft.Container(expand=True),
                    ft.Text("Caritas - San Cristóbal", size=45, weight="bold", color="#660924"),
                    ft.Container(expand=True),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        # --- TARJETAS CON DATOS REALES ---
        stats_grid = ft.Row(
            controls=[
                self._crear_estadisticas_card("Donantes Activos", str(len(donantes)), ft.Icons.PEOPLE, Colors["primary"]),
                self._crear_estadisticas_card("Donaciones Mes", str(len(donaciones)), ft.Icons.ATTACH_MONEY, Colors["secondary"]),
                self._crear_estadisticas_card("Voluntarios", str(len(voluntarios)), ft.Icons.GROUP, Colors["accent"]),
                self._crear_estadisticas_card("Jornadas Realizadas", str(len(jornadas)), ft.Icons.EVENT, Colors["primary"])
            ],
            spacing=18,
            alignment=ft.MainAxisAlignment.CENTER
        )

        # Configurar DatePicker
        date_picker = ft.DatePicker(
            first_date=date(2023, 1, 1),
            last_date=date(2024, 12, 31),
        )
        self.page.overlay.append(date_picker)
        
        # Botón para abrir el calendario
                # Botón para abrir el calendario con la estética de las tarjetas
        btn_abrir_calendario = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.CALENDAR_TODAY, color="white"),
                ft.Text("Ver Calendario", color="white", weight="bold")
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
            bgcolor="#8C1313",
            border_radius=10,
            padding=ft.padding.symmetric(vertical=12, horizontal=24),
            on_click=lambda e: self._abrir_calendario_personalizado(jornadas),  # <--- CAMBIA AQUÍ
            ink=True,
            animate=ft.Animation(400, "easeOutQuad"),
            width=200,
            height=50,
            alignment=ft.alignment.center,
            scale=ft.Scale(1.0),
            on_hover=lambda e: self._animar_card(e)
        )

        hoy = datetime.now().date()
        proxima = None
        for j in jornadas:
            # Suponiendo que j[1] es la fecha en formato 'YYYY-MM-DD'
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
            proxima_jornada_card = self._crear_proxima_jornada_card(
                proxima["nombre"],
                proxima["fecha"].strftime("%d/%m/%Y"),
                proxima["ubicacion"]
            )
        else:
            proxima_jornada_card = self._crear_proxima_jornada_card(
                "No hay próximas jornadas",
                "",
                ""
            )
            


        # Mostrar fecha seleccionada
        fecha_seleccionada = ft.Text()
        
        def handle_date_change(e):
            if date_picker.value:
                fecha_seleccionada.value = f"Fecha seleccionada: {date_picker.value.strftime('%d/%m/%Y')}"
                self.page.update()
        
        date_picker.on_change = handle_date_change

        main_content = ft.Container(
            padding=ft.padding.only(top=0, left=20, right=20, bottom=20),
            content=ft.Column(
                controls=[
                    stats_grid,
                    ft.Divider(height=30, color="transparent"),
                    ft.Container(
                        content=ft.Column([
                            
                            ft.Divider(height=10, color="transparent"),
                            proxima_jornada_card,  # <-- Aquí la tarjeta de próxima jornada
                            ft.Divider(height=10, color="transparent"),
                            btn_abrir_calendario,
                            ft.Divider(height=30, color="transparent"),
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Row([
                                            ft.Icon(ft.Icons.PICTURE_AS_PDF, color="white"),
                                            ft.Text("Exportar PDF", color="white", weight="bold")
                                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                                        bgcolor="#8C1313",
                                        border_radius=10,
                                        padding=ft.padding.symmetric(vertical=12, horizontal=24),
                                        on_click=self._mostrar_dialogo_exportar,
                                        ink=True,
                                        animate=ft.Animation(400, "easeOutQuad"),
                                        width=200,
                                        height=50,
                                        alignment=ft.alignment.center,
                                        scale=ft.Scale(1.0),  # <-- Añade esto
                                        on_hover=lambda e: self._animar_card(e)
                                    ),
                                    ft.Container(
                                        content=ft.Row([
                                            ft.Icon(ft.Icons.TABLE_VIEW, color="white"),
                                            ft.Text("Exportar Excel", color="white", weight="bold")
                                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                                        bgcolor="#8C1313",
                                        border_radius=10,
                                        padding=ft.padding.symmetric(vertical=12, horizontal=24),
                                        on_click=lambda e: self._mostrar_dialogo_exportar(modo="excel"),
                                        ink=True,
                                        animate=ft.Animation(400, "easeOutQuad"),
                                        width=200,
                                        height=50,
                                        alignment=ft.alignment.center,
                                        scale=ft.Scale(1.0),
                                        on_hover=lambda e: self._animar_card(e)
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=20
                            )
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        alignment=ft.alignment.center
                    )
                ],
                alignment=ft.MainAxisAlignment.START
            ),
            alignment=ft.alignment.top_center
        )

        layout_principal = ft.Row(
            controls=[
                navbar,
                ft.Column(
                    expand=True,
                    controls=[
                        header,
                        ft.Container(
                            content=main_content,
                            alignment=ft.alignment.center,
                            expand=True
                        )
                    ]
                )
            ],
            expand=True
        )

        self.page.window_width = 1200
        self.page.window_height = 700
        self.page.add(layout_principal)

    def _imprimir_informes(self):
        # Lógica para imprimir informes
        print("Imprimiendo informes...")

    def _exportar_a_pdf(self):
        # Lógica para exportar a PDF
        print("Exportando a PDF...")


def main(page: ft.Page, navegar):
    Inicio(page, navegar)
